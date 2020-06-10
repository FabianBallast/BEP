"""This module takes care of writing data to the log-file."""

import csv
import numpy as np

headers = ['SolarRef (%)', 'WindRef (%) UI', 'LoadRef (%)', 'SolarU (V)','LoadI (mA)', 'WindU (V)',
                                    'Fuel cell U (V)', 'Fuel cell pwm (0-255)', 'ElectrolyzerU (V)', 'ElectrolyzerI (mA)','Electrolyzer pwm (0-255)',
                                    'gridU (V)','H2 pwm (0-255)', 'looptime (ms)','fanRaw (%) dimmer', 'wind pwm (0-255)',  'mismatch flow (-)',
                                    'zon flow (-)', 'wind flow (-)', 'fuel cell flow (-)', 'Tanklevel (mL)', 't (s)']

keys = ['-', '-', '-', 'zonU', 'loadI', 'windU', 'FC_U', 'FC_Y', 'EL_U', 'EL_I', 'EL_Y', 'gridU', 'gridX', 'loopT', 'fan', 'windY',
        'flowTot', 'zonFlow','windFlow', 'FC_flow', 'tank_level', 'time']


assert len(headers)==len(keys)

class LogWriter():
    """This class writes data to the log-file."""

    def __init__(self):
        try:
            with open('UI/log.csv', 'w', newline='') as file:
                log_file = csv.writer(file)
                log_file.writerow(headers)
            #log_file = open('UI/log.txt', 'w')
        except FileNotFoundError:
            with open('log.csv', 'w', newline='') as file:
                log_file = csv.writer(file)
                log_file.writerow(headers)

        self.max_length = 1000
        self.n = 1
        self.data_matrix = [[] for i in range(len(headers))]
       
    
    def add_data_to_write(self, data_write, sensor_data):
        """Add data to the queue to write when full."""
        for i_key in range(len(keys)):
            if i_key < 3:
                value = data_write[i_key]
            else:
                value = sensor_data[keys[i_key]]

            #print(value)
            self.data_matrix[i_key].append(value)
        


        if len(self.data_matrix[0]) >= self.max_length:
            self.write()

            self.data_matrix = [[]]*len(headers)
        
    def write(self):
        """Write data to the file."""

        try: 
            with open('UI/log.csv', 'a', newline='') as file:
                log_file = csv.writer(file)
                data_t = np.array(self.data_matrix).T
                for i in range(len(data_t)):
                    log_file.writerow(data_t[i])
                    #self.n += 1
        
        except FileNotFoundError:
            with open('log.csv', 'a', newline='') as file:
                log_file = csv.writer(file)
                data_t = np.array(self.data_matrix).T
                for i in range(len(data_t)):
                    log_file.writerow(data_t[i])
          
    
    def close(self):
        """When closed, the last data should still be written to the file."""
        self.write()
