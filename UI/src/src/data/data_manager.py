"""This module will handle all the data and the connection between the Pi and Arduino."""
from PyQt5 import QtCore
from ..data.log_handler import LogWriter
from ..backend.read_tank_sensor import TankReader
from ..backend.serial_communicator2 import SerialCommunicator
from ..backend.loads import Loads
from ..backend.halogen import HalogenLight
from ..serial.serial_page import SerialRaw

class DataManager():
    """This class contains all data."""
    def __init__(self, serial):
        self.mode = ''
        self.last_mode = ''
        self.scenario = ''
        self.manual = [0, 0, 0]

        self.solar_val = 0
        self.wind_val = 0
        self.demand_val = 0
        self.tank_val = 0

        self.mode_changed_handlers = []
        self.sensor_readings_handlers = []
        self.control_values_handlers = []
        self.storage_cal = 0

        if not serial:
            printer = SerialRaw()
            printer.print("No second screen found.")
        else:
            printer = serial

        self.light = HalogenLight(printer)
        self.tank_reader = TankReader()
        self.serial_connection = SerialCommunicator(printer)
        self.loads = Loads(printer)
        self.CONNECTED = self.serial_connection.CONNECTION              #pylint: disable=invalid-name
        self.file = LogWriter()

        self.update_timer = QtCore.QTimer()
        self.update_timer.timeout.connect(self.update_data)
        self.update_timer.start(100)

        self.time_running = QtCore.QTime()
        self.time_running.start()

    def set_mode(self, mode, mode_details):
        """Update the mode in which the system is running."""
        self.mode = mode

        if mode == 'manual':
            self.manual = mode_details
            if self.last_mode != 'manual':
                self.time_running.restart()
        elif mode == 'scenario':
            self.scenario = mode_details
            self.time_running.restart()
        elif mode == 'stop':
            pass
        else:
            raise ValueError(f"Mode should be either 'manual', 'scenario' or 'stop',"
                             f"but was equal to '{mode}'")
        
        self.mode_changed()
        self.last_mode = mode
    
    def get_mode(self):
        """Update the mode."""
        if self.mode == 'manual':
            return self.mode, self.manual

        if self.mode == 'scenario':
            return self.mode, self.scenario
     
        return self.mode, None

    def mode_changed(self):
        """Execute all the connected functions that want to know when the mode changes."""
        for handler in self.mode_changed_handlers:
            handler() 
    
    def connect_for_mode_change(self, handler):
        """Add function that will be executed when the mode changes."""
        self.mode_changed_handlers.append(handler)
    
    def set_storage_value(self, volume):
        """Update the value with the calibrated value."""
        self.tank_reader.set_calibrate(volume)
    
    def connect_for_sensor_readings(self, handler):
        """Add a function that want to get data when updated."""
        self.sensor_readings_handlers.append(handler)

    def send_sensor_readings(self, readings):
        """Execute all the connected functions that want to know when we get sensor data."""
        for handler in self.sensor_readings_handlers:
            handler(readings)
    
    def connect_for_all_values(self, handler):
        """Add a function that want to get the control values."""
        self.control_values_handlers.append(handler)
        
    def update_data(self):
        """First send data to Arduino and to lamp/loads. Then get readings."""
        values = self.values_for_control() 

        #To do: sent data for solar panel to dimmer.
        self.light.set_light(values[0])
        
        self.serial_connection.send_to_arduino(windPower=values[1])
        self.loads.load_set(values[2])

        try:
            readings = self.serial_connection.read_arduino()
        except Exception as error:
            print(error)
            readings = values.copy()
        
        data = []
        sensors = ['solar_power', 'wind_power', 'power_demand']

        for sensor in sensors:
            if sensor in readings:
                data.append(readings[sensor])
            else:
                data.append(values[sensors.index(sensor)])

        data.append(self.tank_reader.read_tank_level())
        data.append(self.time_running.elapsed() / 1000)

        for handler in self.control_values_handlers:
            handler(values, data)

        self.file.add_data_to_write(values, data)
    

    def values_for_control(self):
        """Retrieve the values from the scenario/manual control."""
        if self.mode == 'manual':
            return self.manual
        
        if self.mode == 'scenario':
            return self.scenario.get_values_at(self.time_running.elapsed() / 1000)
        
        return [0, 0, 0]    
