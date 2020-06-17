"""This module deals with the serial page of the UI."""

from PyQt5 import QtCore, QtWidgets, QtGui
import json

class SerialPage(QtWidgets.QWidget):
    """This class inherits from a QWidget.
       It contains all components on the 'serial' page."""

    def __init__(self, parent, text_box, last_data_box):
        super().__init__(parent)
        self.text_browser = text_box
        self.text_browser.setGeometry(QtCore.QRect(int(parent.width() * 0.05), int(parent.height() * 0.05),
                                                   int(parent.width() * 0.50), int(parent.height() * 0.90)))
        self.text_browser.setParent(self)
        
        self.last_data_box = last_data_box
        self.last_data_box.setGeometry(QtCore.QRect(int(parent.width() * 0.50), int(parent.height() * -0.05),
                                                   int(parent.width() * 0.90), int(parent.height() * 1.05)))
        self.last_data_box.setParent(self)
        #self.last_data_box.setAlignment(QtCore.Qt.AlignTop|QtCore.Qt.AlignRight)
        

        font = QtGui.QFont()
        font.setPixelSize(int(parent.height() * 0.025))
        self.text_browser.setFont(font)
        self.last_data_box.setFont(font)
        self.last_data_box.setText("Last data: ")
        self.last_data_box.setWordWrap(True)
        self.parent = parent
        

    #def print(self, text):
    #    """Print the text to the screen."""
    #    self.text_browser.append(text)

class LastDataBox(QtWidgets.QLabel):
    """This class inherits from a QLabel.
    It contains a text box."""

    def update(self, data):
        if self.parent().parent.currentWidget() == self.parent():
            self.setText(str(json.dumps(data, indent=2)))
class SerialTextBox(QtWidgets.QTextBrowser):
    """This class inherits from a QTextBrowser.
       It contains the text box."""
    
    def print(self, text):
        """Print the text to the screen."""
        self.append(text) 

class SerialRaw():
    """Class for when there is no second screen and still print stuff."""
    def __init__(self):
        pass
    def print(self, *stuff):
        """Print stuff to the terminal."""
        print(*stuff)

