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
    def __init__(self, serial, last_data_box):
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
            self.printer = SerialRaw()
            self.printer.print("No second screen found.")
        else:
            self.printer = serial
        
        self.last_data_box = last_data_box

        self.light = HalogenLight(self.printer)
        
        self.serial_connection = SerialCommunicator(self.printer)
        self.loads = Loads(self.printer)
        self.NOT_CONNECTED = self.serial_connection.NO_CONNECTION              #pylint: disable=invalid-name
        self.tank_reader = TankReader(self, self.NOT_CONNECTED)

        self.file = LogWriter()

        self.update_timer = QtCore.QTimer()
        self.update_timer.timeout.connect(self.update_data)
        self.update_timer.start(200)

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
        readings = self.serial_connection.read_arduino()
        

        
        if 'dummy_serial' in readings:
            sensors = ['zonI', 'windI', 'loadI', 'EL_I', 
                       'PS_I', 'FC_I', 'OptWindI', 'EV_U', 'FC_U','gridU', 'loopT']
            
            for sensor in sensors:
                try:
                    readings[sensor] = values[sensors.index(sensor)]
                except IndexError:
                    readings[sensor] = 0
            

        readings['tank_level'] = self.tank_reader.read_tank_level()
        readings['time'] = self.time_running.elapsed() / 1000
        self.last_data_box.update(readings)
        
        
        for handler in self.control_values_handlers:
            handler(values, readings)
        
        self.send_sensor_readings(readings)

        self.file.add_data_to_write(values, readings)
        

    def values_for_control(self):
        """Retrieve the values from the scenario/manual control."""
        if self.mode == 'manual':
            return self.manual
        
        if self.mode == 'scenario':
            return self.scenario.get_values_at(self.time_running.elapsed() / 1000)
        
        return [0, 0, 0]    
