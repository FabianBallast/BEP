"""This module handles the Serial connection between the Pi and Arduino (from the PI-side)."""

import time
import serial
import re

#import numpy.random as rand
#import loads

class rawPrinter:
    def __init__(self):
        pass
    def print(self,*stuff):
        print(*stuff)

class SerialCommunicator:
    """This class represent the communication with the Arduino."""
    
    def __init__(self, printer):
        try:
            self.ser = serial.Serial('/dev/ttyACM0', 9600, timeout=0)
            #self.ser = serial.Serial('COM5', 9600, timeout=0)
            self.NO_CONNECTION = ""
            printer.print("Arduino verbonden")
        except serial.serialutil.SerialException:
            from ..dummy import dummy_serial
            self.ser = dummy_serial
            self.NO_CONNECTION = "Arduino niet verbonden"
        #self.ser = serial.Serial('COM4', 9600, timeout=0

        #initial parameters
        self.send = {'windPower' : 0,
                     'zonPower' : 0,
                     'windMosfet': 0}
        #comm protocol
        self.send_order = ['windPower', 'zonPower', 'windMosfet']
        self.printer = printer
        if not printer:
                print("Gebruikt terminal log" )
                self.printer = rawPrinter()
        self.printer.print(f'comm_size_to_Arduino: {len(self.send)}')
        self.printer.print("Printing all messages from arduino in log")
        self.ser.flush()
        self.last_data = dict(zonU = 2, 
                loadI = 2, 
                windU = 2,
                FC_U = 2,
                FC_Y = 2,
                flowTot = 10,
                EL_U = 2,
                EL_I = 7,
                EL_Y = 2,
                gridU = 2,
                gridX = 2,
                loopT = 2,
                PS_I = 2,
                fan = 2)
           
        self.all_received_data = ""
    
    def send_to_arduino(self, **kwargs):
        """Send data to Arduino. Currently only windpower."""
        if not (self.NO_CONNECTION == "Arduino niet verbonden"):
            for key, value in kwargs.items():
                self.send[key] = value
            #printer.print('Sending', self.send)
            
            array_to_send = [int(self.send[key]) for key in self.send_order]
            bytes_to_send = bytes(array_to_send)
            
            #self.printer.print(f'Pi to Arduino: {array_to_send}')
            self.ser.write(bytes_to_send)
        return self.send

    def read_arduino(self):
        """Receive data from the Arduino."""
        if self.ser.in_waiting ==0:
                if self.all_received_data == "":
                    #needs a reset
                    self.ser.reset_input_buffer()
                    self.ser.reset_output_buffer()
                    self.printer.print(f'Waiting for Arduino to send...')
                    #self.ser.close()
                    #time.sleep(1)
                    #self.ser.open() 
                self.all_received_data = ""
                
#        self.printer.print(f'reading?...')
        rbytes = self.ser.read(self.ser.in_waiting)
        try:
            if rbytes:
                self.NO_CONNECTION = False
                received_from_arduino = rbytes.decode('utf-8').rstrip()
                self.all_received_data = self.all_received_data + received_from_arduino

                #self.printer.print(f'Received from Arduino: {received_from_arduino}')
                
                if "nd=" in self.all_received_data.rsplit('ed', 1)[0]:   #check if newdata occurs before enddata
                    end_splits = self.all_received_data.split('ed')[:-1]
                    if len(end_splits) > 0:
                        for split in end_splits:
                            if "nd=" in split:
                                start_splits = split.split("nd=")
                                if len(start_splits[0]) > 0:
                                    self.printer.print(f'Received from Arduino {start_splits[0]}')
                                self.last_data = eval(start_splits[1])
                                #self.printer.print('Data updated from Arduino')
                            elif "}" not in split:
                                self.printer.print(f'Received from Arduino: {split}')
                    self.all_received_data = ""

        except Exception as error:
            rbytes = str(rbytes)
            self.all_received_data = ""
            if type(self.ser) == serial.Serial: 
                self.printer.print(f"Attribute error reading data from arduino: {error}, bytes: {rbytes}")
            self.NO_CONNECTION = "Arduino niet verbonden"
            self.ser.reset_input_buffer()
            self.ser.reset_output_buffer()    
        
        return self.last_data            


if __name__ == '__main__':
    comm = SerialCommunicator(rawPrinter())
    windPower_desired = 10
    #windPower_desired = int(input('Fan power?'))
    comm.send_to_arduino(windPower=windPower_desired)
    
    while True:
        print(comm.read_arduino())
        time.sleep(2)
