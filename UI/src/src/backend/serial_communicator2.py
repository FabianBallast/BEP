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
            self.ser = serial.Serial('/dev/ttyACM1', 9600, timeout=0)
            #self.ser = serial.Serial('COM5', 9600, timeout=0)
            self.CONNECTION = True
        except serial.serialutil.SerialException:
            from ..dummy import dummy_serial
            self.ser = dummy_serial
            self.CONNECTION = False
        #self.ser = serial.Serial('COM4', 9600, timeout=0

        #initial parameters
        self.send = {'windPower' : 0,
                     'stest0' : 0,
                     'stest1' : 0}
        #comm protocol
        self.send_order = ['windPower', 'stest0', 'stest1']
        self.printer = printer
        if not printer:
                print("Gebruikt terminal log" )
                self.printer = rawPrinter()
        self.printer.print(f'comm_size_to_Arduino: {len(self.send)}')
        self.printer.print("Printing all messages from arduino in log")
        self.ser.flush()
        self.last_data = dict(solar_current = 2, 
                wind_current = 2, 
                load_current = 2,
                elektrolyzer_current = 2,
                power_supply_current = 2,
                fuel_cell_current = 2,
                dummy_serial = 2)
        self.all_received_data = ""
    
    def send_to_arduino(self, **kwargs):
        """Send data to Arduino. Currently only windpower."""
        if self.CONNECTION:
            for key, value in kwargs.items():
                self.send[key] = value
            #printer.print('Sending', self.send)
            
            array_to_send = [int(self.send[key]) for key in self.send_order]
            bytes_to_send = bytes(array_to_send)
            
            self.printer.print(f'Pi to Arduino: {array_to_send}')
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
                
        
        rbytes = self.ser.read(self.ser.in_waiting)
        try:
            if rbytes:
                self.CONNECTION = True
                received_from_arduino = rbytes.decode('utf-8').rstrip()
                self.all_received_data = self.all_received_data + received_from_arduino

                #self.printer.print(f'Received from Arduino: {received_from_arduino}')
                
                if "newdata=" in self.all_received_data.rsplit('enddata', 1)[0]:   #check if newdata occurs before enddata
                    end_splits = self.all_received_data.split('enddata')[:-1]
                    if len(end_splits) > 0:
                        for split in end_splits:
                            if "newdata=" in split:
                                start_splits = split.split("newdata=")
                                if len(start_splits[0]) > 0:
                                    self.printer.print(f'Received from Arduino {start_splits[0]}')
                                self.last_data = eval(start_splits[1])
                                #self.printer.print('Data updated from Arduino')
                            elif "}" not in split:
                                self.printer.print(f'Received from Arduino: {split}')
                    self.all_received_data = ""

        except AttributeError as error:
            rbytes = str(rbytes)
            self.all_received_data = ""
            self.printer.print(f"Attribute error reading data from arduino: {error}, bytes: {rbytes}")
            self.CONNECTION = False
            self.ser.reset_input_buffer()
            self.ser.reset_output_buffer()    
        
        print(isinstance(self.last_data, dict))
        return self.last_data            


if __name__ == '__main__':
    comm = SerialCommunicator(rawPrinter())
    windPower_desired = 10
    #windPower_desired = int(input('Fan power?'))
    comm.send_to_arduino(windPower=windPower_desired)
    
    while True:
        print(comm.read_arduino())
        time.sleep(2)