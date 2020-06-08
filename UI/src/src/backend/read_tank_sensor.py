"""This class handles the sensor for reading the tank level."""
try:
    import board
except NotImplementedError:
    from ..dummy import dummy_board as board                            #pylint: disable=relative-beyond-top-level

import busio
import adafruit_vl6180x
#import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from ..dummy import dummy_range_sensor as sensor                        #pylint: disable=relative-beyond-top-level

class TankReader:
    """This class represents the sensor."""
    def __init__(self, NO_CONNECTION, N_FILTER=30):

        try:
            i2c = busio.I2C(board.SCL, board.SDA)
            self.sensor = adafruit_vl6180x.VL6180X(i2c)
            NO_CONNECTION += "Tank sensor niet verbonden"
        except ValueError:
            self.sensor = sensor
        except ModuleNotFoundError:
            self.sensor = sensor  
        
        #Main loop print
        self.N_FILTER = N_FILTER                                    #pylint: disable=invalid-name

        self.raw_data_queue = [self.sensor.range] * self.N_FILTER

        D_TANK = 0.0335                                             #pylint: disable=invalid-name
        self.A_TANK = (3.1416*(D_TANK/2)**2)*1e3                    #pylint: disable=invalid-name
        self.V0 = 110                                               #pylint: disable=invalid-name
        
        self.corr = 0
    
    def set_calibrate(self, volume):
        """Calibrate sensor with actual value."""
        current_reading = self.read_range()
        self.corr = volume - (self.V0- current_reading * self.A_TANK)
    
    def read_range(self):
        """Return the range from the sensor."""
        range_mm = self.sensor.range
        self.raw_data_queue.append(range_mm)
        self.raw_data_queue.pop(0)
        avg = sum(self.raw_data_queue)/self.N_FILTER
        return avg
    
    def read_tank_level(self):
        """Return the volume in the tank."""
        current_reading = self.read_range() 
        volume = (self.V0- current_reading * self.A_TANK) + self.corr
        return volume

def plot_tank_level(i):                         #pylint: disable=unused-argument
    """Plot the level in the tank over time."""
    volume_data.append(h2_tank.read_tank_level())
    ax1.clear()
    
    plt.ylim(0, 80)
    ax1.plot(volume_data)

if __name__ == '__main__':
    h2_tank = TankReader()
    
    volume_data = []
    
    #animate    
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)

    ani = FuncAnimation(fig, plot_tank_level, interval=40)
    plt.show()
