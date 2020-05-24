"""This module handles the Serial connection between the Pi and Arduino (from the PI-side)."""

import time
import serial

#import numpy.random as rand
#import loads


class SerialCommunicator:
    """This class represent the communication with the Arduino."""
    
    def __init__(self, printer):
        try:
            #self.ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=0)
            self.ser = serial.Serial('COM5', 9600, timeout=0)
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
        self.printer.print(f'comm_size_to_Arduino: {len(self.send)}')
        self.printer.print("Printing all messages from arduino in log")
        self.ser.flush()
        self.last_data = dict()
    
    def send_to_arduino(self, **kwargs):
        """Send data to Arduino. Currently only windpower."""
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
        bytes_awaiting = self.ser.in_waiting
        if bytes_awaiting>0:
            received_from_arduino = self.ser.read(bytes_awaiting).decode('utf-8').rstrip()
            self.printer.print(f'Received from Arduino: {received_from_arduino}')
            try:
                data_part = received_from_arduino.split("newdata=")[-1].split("}enddata")[0]
                return eval(data_part)
            except:
                self.printer.print("No data found in data received from Arduino")

        return self.last_data            


if __name__ == '__main__':
    comm = SerialCommunicator(None)
    windPower_desired = int(input('Fan power?'))
    comm.send_to_arduino(windPower=windPower_desired)
    
    while True:
        comm.read_arduino()
        time.sleep(2)
