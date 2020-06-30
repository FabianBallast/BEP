"""This module contains the main component for the map-page.
   All components for this page are placed on this widget."""
import os
import pathlib
import math
from PyQt5 import QtWidgets, QtCore, QtGui
from pyqt_led import Led                                        #pylint: disable=W0611

class MapLayout(QtWidgets.QWidget):
    """This class inherits from a QWidget.
       It contains all components on the 'map' page."""
    def __init__(self, MainWindow, parent):
        super().__init__(parent)
        self.main_window = MainWindow

        self.color_on = 'green'
        self.color_off = 'black'
        self.shape = 'circle'

        self.base_path = os.path.join(pathlib.Path(__file__).parent.absolute(), '../../img/')

        width = parent.width()
        height = parent.height()
        
        self.x_pos = [int(width * x) for x in [.34, .515, .685, .09, .89, 
                                               .528, .718]]
        self.y_pos = [int(height * y) for y in [0.06, 0.060, 0.06, 0.26, 0.32, 
                                                0.765, 0.78]]
        self.diameter = int(width * 0.03)
        self.value_progress_bar = 50

        self.create_leds()
        self.create_progress_bar(self.value_progress_bar, width, height)
        self.create_background(width, height)

    def create_leds(self):
        """Create all the LED's and place them in the correct spot."""
        for i in range(len(self.x_pos)):
            exec(f"self.LED_{i+1} = Led(parent=self," 
                                  f"on_color=Led.{self.color_on}," 
                                  f"off_color=Led.{self.color_off},"
                                  f"shape=Led.{self.shape}," 
                                  f"build='debug'," 
                                  f"ind={i})")
            exec(f"self.LED_{i+1}.setGeometry(QtCore.QRect({self.x_pos[i]}, {self.y_pos[i]}," 
                                                         f"{self.diameter}, {self.diameter}))")
            exec(f"self.LED_{i+1}.setCheckable(False)")
            
    def create_progress_bar(self, default_value, width, height):
        """Create the progress bar to visualize the amount of hydrogen stored."""
      #  self.storage_bar = QtWidgets.QProgressBar(self)
        # self.storage_bar.setGeometry(QtCore.QRect(int(width * 0.310), int(height * 0.5), 
        #                                           int(width * 0.021), int(height * 0.25)))
        # self.storage_bar.setProperty("value", default_value)
        # self.storage_bar.setOrientation(QtCore.Qt.Vertical)
        self.text_font = QtGui.QFont()
        self.text_font.setPixelSize(int(height * 0.05))

        self.storage_level = QtWidgets.QLabel(self)
        self.storage_level.setFont(self.text_font)
        self.storage_level.setText("0 mL")
        self.storage_level.setGeometry(QtCore.QRect(int(width * 0.390), int(height * 0.5), 
                                                  int(width * 0.1), int(height * 0.25)))
       # self.hydrogen_text.setAlignment(QtCore.Qt.AlignTop|QtCore.Qt.AlignLeft)

       # self.storage_bar.setDisabled(True)
        #self.storage_bar.setAutoFillBackground(True)
      #  self.storage_bar.setStyleSheet(" ")

    def create_background(self, width, height):
        """Create a label to display a background image."""
    
        self.map_picture = QtWidgets.QLabel(self)
        self.map_picture.setGeometry(QtCore.QRect(0, 0, width, height))
        self.map_picture.setPixmap(QtGui.QPixmap(self.base_path + 'None.png'))
        self.map_picture.setScaledContents(True)
        self.map_picture.lower()

    def get_current_values(self, values, readings):
        """Update the map to match with the current data.
           Use multiple other functions to accomplish this."""
        solar = values[0][#readings['zonPC']
        wind = values[1]  #readings['windPC'] 
        demand = values[2]  #readings['loadPC']
        h2ref  = readings['H2_PC']
        self.storage_level.setText("{0:.0f} mL".format(readings['tank_level']))
        self.update_background(solar, demand)
        self.update_leds(solar, wind, demand, h2ref)
    
    # def update_progress_bar(self, val):
    #     """Update the progress bar to match with the current data."""
    #     self.storage_bar.setProperty('value', val)
    #     self.storage_bar.update()
    #     self.value_progress_bar = val
    
    def update_background(self, solar_power, power_demand):
        """Update the background to match with the current data."""
        solar_power = round(solar_power, 0)
        power_demand = round(power_demand, 0) if self.value_progress_bar > 0 else 0

        val = "SL" + str(min(math.floor(power_demand / 25), 3)) if solar_power > 50 else "L" + str(min(math.floor(power_demand / 25), 3)) #pylint: disable=line-too-long
        
        
        self.map_picture.setPixmap(QtGui.QPixmap(self.base_path + f"{val}.png"))
    
    def update_leds(self, solar, wind, demand, diff):
        """Update the LED's to match with the current data."""
        led_list = []
        solar = round(solar, 0)
        demand = round(demand, 0)

        if diff > 0 and self.value_progress_bar < 100:
            led_list.append(1)
        elif diff < 0 and self.value_progress_bar > 0:
            led_list.append(6)
        
        if solar > 50:
            led_list.append(7)
        
        if wind > 50:
            led_list.append(4)
        
        if demand > 75 and self.value_progress_bar > 0:
            led_list.append(2)
            led_list.append(3)
            led_list.append(5)
        elif demand > 50 and self.value_progress_bar > 0:
            led_list.append(2)
            led_list.append(5)
        elif demand >= 25 and self.value_progress_bar > 0:
            led_list.append(2)
        
        for led in range(1, len(self.x_pos) + 1):
            if led in led_list:
                exec(f"self.LED_{led}.set_status(True)")
            else:
                exec(f"self.LED_{led}.set_status(False)")
        


    
