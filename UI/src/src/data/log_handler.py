"""This module takes care of writing data to the log-file."""

import csv

class LogWriter():
    """This class writes data to the log-file."""

    def __init__(self):
        try:
            with open('UI/log.csv', 'w', newline='') as file:
                log_file = csv.writer(file)
                log_file.writerow([0, 'Log file'])
            #log_file = open('UI/log.txt', 'w')
        except FileNotFoundError:
            with open('log.csv', 'w', newline='') as file:
                log_file = csv.writer(file)
                log_file.writerow([0, 'Log file'])

        self.max_length = 1000
        self.n = 1
        self.solar_write = []
        self.wind_write = []
        self.demand_write = []

        self.solar_curr = []
        self.wind_curr = []
        self.demand_curr = []
        self.elec_curr = []
        self.fuel_curr = []

        self.tank_level = []
        self.time = []

    
    def add_data_to_write(self, data_write, sensor_data):
        """Add data to the queue to write when full."""
        
        self.solar_write.append(data_write[0])
        self.wind_write.append(data_write[1])
        self.demand_write.append(data_write[2])

        self.solar_curr.append(sensor_data['solar_current'])
        self.wind_curr.append(sensor_data['wind_current'])
        self.demand_curr.append(sensor_data['load_current'])
        self.tank_level.append(sensor_data['tank_level'])
        self.time.append(sensor_data['time'])

        if len(self.solar_write) >= self.max_length:
            self.write()

            self.solar_write = []
            self.wind_write = []
            self.demand_write = []

            self.solar_curr = []
            self.wind_curr = []
            self.demand_curr = []
            self.elec_curr = []
            self.fuel_curr = []

            self.tank_level = []
            self.time = []
        
    def write(self):
        """Write data to the file."""

        try: 
            with open('UI/log.csv', 'a', newline='') as file:
                log_file = csv.writer(file)
                for i in range(len(self.solar_write)):
                    log_file.writerow([self.n, f"S:{self.solar_write[i]:5.1f}%", f"W:{self.wind_write[i]:5.1f}%", f"D:{self.demand_write[i]:5.1f}%",
                                               f"S:{self.solar_curr[i]:5.1f}mA", f"W:{self.wind_curr[i]:5.1f}mA", f"D:{self.demand_curr[i]:5.1f}mA",
                                               f"T:{self.tank_level[i]:5.1f}mL", f"t:{self.time[i]:4.1f}s"])
                    self.n += 1
        
        except FileNotFoundError:
            with open('log.csv', 'a', newline='') as file:
                log_file = csv.writer(file)
                for i in range(len(self.solar_write)):
                    log_file.writerow([self.n, f"S:{self.solar_write[i]:5.1f}%", f"W:{self.wind_write[i]:5.1f}%", f"D:{self.demand_write[i]:5.1f}%",
                                               f"S:{self.solar_curr[i]:5.1f}mA", f"W:{self.wind_curr[i]:5.1f}mA", f"D:{self.demand_curr[i]:5.1f}mA",
                                               f"T:{self.tank_level[i]:5.1f}mL", f"t:{self.time[i]:4.1f}s"])
                    self.n += 1
          
    
    def close(self):
        """When closed, the last data should still be written to the file."""
        self.write()
