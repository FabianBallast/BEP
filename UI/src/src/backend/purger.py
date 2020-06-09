"""This class handles the sensor for reading the tank level."""

import time
from PyQt5 import QtCore
try:
    import board
except NotImplementedError:
    from ..dummy import dummy_board as board                            #pylint: disable=relative-beyond-top-level

try:
    import RPi.GPIO as IO
except ModuleNotFoundError:
    print("using dummy gpio")
    from ..dummy import dummy_io as IO                      #pylint: disable=relative-beyond-top-level



VALVE_PIN = 25

class ValvePurger:


    """This class represents the sensor."""
    def __init__(self, printer):
        self.current_wind_voltage = 0
        
        IO.setmode(IO.BCM)
        IO.setup(VALVE_PIN, IO.OUT)
        IO.output(VALVE_PIN,0)
        self.lastOpen = time.time()
        self.printer = printer

    def timeValve(self, periodMillis, timeOpenMillis):
        if time.time() - self.lastOpen > periodMillis/1000:
            self.openValve(timeOpenMillis)
            
    
    def openValve(self, timeOpenMillis):
        IO.output(VALVE_PIN, 1)
        self.printer.print("Valve opened")
        self.lastOpen = time.time()
        self.close_timer = QtCore.QTimer()
        self.close_timer.timeout.connect(self.closeValve)
        self.close_timer.start(timeOpenMillis)
    
    def closeValve(self):
        IO.output(VALVE_PIN, 0)
        self.printer.print("Valve closed")
        self.close_timer.stop()


if __name__ == "__main__":
    purge = ValvePurger()
    purge.openValve(100)