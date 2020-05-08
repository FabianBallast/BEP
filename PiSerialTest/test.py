#!/usr/bin/env python3
import serial
import time
import numpy.random as rand
import Loads

comm_size_to_A = 9
comm_size_to_P = 3

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
   # ser = serial.Serial('COM3', 9600, timeout=0)
    ser.flush()

    while True:
        led_power_str = input('Led power?')
        if led_power_str:
            Loads.load_set(int(led_power_str))
         
        fan_power_str = input('Fan power?')
 
        if fan_power_str:
 
            array_to_send = [0]*comm_size_to_A
            array_to_send[0] = int(fan_power_str)
            bytes_to_send = bytes(list(array_to_send))
            
            print('We sent', array_to_send)
        
#        expected_return = [0,0,0]
#        expected_return[0] = fan_power
#        expected_return[1] = 0
#        expected_return[2] = 0
#        
#        ser.write(bytes_to_send)
#        print('we expect', expected_return)
        
        time.sleep(2)
        
        raw_byte_array = ser.read(comm_size_to_P) #.decode('utf-8').rstrip()
        comm_array = [x for x in raw_byte_array]
        print("Received", comm_array)
        