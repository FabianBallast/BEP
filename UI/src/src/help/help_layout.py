"""This module covers all help/safety information for the user."""
from PyQt5 import QtCore, QtGui, QtWidgets

class HelpLayout(QtWidgets.QWidget):
    """This class inherits from a QWidget.
       It contains all components on the 'help' page."""
    def __init__(self, data_manager, parent):
        super().__init__()
        self.data_manager = data_manager    
        self.create_text(parent.width(), parent.height())
        self.create_tuner(parent.width(), parent.height())
        self.create_button(parent.width(), parent.height())
        self.create_calibration_text(parent.width(), parent.height())
    
    def create_text(self, width, height):
        """Creates the main info text with safety precautions."""
        font = QtGui.QFont()
        font.setPixelSize(int(height * 0.045))
        self.help_label = QtWidgets.QLabel(self)
        self.help_label.setText("Wees voorzichtig. \n\n\n"
                                "1. Alleen bijvullen met gedemineraliseerd water.\n\n"
                                "2. Raak alleen het besturingsscherm aan " 
                                   "als de opstelling aan staat.\n\n"
                                "3. Zorg dat er altijd minstens één iemand aanwezig is " 
                                   "om toezicht te houden op de opstelling. \n\n"
                                "4. Rook niet in de buurt van de opstelling. ")
        self.help_label.setFont(font)
        self.help_label.setAlignment(QtCore.Qt.AlignJustify)
        self.help_label.setWordWrap(True)
        self.help_label.setGeometry(QtCore.QRect(int(width * 0.2), int(height * 0.05), 
                                                 int(width * 0.6), int(height * 0.8)))


    def create_tuner(self, width, height):
        """Creates the LineEdit to enter the current volume of hydrogen stored."""
        font = QtGui.QFont()
        font.setPixelSize(int(height * 0.04))

        self.tuner = QtWidgets.QLineEdit(self)
        self.tuner.setGeometry(QtCore.QRect(int(width * 0.45), int(height * 0.8), 
                                            int(width * 0.025), int(height * 0.05)))
        self.tuner.setFont(font)
        self.tuner.setValidator(QtGui.QIntValidator(0, 99))
        self.tuner.setText("50")
        self.tuner.setMaxLength(2)
    
    def create_calibration_text(self, width, height):
        """Creates a label to clarify how to calibrate and the unit (mL)."""
        font = QtGui.QFont()
        font.setPixelSize(int(height * 0.04))

        self.cal_label = QtWidgets.QLabel(self)
        self.cal_label.setText("Calibration:")
        self.cal_label.setFont(font)
        self.cal_label.setAlignment(QtCore.Qt.AlignRight)
        self.cal_label.setGeometry(QtCore.QRect(int(width * 0.30), int(height * 0.80), 
                                                int(width * 0.15), int(height * 0.05)))

        self.unit_label = QtWidgets.QLabel(self)
        self.unit_label.setText("mL")
        self.unit_label.setFont(font)              
        self.unit_label.setGeometry(QtCore.QRect(int(width * 0.475), int(height * 0.8), 
                                                 int(width * 0.025), int(height * 0.05)))             

    def create_button(self, width, height):
        """Creates a button to confirm the entered value for the tuner."""
        help_button_font = QtGui.QFont()
        help_button_font.setFamily("Segoe UI")
        help_button_font.setPixelSize(int(height * 0.04))
        help_button_font.setBold(True)

        self.calibrate_button = QtWidgets.QPushButton(self)
        self.calibrate_button.setText("Set Value")
        self.calibrate_button.setGeometry(QtCore.QRect(int(width * 0.55), int(height * 0.7875), 
                                                      int(width * 0.15), int(height * 0.075)))
        self.calibrate_button.setFont(help_button_font)
        self.calibrate_button.clicked.connect(self.calibrate)
    
    def calibrate(self):
        """Update the data manager when the button is pressed."""
        self.data_manager.set_storage_value(int(self.tuner.text()))
        