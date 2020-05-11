"""This module will handle all the data and the connection between the Pi and Arduino."""
from PyQt5 import QtCore
#from ..backend.readTankSensor import TankReader
#from ..backend.SerialCommunicator import SerialCommunicator
#from ..backend import Loads
class DataManager():
    """This class contains all data."""
    def __init__(self):
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
        self.storage_cal = 0

        #self.tank_reader = TankReader()
        #self.serial_connection = SerialCommunicator()

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
        
    def update_data(self):
        """First send data to Arduino and to lamp/loads. Then get readings."""
        values = self.values_for_control()

        #print(f"Data for control: solar power: {values[0]}, wind power: {values[1]} and power demand: {values[2]}.")

        #To do: sent data for solar panel to dimmer.
        #self.serial_connection.sendToArduino(windPower=values[1])
        #Loads.load_set(values[2])

        #readings = self.serial_connection.readArduino()
        #readings = {'wind_power': 5,
        #            'solar_power': 2,
        #            'power_demand': 1}
        readings = dict()
        data = []
        sensors = ['solar_power', 'wind_power', 'power_demand']

        for sensor in sensors:
            if sensor in readings:
                data.append(readings[sensor])
            else:
                if self.mode == 'manual':
                    data.append(values[sensors.index(sensor)] / 20)
                else:
                    data.append(values[sensors.index(sensor)])

        #data.append(self.tank_reader.readTankLevel())
        data.append(50)
        data.append(self.time_running.elapsed() / 1000)

       # print(f"Data from sensors: solar power: {data[0]}, wind power: {data[1]}, "
       #                         f"power demand: {data[2]} and tank level: {data[3]}")

        self.send_sensor_readings(data)
    

    def values_for_control(self):
        """Retrieve the values from the scenario/manual control."""
        if self.mode == 'manual':
            return self.manual
        
        if self.mode == 'scenario':
            return self.scenario.get_values_at(self.time_running.elapsed() / 1000)
        
        return [0, 0, 0]
    