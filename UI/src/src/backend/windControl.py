"""This class handles the sensor for reading the tank level."""

import time
import numpy as np



Kp_wind = 90
Ki_wind = 50
Kd_wind = 10

class WindMPPT:


    def __init__(self):
        self.current_wind_voltage = 0   
        self.current_error = 0
        self.prev_error = 0
        self.cum_error = 0                               #pylint: disable=invalid-name
        self.prev_time = time.time()
        self.prev_error = 0
        

    def controlMPPT(self, readings):
        opt = self.findMPPT(readings['windU'], readings['fan'])
        wind_control_value, wind_duty_cycle = self.windPID(opt, readings['windU'])

        return wind_control_value, wind_duty_cycle
    
    def findMPPT(self, new_wind_voltage, current_wind_strength):
        """Find optimal volt"""
        opt_wind_voltage = 4.35
        #insert lookup table
        return opt_wind_voltage
    
    def windPID(self, target_voltage, current_voltage):
        newTime = time.time()
        elapsedTime = newTime - self.prev_time
        
        self.current_error = current_voltage - target_voltage
        self.cum_error += self.current_error*elapsedTime
        if abs(self.cum_error)*Ki_wind > 255:
            self.cum_error = np.sign(self.cum_error)*255/Ki_wind
        self.rate_error = (self.current_error - self.prev_error)/elapsedTime
        
        self.prev_time = newTime
        self.prev_error = self.current_error

        wind_control_value = 128 + Kp_wind* self.current_error +  Ki_wind* self.cum_error + Kd_wind* self.rate_error
        
        
        if wind_control_value > 255:
            wind_duty_cycle    = 255
        elif wind_control_value < 0:
            wind_duty_cycle    = 0
        else:
            wind_duty_cycle    = wind_control_value

        return wind_control_value, wind_duty_cycle


if __name__ == '__main__':
    mppt = WindMPPT()
    time.sleep(10)
    
