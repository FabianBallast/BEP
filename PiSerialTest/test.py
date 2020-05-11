#!/usr/bin/env python3
import serial
import time
import numpy.random as rand
#import Loads


class SerialCommunicator:

    
    def __init__(self):
        self.ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=0)
        #self.ser = serial.Serial('COM4', 9600, timeout=0

        #initial parameters
        self.send = {'windPower':0,
                 'stest0':0,
                  'stest1':0}
        #comm protocol
        self.sendOrder = ['windPower','stest0', 'stest1']
        self.receiveOrder = ['start','currentWindPower','rtest0', 'end']
        self.end_char_RP = 254
        self.start_char_RP = 255
        print('comm_size_to_Arduino', len(self.send))
        print('comm_size_to_Pi', len(self.receiveOrder))
        print('start char to Pi', self.start_char_RP)
        print('end char to Pi', self.end_char_RP)
        self.ser.flush()
    
    def sendToArduino(self, **kwargs):
        for key, value in kwargs.items():
            self.send[key] = value
        print('Sending',self.send)
        
        array_to_send = [int(self.send[key]) for key in self.sendOrder]
        bytes_to_send = bytes(array_to_send)
        
        print('We sent', array_to_send)
        self.ser.write(bytes_to_send)
        return self.send

    def readArduino(self):
        bytes_awaiting = self.ser.in_waiting
        
        if (bytes_awaiting<len(self.receiveOrder)):
            print("Nothing to receive yet")     
        else:
            raw_byte_array = self.ser.read(bytes_awaiting) #.decode('utf-8').rstrip()
            comm_array = [x for x in raw_byte_array]
            
            if self.end_char_RP not in comm_array:
                print("Received ",bytes_awaiting, " bytes incorrectly: ", comm_array)
            else:
                last_occurence_of_end_char = len(comm_array)- comm_array[::-1].index(self.end_char_RP)
                comm_array = comm_array[last_occurence_of_end_char-len(self.receiveOrder):last_occurence_of_end_char]
                if not comm_array[0] == self.start_char_RP:
                    print("Received ",bytes_awaiting, " bytes incorrectly: ", comm_array)
                else:
                    print("Correctly received: ",comm_array, " out of ", bytes_awaiting, ' bytes')
                    data = dict(zip(self.receiveOrder, comm_array))
                    print(data)
                    return data
                    


if __name__ == '__main__':
    comm = SerialCommunicator()
    windPower_desired = int(input('Fan power?'))
    comm.sendToArduino(windPower = windPower_desired)
    
    while True:
        comm.readArduino()
        time.sleep(2)
        
   


