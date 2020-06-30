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
        self.printer = printer
        self.NO_CONNECTION = ""

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
                windY = 2,
                H2ref = 2,
                fan = 2)
        
        self.attachSerial()
        #initial parameters
        self.send = {'windPower' : 0,
                     'h2' : 0,
                     'windMosfet': 0}
        #comm protocol
        self.send_order = ['windPower', 'h2', 'windMosfet']
        
        if not printer:
                print("Gebruikt terminal log" )
                self.printer = rawPrinter()
        self.printer.print(f'comm_size_to_Arduino: {len(self.send)}')
        self.printer.print("Printing all messages from arduino in log")
        self.ser.flush()
           
        self.all_received_data = ""
        self.last_connect_event = time.time() + 3
    
    def attachSerial(self):
        try:
            self.ser = serial.Serial('/dev/ttyACM0', 9600, timeout=0, write_timeout=0.5, inter_byte_timeout=1)
            #self.ser.open()
            #self.ser = serial.Serial('/dev/ttyACM0', 9600, timeout=0, write_timeout=0.5, inter_byte_timeout=1)
            self.printer.print("Arduino verbonden")
        except serial.serialutil.SerialException:
            self.printer.print("Fout met verbinden met Arduino")
            from ..dummy import dummy_serial
            self.ser = dummy_serial
            self.last_data['dummy_serial'] = 0
            self.NO_CONNECTION = "Arduino niet gevonden"

    def send_to_arduino(self, **kwargs):
        """Send data to Arduino. Currently only windpower."""
        if not (self.NO_CONNECTION):
            for key, value in kwargs.items():
                self.send[key] = value
            #printer.print('Sending', self.send)
            
            array_to_send = [int(self.send[key]) for key in self.send_order]
           # array_to_send[1] = 0
            bytes_to_send = bytes(array_to_send)
            
            self.printer.print(f'Pi to Arduino: {array_to_send}')
            try:
                self.ser.write(bytes_to_send)
            except Exception as error:
                self.printer.print("Arduino crashed")
                self.NO_CONNECTION = "Verbinding verloren"

        return self.send

    def read_arduino(self):
        """Receive data from the Arduino."""
        if self.ser.in_waiting == 0:
            if time.time() - self.last_connect_event > 3:
                #3 sec fallout, needs a reset
                #self.ser.reset_input_buffer()
                #self.ser.reset_output_buffer()
                self.printer.print(f'Retrying to connect with Arduino...')
                self.ser.close()
                self.ser.__del__()
                self.attachSerial()
                #self.ser.open() 
                self.last_connect_event = time.time()
                
#        self.printer.print(f'reading?...')
        if self.ser.in_waiting > 1000:
            self.ser.flush()
            self.printer.print(f'Serial flushed, {self.ser.in_waiting} in waiting')

        try:
            if self.ser.in_waiting>0:
                rbytes = self.ser.read(self.ser.in_waiting)

                if rbytes:
                    self.NO_CONNECTION = ""
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
                        self.last_connect_event = time.time()

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
