
import time
import board
import busio
import adafruit_vl6180x
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import style

i2c = busio.I2C(board.SCL, board.SDA)
#i2c = busio.I2C(board.D3, board.D2)
sensor = adafruit_vl6180x.VL6180X(i2c)

N_filter = 20

raw_data_queue = [sensor.range]*N_filter
raw_data = []
filtered_data = []

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

def readTankLevel(i):
    range_mm = sensor.range
    raw_data.append(range_mm)
    raw_data_queue.append(range_mm)
    raw_data_queue.pop(0)
    avg = sum(raw_data_queue)/N_filter
    filtered_data.append(avg)
    ax1.clear()
    ax1.plot(filtered_data)
    ax1.plot(raw_data)
    return avg
# Main loop prints the range and lux every second:
#while True:
    # Read the range in millimeters and print it.
ani = FuncAnimation(fig, readTankLevel, interval=40)
plt.show()
    #range_mm = readTankLevel()
    #ax1.plot(ts, filtered_data)
    #print("Range: {0}mm".format(range_mm))
