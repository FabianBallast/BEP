"""This module deals with the serial page of the UI."""

from PyQt5 import QtCore, QtWidgets, QtGui


class SerialPage(QtWidgets.QWidget):
    """This class inherits from a QWidget.
       It contains all components on the 'serial' page."""

    def __init__(self, parent, text_box):
        super().__init__(parent)
        self.text_browser = text_box
        self.text_browser.setGeometry(QtCore.QRect(int(parent.width() * 0.05), int(parent.height() * 0.05),
                                                   int(parent.width() * 0.90), int(parent.height() * 0.90)))
        self.text_browser.setParent(self)
        
        font = QtGui.QFont()
        font.setPixelSize(int(parent.height() * 0.04))
        self.text_browser.setFont(font)

    #def print(self, text):
    #    """Print the text to the screen."""
    #    self.text_browser.append(text)

class SerialTextBox(QtWidgets.QTextBrowser):
    """This class inherits from a QTextBrowser.
       It contains the text box."""
    
    def print(self, text):
        """Print the text to the screen."""
        self.append(text) 

