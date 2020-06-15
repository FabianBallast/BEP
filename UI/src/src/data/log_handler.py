"""This module takes care of writing data to the log-file."""

import csv
import numpy as np
from time import time

headers = ['SolarRef (%)', 'WindRef (%) UI', 'LoadRef (%)', 'SolarU (V)','LoadI (mA)', 'WindU (V)',
                                    'Fuel cell U (V)', 'Fuel cell pwm (0-255)', 'ElectrolyzerU (V)', 'ElectrolyzerI (mA)','Electrolyzer pwm (0-255)',
                                    'gridU (V)','H2Ref byte (0-255)', 'looptime (ms)','fanRaw (%) dimmer', 'wind pwm (0-255)',  'Total current multiplier (mA)',
                                    'zon power (W)', 'wind power (W)', 'fuel cell flow (-)', 'Tanklevel (mL)', 't (s)']

keys = ['-', '-', '-', 'zonU', 'loadI', 'windU', 'FC_U', 'FC_Y', 'EL_U', 'EL_I', 'EL_Y', 'gridU', 'H2ref', 'loopT', 'fan', 'windY',
        'curr_to_add', 'zonPower','windPower', 'loadPower', 'tank_level', 'time']

log_name = 'logFiles/log'+str(int(time()))+'.csv'

assert len(headers)==len(keys)

class LogWriter():
    """This class writes data to the log-file."""

    def __init__(self, printer):
        self.printer = printer

        try:
            with open('UI/' + log_name, 'w', newline='') as file:
                log_file = csv.writer(file)
                log_file.writerow(headers)
            #log_file = open('UI/log.txt', 'w')
        except FileNotFoundError:
            with open(log_name, 'w', newline='') as file:
                log_file = csv.writer(file)
                log_file.writerow(headers)

        self.max_length = 100
        self.n = 1
        self.data_matrix = [[] for i in range(len(headers))]
       
    
    def add_data_to_write(self, data_write, sensor_data):
        """Add data to the queue to write when full."""
        for i_key in range(len(keys)):
            if i_key < 3:
                value = data_write[i_key]
            else:
                value = sensor_data[keys[i_key]]
              #  if keys[i_key] =='windU' :
               #     self.printer.print(str(value))

            #print(value)
            self.data_matrix[i_key].append(value)
        


        if len(self.data_matrix[0]) >= self.max_length:
            self.write()

            self.data_matrix = [[] for i in range(len(headers))]
        
    def write(self):
        """Write data to the file."""
        self.printer.print('Data opgeslagen' )
        try: 
            with open('UI/' + log_name, 'a', newline='') as file:
                log_file = csv.writer(file)
                data_t = np.array(self.data_matrix).T
                #self.printer.print(str(len(data_t)))
                for i in range(len(data_t)):
                    log_file.writerow(data_t[i])
                    #self.n += 1
        
        except FileNotFoundError:
            with open(log_name, 'a', newline='') as file:
                log_file = csv.writer(file)
                data_t = np.array(self.data_matrix).T
                for i in range(len(data_t)):
                    log_file.writerow(data_t[i])
        
        self.data_matrix = [[]]*len(headers)
    
    def close(self):
        """When closed, the last data should still be written to the file."""
        self.write()
