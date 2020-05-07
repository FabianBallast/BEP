# -*- coding: utf-8 -*-

import sys
sys.path.insert(1, '../libs')

from PyQt5 import QtCore, QtGui, QtWidgets
from pyqt_led import Led

class map_layout(QtWidgets.QWidget):

    def __init__(self, MainWindow, parent):
        super().__init__(parent)
        self.MainWindow = MainWindow

        self.color_on = 'green'
        self.color_off = 'black'
        self.shape = 'circle'

        width = parent.width()
        height = parent.height()

        self.x_pos = [int(width * x) for x in [.340, .515, .685, .090, .890, .090, .528, .718, .925]]
        self.y_pos = [int(height * y) for y in [0.06, 0.06, 0.06, 0.26, 0.32, 0.62, 0.765, 0.78, 0.78]]
        self.diameter = int(width * 0.03)

        self.value_progress_bar = 50

        self.create_leds()
        self.create_progress_bar(self.value_progress_bar, width, height)
        self.create_background(width, height) 
    
    def create_leds(self):

        for i in range(len(self.x_pos)):
            exec(f"self.LED_{i+1} = Led(parent=self, on_color=Led.{self.color_on}, off_color=Led.{self.color_off}, shape=Led.{self.shape}, build='debug', ind={i})")
            exec(f"self.LED_{i+1}.setGeometry(QtCore.QRect({self.x_pos[i]}, {self.y_pos[i]}, {self.diameter}, {self.diameter}))")
            exec(f"self.LED_{i+1}.setCheckable(False)")
    
    def create_progress_bar(self, default_value, width, height):
        self.storage_bar = QtWidgets.QProgressBar(self)
        self.storage_bar.setGeometry(QtCore.QRect(int(width * 0.31), int(height * 0.5), int(width * 0.021), int(height * 0.25)))
        self.storage_bar.setProperty("value", default_value)
        self.storage_bar.setOrientation(QtCore.Qt.Vertical)

    def create_background(self, width, height):

        self.map_picture = QtWidgets.QLabel(self)
        self.map_picture.setGeometry(QtCore.QRect(0, 0, width, height))
        self.map_picture.setPixmap(QtGui.QPixmap("../img/bg_1.jpg"))
        self.map_picture.setScaledContents(True)
        self.map_picture.lower()

    def get_current_values(self, solar, wind, demand):

        self.update_progress_bar(solar + wind - demand)
        self.update_background(solar, demand)
        self.update_leds(solar, wind, demand, solar + wind - demand)
        
    def button_press(self):
        
        led_ind = self.MainWindow.sender().ind + 2 if self.MainWindow.sender().ind < len(self.x_pos) - 1 else 1
        exec(f"self.LED_{led_ind}.set_status(True)")
    
    def update_progress_bar(self, val):
        val = val / 10
        self.value_progress_bar = max(min(self.value_progress_bar + val, 100), 0) 
        self.storage_bar.setProperty('value', int(self.value_progress_bar))
        self.storage_bar.update()
    
    def update_background(self, solar_power, power_demand):
        solar_power = round(solar_power, 0)
        power_demand = round(power_demand, 0) if self.value_progress_bar > 0 else 0

        val = int(6 + min(power_demand, 4) if solar_power > 2 else 1 + min(power_demand, 4)) 
        self.map_picture.setPixmap(QtGui.QPixmap(f"../img/bg_{str(val)}.jpg"))
    
    def update_leds(self, solar, wind, demand, diff):
        
        led_list = []
        solar = round(solar, 0)
        demand = round(demand, 0)

        if diff > 0 and self.value_progress_bar < 100:
            led_list.append(1)
        elif diff < 0 and self.value_progress_bar > 0:
            led_list.append(7)
        
        if solar > 2:
            led_list.append(8)
            led_list.append(9)
        
        if wind > 1.5:
            led_list.append(4)
            led_list.append(6)
        
        if demand > 4 and self.value_progress_bar > 0:
            led_list.append(2)
            led_list.append(3)
            led_list.append(5)
        elif demand > 3 and self.value_progress_bar > 0:
            led_list.append(3)
            led_list.append(5)
        elif demand >= 1 and self.value_progress_bar > 0:
            led_list.append(5)
        
        for Led in range(1, len(self.x_pos) + 1):
            if Led in led_list:
                exec(f"self.LED_{Led}.set_status(True)") 
            else:
                 exec(f"self.LED_{Led}.set_status(False)") 
        


    
