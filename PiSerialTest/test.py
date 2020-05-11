#!/usr/bin/env python3
import serial
import time
import numpy.random as rand
#import Loads

comm_size_to_A = 9
comm_size_to_P = 3

if __name__ == '__main__':
   # ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    ser = serial.Serial('COM4', 9600, timeout=0)
    ser.flush()

    while True:
        for i in range(100):
            if i % 4 ==0:
                Loads.load_set(i)
                print("Load goal:", i)
            if i % 10 ==0:
                array_to_send = [0]*comm_size_to_A
                array_to_send[0] = i
                bytes_to_send = bytes(list(array_to_send))
                print('We sent', array_to_send)
                print('Fan goal: ', i)
                ser.write(bytes_to_send)

            if True: #always read
                raw_byte_array = ser.read(comm_size_to_P) #.decode('utf-8').rstrip()
                comm_array = [x for x in raw_byte_array]
                print("Received", comm_array)
            time.sleep(0.2) 
        
   


