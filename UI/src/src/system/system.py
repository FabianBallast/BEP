"""This module deals with the figures page of the UI."""

from PyQt5 import QtCore, QtWidgets, QtGui


class System(QtWidgets.QWidget):
    """This class inherits from a QWidget.
       It contains all components on the 'figures' page."""

    def __init__(self, parent):
        super().__init__(parent)
        self.create_fonts(parent.height())   
        self.create_source_text(parent.width(), parent.height())
        self.create_hydrogen_text(parent.width(), parent.height())
        self.create_load_text(parent.width(), parent.height())
    
    def create_fonts(self, height):
        """Create the fonts used for the figures."""
        self.text_font = QtGui.QFont()
        self.text_font.setPixelSize(int(height * 0.05))
    
    def create_source_text(self, width, height):
        """Create the text and values for the sources."""
        self.source_text = QtWidgets.QLabel(self)
        self.source_text.setFont(self.text_font)
        self.source_text.setText("Zon: 0W (0%)\nWind: 0W (0%)")
        self.source_text.setGeometry(QtCore.QRect(int(width * 0.05), int(height * 0.05),
                                                  int(width * 0.10), int(height * 0.10)))
        self.source_text.setAlignment(QtCore.Qt.AlignTop|QtCore.Qt.AlignRight)
    
    def create_hydrogen_text(self, width, height):
        """Create the text for the hydrogen text."""
        self.hydrogen_text = QtWidgets.QLabel(self)
        self.hydrogen_text.setFont(self.text_font)
        self.hydrogen_text.setText("Verbruik/productie: 0W\nOpslag: 50%")
        self.hydrogen_text.setGeometry(QtCore.QRect(int(width * 0.45), int(height * 0.70),
                                                    int(width * 0.10), int(height * 0.10)))
        self.hydrogen_text.setAlignment(QtCore.Qt.AlignTop|QtCore.Qt.AlignRight)
    
    def create_load_text(self, width, height):
        """Create text for the loads"""
        self.load_text = QtWidgets.QLabel(self)
        self.load_text.setFont(self.text_font)
        self.load_text.setText("Huizen: 0W (0%)\nIndustrie: 0W (0%)")
        self.load_text.setGeometry(QtCore.QRect(int(width * 0.85), int(height * 0.05),
                                                int(width * 0.10), int(height * 0.10)))
        self.load_text.setAlignment(QtCore.Qt.AlignTop|QtCore.Qt.AlignRight)
    
    def update_text(self, input_data, sensor_data):
        """Update the text."""
        self.source_text.setText(f"Zon: 0W ({input_data[0]:5.1f}%)\nWind: 0W ({input_data[1]:5.1f}%)")
        self.hydrogen_text.setText(f"Verbruik/productie: 0W\nOpslag: 50%")
        self.load_text.setText(f"Huizen: 0W ({input_data[2]:5.1f}%)\nIndustrie: 0W (0%)")
    
    def update_system(self, sensor_values):
        """Update the text related to the sensors."""
        self.system_text_right.setText(f"\n\n{round(sensor_values[0] / 20, 1)}W\n"
                                       f"{round(sensor_values[1] / 20, 1)}W\n"
                                       f"{round(sensor_values[2] / 20, 1)}W\n\n\n\n\n"
                                       f"{round((sensor_values[0] + sensor_values[1] - sensor_values[2]) / 20, 1)}W\n" #pylint: disable=line-too-long
                                       f"{round(sensor_values[3], 1)}%")
