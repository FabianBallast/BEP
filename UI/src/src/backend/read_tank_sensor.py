"""This class handles the sensor for reading the tank level."""
import board
import busio
import adafruit_vl6180x
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class TankReader:
    """This class represents the sensor."""
    def __init__(self, N_FILTER=20):
        i2c = busio.I2C(board.SCL, board.SDA)
        #self.i2c = busio.I2C(board.D3, board.D2)
        self.sensor = adafruit_vl6180x.VL6180X(i2c)
        
        #Main loop print
        self.N_FILTER = N_FILTER                                    #pylint: disable=C0103

        self.raw_data_queue = [self.sensor.range] * self.N_FILTER
        self.raw_data = []
        self.filtered_data = []
        self.volume_data = []
        
        D_TANK = 0.0335                                             #pylint: disable=C0103
        self.A_TANK = (3.1416*(D_TANK/2)**2)*1e3                    #pylint: disable=C0103
        
        self.corr = 0
    
    def set_calibrate(self, volume):
        """Calibrate sensor with actual value."""
        current_reading = self.read_range()
        self.corr = volume - current_reading * self.A_TANK
    
    def read_range(self):
        """Return the range from the sensor."""
        range_mm = self.sensor.range
        self.raw_data.append(range_mm)
        self.raw_data_queue.append(range_mm)
        self.raw_data_queue.pop(0)
        avg = sum(self.raw_data_queue)/self.N_FILTER
        
        self.filtered_data.append(avg)
        return avg
    
    def read_tank_level(self):
        """Return the volume in the tank."""
        current_reading = self.read_range() 
        volume = current_reading * self.A_TANK + self.corr
        self.volume_data.append(volume)
        return volume

def plot_tank_level(i):                         #pylint: disable=unused-argument
    """Plot the level in the tank over time."""
    h2_tank.read_tank_level()
    ax1.clear()
    ax1.plot(h2_tank.volume_data)

if __name__ == '__main__':
    h2_tank = TankReader()
        
        
    #animate    
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)
    ani = FuncAnimation(fig, plot_tank_level, interval=40)
    plt.show()
