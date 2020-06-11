"""This module will handle all the data and the connection between the Pi and Arduino."""
from PyQt5 import QtCore
from ..data.log_handler import LogWriter
from ..backend.read_tank_sensor import TankReader
from ..backend.serial_communicator2 import SerialCommunicator
from ..backend.loads import Loads
from ..backend.windControl import WindMPPT
from ..backend.gridControl import gridControlMultiply
from ..backend.purger import ValvePurger
from ..backend.halogen import HalogenLight
from ..serial.serial_page import SerialRaw
from ..power_curves.readPowerCurve  import convertSolarToPower, convertWindToPower
import numpy as np

MULTIPLIER_SOLAR      = 3
MULTIPLIER_WIND       = 24
MULTIPLIER_FUEL_CELL  = 0


def current_to_add(readings):
        power_to_add = readings['zonPower'] * (MULTIPLIER_SOLAR - 1) + readings['windPower'] * (MULTIPLIER_WIND - 1) #+ current_fuel_cell * (MULTIPLIER_FUEL_CELL - 1)
        volt = readings['gridU']
        if volt < 1: volt = 12
        curr_to_add = power_to_add/volt
        return curr_to_add


def current_mismatch(readings):
        power_to_add = readings['zonPower'] * (MULTIPLIER_SOLAR) + readings['windPower'] * (MULTIPLIER_WIND) - readings['loadPower'] #+ current_fuel_cell * (MULTIPLIER_FUEL_CELL - 1)
        volt = readings['gridU']
        if volt < 1: volt = 12
        curr_to_add = power_to_add/volt
        return curr_to_add

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


        self.windMPPT = WindMPPT()
        self.gridPID  = gridControlMultiply()
        self.valve = ValvePurger(self.printer)
        self.light = HalogenLight(self.printer, 0)
        
        self.serial_connection = SerialCommunicator(self.printer)
        self.loads = Loads(self.printer)
        self.NOT_CONNECTED = self.serial_connection.NO_CONNECTION              #pylint: disable=invalid-name
        self.tank_reader = TankReader(self.serial_connection)

        self.file = LogWriter(self.printer)

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

    def purge_valve_manual(self):
        self.valve.timeValve(1000, 1000)

    def update_data(self):
        """First send data to Arduino and to lamp/loads. Then get readings."""
        values = self.values_for_control() 

        
        #To do: sent data for solar panel to dimmer.
        self.light.set_light(values[0])
        
        
        
        readings = self.serial_connection.read_arduino()
        windControl, windDuty = self.windMPPT.controlMPPT(readings)

        readings['windControl'] = windControl
        #readings['windDuty'] = windDuty
        readings['zonPower'] = convertSolarToPower(values[0], readings['zonU'])
        readings['windPower'] = convertWindToPower(readings['fan'], readings['windU'])
        readings['loadPower'] = readings['gridU']*readings['loadI']

        readings['curr_to_add'] = current_mismatch(readings)
        readings['h2_control_value'] = self.gridPID.controlPSmultiply(readings)

        #h2ref = 0
        h2ref = readings['h2_control_value']+128
        
        #if len(values)>3:
        #    h2ref = (values[3] - 50) + 128
        #else:
        #    h2ref = 0

        # readings['zonFlow'] = readings['zonU']*20
        # readings['windFlow']= readings['windU']*0.3
        # readings['FC_flow'] = readings['FC_U']*14
        #readings['mismatch'] = readings['PS_I'] - readings['zonI'] - readings['windI'] - readings['FC_I']
        
        if h2ref>255:    h2ref = 255
        if h2ref<1:      h2ref = 0
        if np.isnan(h2ref): h2ref = 0
        h2ref = int(h2ref)

        self.serial_connection.send_to_arduino(windPower=values[1], windMosfet=windDuty, h2 = h2ref)
                

        self.loads.load_set(values[2])
        
        if 'dummy_serial' in readings:
            sensors = ['zonU', 'windU', 'loadI', 'EL_I','windU','flowTot',
                       'PS_I', 'FC_I', 'fan', 'EV_U', 'FC_U','FC_Y','gridU', 'loopT', 'windY']
            
            for sensor in sensors:
                try:
                    readings[sensor] = values[sensors.index(sensor)]
                except IndexError:
                    readings[sensor] = 0
            
        # self.valve.timeValve(readings['FC_Y'], 100)
        


        readings['tank_level'] = self.tank_reader.read_tank_level()
        readings['time'] = self.time_running.elapsed() / 1000
        self.file.add_data_to_write(values, readings)

        self.last_data_box.update(readings)
        
        
        for handler in self.control_values_handlers:
            handler(values, readings)
        
        
        self.send_sensor_readings(readings)

                

    def values_for_control(self):
        """Retrieve the values from the scenario/manual control."""
        if self.mode == 'manual':
            return self.manual
        
        elif self.mode == 'scenario':
            return self.scenario.get_values_at(self.time_running.elapsed() / 1000)
#        else:
#            print("mode=", self.mode)
        return [0, 0, 0]    
