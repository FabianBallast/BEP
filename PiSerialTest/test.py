#!/usr/bin/env python3
import serial
import time
import numpy.random as rand

comm_size_to_A = 9
comm_size_to_P = 3

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
   # ser = serial.Serial('COM3', 9600, timeout=0)
    ser.flush()

    while True:
        array_to_send = rand.randint(0,20,comm_size_to_A)
        bytes_to_send = bytes(list(array_to_send))
        
        print('We sent', array_to_send)
        expected_return = [0,0,0]
        expected_return[0] = sum(array_to_send[0:3])
        expected_return[1] = sum(array_to_send[3:6])
        expected_return[2] = sum(array_to_send[6:9])
        
        ser.write(bytes_to_send)
        print('we expect', expected_return)
        
        time.sleep(2)
        
        raw_byte_array = ser.read(comm_size_to_P) #.decode('utf-8').rstrip()
        comm_array = [x for x in raw_byte_array]
        print(comm_array)
        