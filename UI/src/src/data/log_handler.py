"""This module takes care of writing data to the log-file."""

class LogWriter():
    """This class writes data to the log-file."""

    def __init__(self):
        log_file = open('UI/log.txt', 'w')
        log_file.write('Log file')
        log_file.close()

        self.max_length = 1000

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

        self.solar_curr.append(sensor_data[0])
        self.wind_curr.append(sensor_data[1])
        self.demand_curr.append(sensor_data[2])
        self.tank_level.append(sensor_data[3])
        self.time.append(sensor_data[4])

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
        log_file = open('UI/log.txt', 'a')

        for i in range(len(self.solar_write)):
            log_file.write(f"\nOutput: S:{self.solar_write[i]:5.1f}%, "
                                     f"W:{self.wind_write[i]:5.1f}%, "
                                     f"D:{self.demand_write[i]:5.1f}%. "
                           f"   Input: S:{self.solar_curr[i]:5.1f}mA, "
                                     f"W:{self.wind_curr[i]:5.1f}mA, "
                                     f"D:{self.demand_curr[i]:5.1f}mA, "
                                    # f"E:{self.elec_curr[i]}mA, "
                                    # f"F:{self.fuel_curr[i]}mA, "
                                     f"T:{self.tank_level[i]:5.1f}mL at {self.time[i]:4.1f}s")
        
        log_file.close()
    
    def close(self):
        """When closed, the last data should still be written to the file."""
        self.write()
