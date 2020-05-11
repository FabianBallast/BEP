#import board
#import RPi.GPIO as IO

class HalogenLight:
    def __init__(self):
        """wrapper for dimmable halogenlight with slow start"""
        HALOGEN_MOSFET_PIN = 18
        self.start_value = 0
        # IO.setmode(IO.BCM)
        # IO.setup(HALOGEN_MOSFET_PIN, IO.OUT)

        # self.pwm = IO.PWM(led, 100)
        # self.pwm.start(0)
    
    def set_light(self, set_value):
        """input value between 0-100"""
        #self.pwm.ChangeDutyCycle(set_value)
        if ((set_value<20)&(set_value>0)):
            print("Warning, halogen light lifetime may be decreasing fast")
