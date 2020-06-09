"""This module handler the halogen lamp."""
import time
from PyQt5 import QtCore
try:
    import RPi.GPIO as IO
except ModuleNotFoundError:
    print("using dummy gpio")
    from ..dummy import dummy_io as IO                      #pylint: disable=relative-beyond-top-level


class HalogenLight:
    """This class represents the halogen lamp."""
    def __init__(self, printer, start_value=0):
        """Wrapper for dimmable halogenlight with slow start."""
        HALOGEN_MOSFET_PIN = 23                             #pylint: disable=invalid-name
        IO.setmode(IO.BCM)
        IO.setup(HALOGEN_MOSFET_PIN, IO.OUT)
        self.pwm = IO.PWM(HALOGEN_MOSFET_PIN, 100)
        self.pwm.start(start_value)
        self.intermediate_value = start_value
        self.printer = printer
        self.end_value = start_value
    
    def set_light(self, set_value):
        """Input value between 0-100."""
        #self.adjust(set_value)########
        
        self.end_value = set_value
        #self.printer.print("End goal light: ", set_value,  ' intermediate' , self.intermediate_value)
        # self.adjust(set_value)
        if set_value > self.intermediate_value:
            self.animate_timer = QtCore.QTimer()
            self.animate_timer.timeout.connect(self.animate)
            self.animate_timer.start(40)
        elif set_value < self.intermediate_value:
            self.adjust(set_value)
            
        # if 0 < set_value < 20:
        #     self.printer.print("Warning, halogen light lifetime may be decreasing fast")

    def adjust(self, set_value):
        """Adjust value of lamp on a range from 0 to 100."""
        if set_value > 99: 
            set_value = 100
        elif set_value < 1: 
            set_value = 0
        self.pwm.ChangeDutyCycle(set_value)
        self.intermediate_value = set_value
        self.printer.print(f'light: {set_value}')

    def animate(self, step_size=2):
        """Slow start the lamp."""
        new_value = self.intermediate_value+step_size
        self.adjust(new_value)
        
        if new_value >= self.end_value:
            self.animate_timer.stop()
            #self.adjust(intermediate_value)
        else:
            pass
            
            
if __name__ == '__main__':
    class SerialRaw():
        """Class for when there is no second screen and still print stuff."""
        def __init__(self):
            pass
        def print(self, *stuff):
            """Print stuff to the terminal."""
            print(*stuff)
    light = HalogenLight(SerialRaw(), 50)
    light.set_light(30)
    time.sleep(2)
