import board
import busio
import adafruit_vl6180x
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class TankReader:
    def __init__(self, N_filter=20):
        i2c = busio.I2C(board.SCL, board.SDA)
        #self.i2c = busio.I2C(board.D3, board.D2)
        self.sensor = adafruit_vl6180x.VL6180X(i2c)
        
        #Main loop print
        self.N_filter = N_filter

        self.raw_data_queue = [self.sensor.range]*self.N_filter
        self.raw_data = []
        self.filtered_data = []
        self.volum_data = []
        
        D_tank = 0.0335
        self.A_tank = (3.1416*(D_tank/2)**2)*1e3
        
        self.corr = 0
    
    def set_calibrate(self, volume):
        current_reading = self.readRange()
        self.corr =  volume - current_reading * self.A_tank
    
    def readRange(self):
        range_mm = self.sensor.range
        self.raw_data.append(range_mm)
        self.raw_data_queue.append(range_mm)
        self.raw_data_queue.pop(0)
        avg = sum(self.raw_data_queue)/self.N_filter
        
        self.filtered_data.append(avg)
        return avg
    
    def readTankLevel(self):
        current_reading = self.readRange()
        volum = current_reading*self.A_tank+self.corr
        self.volum_data.append(volum)
        return volum

def plotTanklevel(i):
    h2_tank.readTankLevel()
    ax1.clear()
    ax1.plot(h2_tank.volum_data)

if __name__ == '__main__':
    h2_tank = TankReader()
        
        
    #animate    
    fig = plt.figure()
    ax1 = fig.add_subplot(1,1,1)
    ani = FuncAnimation(fig, plotTanklevel, interval=40)
    plt.show()

