"""This class handles the sensor for reading the tank level."""

from time import time
try:
    import board
except NotImplementedError:
    from ..dummy import dummy_board as board                            #pylint: disable=relative-beyond-top-level

try:
    import RPi.GPIO as IO
except ModuleNotFoundError:
    print("using dummy gpio")
    from ..dummy import dummy_io as IO                      #pylint: disable=relative-beyond-top-level


Kp_wind = 3
Ki_wind = 2
Kd_wind = 1

WIND_MOSFET_PIN = 24

class WindMPPT:


    """This class represents the sensor."""
    def __init__(self, N_FILTER=30):
        self.current_wind_voltage = 0
        
        self.N_FILTER = N_FILTER     
        self.current_error = 0
        self.prev_error = 0
        self.cum_error = 0                               #pylint: disable=invalid-name
        self.prev_time = time()

        self.pwm = IO.PWM(WIND_MOSFET_PIN, 100)
        self.pwm.start(100)

    def controlMPPT(self, readings):
        opt = self.findMPPT(readings['windU'], readings['fan'])
        wind_control_value, wind_duty_cycle = self.windPID(opt, readings['windU'])
        self.pwm.ChangeDutyCycle(wind_duty_cycle)    

        return wind_control_value, wind_duty_cycle
    
    def findMPPT(self, new_wind_voltage, current_wind_strength):
        """Find optimal volt"""
        opt_wind_voltage = 4.35
        #insert lookup table
        return opt_wind_voltage
    
    def windPID(self, target_voltage, current_voltage):
        newTime = time()
        elapsedTime = self.prev_time - newTime
        
        self.current_error = target_voltage - current_voltage
        self.cum_error += self.current_error*elapsedTime
        self.rate_error = (self.current_error - self.prev_time)/elapsedTime
    	
        self.prev_time = newTime

        wind_control_value = 50 + Kp_wind* self.current_error +  Ki_wind* self.cum_error + Kd_wind* self.rate_error
        
        
        if wind_control_value > 100:
            wind_duty_cycle    = 100
        elif wind_control_value < 0:
            wind_duty_cycle    = 0
        else:
            wind_duty_cycle    = wind_control_value

        return wind_control_value, wind_duty_cycle


if __name__ == '__main__':
    mppt = WindMPPT()
    
    
