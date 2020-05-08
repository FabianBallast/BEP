
import time
import board
import busio
import adafruit_vl6180x


i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_vl6180x.VL6180X(i2c)

def readTankLevel():
    range_mm = sensor.range
# Main loop prints the range and lux every second:
while True:
    # Read the range in millimeters and print it.
    readTankLevel()

    print("Range: {0}mm".format(range_mm))

    time.sleep(1.0)