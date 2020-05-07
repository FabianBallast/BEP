# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets

class help_layout(QtWidgets.QWidget):

    def __init__(self, parent):
        super().__init__()
    
        self.create_text(parent.width(), parent.height())
        self.create_tuner(parent.width(), parent.height())
        #self.create_button()
    
    def create_text(self, width, height):
        font = QtGui.QFont()
        font.setPixelSize(int(height * 0.05))
        self.help_label = QtWidgets.QLabel(self)
        self.help_label.setText("Wees voorzichtig. \n\n\n"
                                "1. Alleen bijvullen met gedemineraliseerd water.\n\n"
                                "2. Raak alleen het besturingsscherm aan als de opstelling aan staat.  \n\n"
                                "3. Zorg dat er altijd minstens één iemand aanwezig is om toezicht te houden op de opstelling. \n\n"
                                "4. Rook niet in de buurt van de opstelling. ")
        self.help_label.setFont(font)
        self.help_label.setAlignment(QtCore.Qt.AlignJustify)
        self.help_label.setWordWrap(True)
        self.help_label.setGeometry(QtCore.QRect(int(width * 0.2), int(height * 0.1), int(width * 0.6), int(height * 0.8)))

    def create_tuner(self, width, height):
        font = QtGui.QFont()
        font.setPixelSize(int(height * 0.04))

        self.tuner = QtWidgets.QLineEdit(self)
        self.tuner.setGeometry(QtCore.QRect(int(width * 0.2), int(height * 0.8), int(width * 0.4), int(height * 0.05)))
        self.tuner.setFont(font)
        self.tuner.setValidator(QtGui.QIntValidator(0, 99))
        self.tuner.setText("50")
        self.tuner.setMaxLength(2)
        self.tuner.setStyleSheet("QLineEdit {background-color: rgba(0, 0, 0, 0); color: rgb(255, 255, 255)}")

    def create_button(self):

        help_button_font = QtGui.QFont()
        help_button_font.setFamily("Segoe UI")
        help_button_font.setPointSize(14)
        help_button_font.setBold(True)

        self.continue_button = QtWidgets.QPushButton(self)
        self.continue_button.setText("Continue")
        self.continue_button.setGeometry(QtCore.QRect(425, 450, 150, 50))
        self.continue_button.setFont(help_button_font)
        