"""This module handles the Serial connection between the Pi and Arduino (from the PI-side)."""

import time
import serial
#import numpy.random as rand
#import loads


class SerialCommunicator:
    """This class represent the communication with the Arduino."""
    
    def __init__(self):
        self.ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=0)
        #self.ser = serial.Serial('COM4', 9600, timeout=0

        #initial parameters
        self.send = {'windPower' : 0,
                     'stest0' : 0,
                     'stest1' : 0}
        #comm protocol
        self.send_order = ['windPower', 'stest0', 'stest1']
        self.receive_order = ['start', 'wind_power', 'rtest0', 'end']
        self.END_CHAR_RP = 254                                                  #pylint: disable=C0103
        self.START_CHAR_RP = 255                                                #pylint: disable=C0103
        print('comm_size_to_Arduino', len(self.send))
        print('comm_size_to_Pi', len(self.receive_order))
        print('start char to Pi', self.START_CHAR_RP)
        print('end char to Pi', self.END_CHAR_RP)
        self.ser.flush()
        self.last_data = dict()
    
    def send_to_arduino(self, **kwargs):
        """Send data to Arduino. Currently only windpower."""
        for key, value in kwargs.items():
            self.send[key] = value
        print('Sending', self.send)
        
        array_to_send = [int(self.send[key]) for key in self.send_order]
        bytes_to_send = bytes(array_to_send)
        
        print('We sent', array_to_send)
        self.ser.write(bytes_to_send)
        return self.send

    def read_arduino(self):
        """Receive data from the Arduino."""
        bytes_awaiting = self.ser.in_waiting
        
        if bytes_awaiting < len(self.receive_order):
            print("Nothing to receive yet")     
        else:
            raw_byte_array = self.ser.read(bytes_awaiting) #.decode('utf-8').rstrip()
            comm_array = [x for x in raw_byte_array]
            
            if self.END_CHAR_RP not in comm_array:
                print("Received ", bytes_awaiting, " bytes incorrectly: ", comm_array)
            else:
                last_occurence_of_end_char = len(comm_array) - comm_array[::-1].index(self.END_CHAR_RP)                     #pylint: disable=C0301
                comm_array = comm_array[last_occurence_of_end_char - len(self.receive_order):last_occurence_of_end_char]    #pylint: disable=C0301
                if not comm_array[0] == self.START_CHAR_RP:
                    print("Received ", bytes_awaiting, " bytes incorrectly: ", comm_array)
                else:
                    print("Correctly received: ", comm_array, " out of ", bytes_awaiting, ' bytes')
                    data = dict(zip(self.receive_order, comm_array))
                    print(data)
                    self.last_data = data
                    return data
        return self.last_data            


if __name__ == '__main__':
    comm = SerialCommunicator()
    windPower_desired = int(input('Fan power?'))
    comm.send_to_arduino(windPower=windPower_desired)
    
    while True:
        comm.read_arduino()
        time.sleep(2)
