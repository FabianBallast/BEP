"""This module handler the halogen lamp."""
#import board
#import RPi.GPIO as IO

class HalogenLight:
    """This class represents the halogen lamp."""
    def __init__(self):
        """Wrapper for dimmable halogenlight with slow start."""
        HALOGEN_MOSFET_PIN = 18                             #pylint: disable=C0103
        self.start_value = 0
        # IO.setmode(IO.BCM)
        # IO.setup(HALOGEN_MOSFET_PIN, IO.OUT)

        # self.pwm = IO.PWM(led, 100)
        # self.pwm.start(0)
    
    def set_light(self, set_value):
        """Input value between 0-100."""
        #self.pwm.ChangeDutyCycle(set_value)
        if 0 < set_value < 20:
            print("Warning, halogen light lifetime may be decreasing fast")
