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
        #
        if ((set_value<20)&(set_value>0)):
            print("Warning, halogen light lifetime may be decreasing fast")

    def adjust(self, set_value):
        self.pwm.ChangeDutyCycle(set_value)

    def animate(self, end_value, step_size=10):
        if set_value>self.end_value:
            intermediate_value = self.start_value+step_size
            if intermediate_value>self.end_value:
                intermediate_value = self.end_value
            self.adjust(intermediate_value)
        else:
            adjust()