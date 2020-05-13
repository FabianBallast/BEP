"""This module deals with the figures page of the UI."""

from PyQt5 import QtCore, QtWidgets, QtGui


class Figures(QtWidgets.QWidget):
    """This class inherits from a QWidget.
       It contains all components on the 'figures' page."""

    def __init__(self, parent):
        super().__init__() 
        self.create_fonts(parent.height())   
        self.create_input_text(parent.width(), parent.height())
        #self.create_output_text(parent.width(), parent.height())
        self.create_system_text(parent.width(), parent.height())

    
    def create_fonts(self, height):
        """Create the fonts used for the figures."""
        self.title_font = QtGui.QFont()
        self.title_font.setPixelSize(int(height * 0.06))

        self.text_font = QtGui.QFont()
        self.text_font.setPixelSize(int(height * 0.05))
    
    def create_input_text(self, width, height):
        """Create the text to show the input power text."""
        self.input_text_title = QtWidgets.QLabel(self)
        self.input_text_title.setFont(self.title_font)
        self.input_text_title.setText("Input\n\n\n\n\n\n\nOutput")
        self.input_text_title.setGeometry(QtCore.QRect(int(width * 0.05), int(height * 0.05),
                                                       int(width * 0.10), int(height * 0.75)))
        self.input_text_title.setAlignment(QtCore.Qt.AlignTop)
                                                       

        self.input_text_left = QtWidgets.QLabel(self)
        self.input_text_left.setGeometry(QtCore.QRect(int(width * 0.15), int(height * 0.15),
                                                      int(width * 0.15), int(height * 0.80)))
        self.input_text_left.setFont(self.text_font)
        self.input_text_left.setText("\n\nZon:\nWind:\n\n\n\n\n\nVerbruik:")
        self.input_text_left.setAlignment(QtCore.Qt.AlignTop)

        self.input_text_right = QtWidgets.QLabel(self)
        self.input_text_right.setGeometry(QtCore.QRect(int(width * 0.30), int(height * 0.15),
                                                       int(width * 0.15), int(height * 0.80)))
        self.input_text_right.setFont(self.text_font)
        self.input_text_right.setText("\n\n0%\n0%\n\n\n\n\n\n0%")
        self.input_text_right.setAlignment(QtCore.Qt.AlignTop)

    def create_output_text(self, width, height):
        """Create the text to display the output power."""
        self.output_text_title = QtWidgets.QLabel(self)
        self.output_text_title.setFont(self.title_font)
        self.output_text_title.setText("Output")
        self.output_text_title.setGeometry(QtCore.QRect(int(width * 0.05), int(height * 0.65),
                                                       int(width * 0.10), int(height * 0.10)))

        self.output_text_left = QtWidgets.QLabel(self)
        self.output_text_left.setGeometry(QtCore.QRect(int(width * 0.20), int(height * 0.75),
                                                      int(width * 0.15), int(height * 0.15)))
        self.output_text_left.setFont(self.text_font)
        self.output_text_left.setText("Verbruik:")

        self.output_text_right = QtWidgets.QLabel(self)
        self.output_text_right.setGeometry(QtCore.QRect(int(width * 0.35), int(height * 0.75),
                                                       int(width * 0.15), int(height * 0.15)))
        self.output_text_right.setFont(self.text_font)
        self.output_text_right.setText("0%")

    def create_system_text(self, width, height):
        """Create the label to display sensor data."""
        self.system_text_title = QtWidgets.QLabel(self)
        self.system_text_title.setFont(self.title_font)
        self.system_text_title.setText("Systeem")
        self.system_text_title.setGeometry(QtCore.QRect(int(width * 0.50), int(height * 0.05),
                                                        int(width * 0.15), int(height * 0.10)))

        self.system_text_left = QtWidgets.QLabel(self)
        self.system_text_left.setGeometry(QtCore.QRect(int(width * 0.50), int(height * 0.15),
                                                       int(width * 0.30), int(height * 0.75)))
        self.system_text_left.setFont(self.text_font)
        self.system_text_left.setText("Opbrengst/vraag:\n\n        Zon:\n        Wind:\n        Huizen/industrie:\n\n\n"
                                      "Waterstof:\n\n        Verbruik/productie:\n        Opslag:")
        self.system_text_left.setAlignment(QtCore.Qt.AlignTop)

        self.system_text_right = QtWidgets.QLabel(self)
        self.system_text_right.setGeometry(QtCore.QRect(int(width * 0.80), int(height * 0.15),
                                                        int(width * 0.10), int(height * 0.75)))
        self.system_text_right.setFont(self.text_font)
        self.system_text_right.setText("\n\n0W\n0W\n0W\n\n\n\n\n\n0W\n50%")
        self.system_text_right.setAlignment(QtCore.Qt.AlignTop)
    
    def update_input(self, input_values):
        """Update the text related to the input/output of the system."""
        self.input_text_right.setText(f"\n\n{input_values[0]}%\n{input_values[1]}%\n\n\n\n\n\n{input_values[2]}%")
    
    def update_system(self, sensor_values):
        """Update the text related to the sensors."""
        self.system_text_right.setText(f"\n\n{round(sensor_values[0] / 20, 1)}W\n"
                                       f"{round(sensor_values[1] / 20, 1)}W\n"
                                       f"{round(sensor_values[2] / 20, 1)}W\n\n\n\n\n"
                                       f"{round((sensor_values[0] + sensor_values[1] - sensor_values[2]) / 20, 1)}W\n"
                                       f"{round(sensor_values[3], 1)}%")
