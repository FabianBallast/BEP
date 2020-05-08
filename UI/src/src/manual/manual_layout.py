"""This module handles the manual control page of the UI."""

from PyQt5 import QtCore, QtGui, QtWidgets

class ManualLayout(QtWidgets.QWidget):
    """This class inherits from a QWidget.
       It contains all components on the 'manual control' page."""

    def __init__(self, dataManager, MainWindow, parent):

        super().__init__()
        self.mode_nl = ['Zon', 'Wind', 'Vraag']
        self.mode = ['solar', 'wind', 'demand']

        width = parent.width()
        height = parent.height()

        self.create_title(width, height)
        self.create_sliders(width, height)
        self.create_buttons(width, height)
        self.data_manager = dataManager
        self.main_window = MainWindow
    
    def create_title(self, width, height):
        """Creates a label with the title of the page."""
        font = QtGui.QFont()
        font.setPixelSize(int(height * 0.08))

        self.page_title = QtWidgets.QLabel(self)
        self.page_title.setGeometry(QtCore.QRect(int(width * 0.05), int(height * 0.05), 
                                                int(width * 0.650), int(height * 0.14)))
        self.page_title.setFont(font)
        self.page_title.setAlignment(QtCore.Qt.AlignCenter)
        self.page_title.setText("Handmatige besturing")

    def create_sliders(self, width, height):
        """Creates the sliders, label for the slider, 
           text with value of slider and the percentage sign."""
        font = QtGui.QFont()

        x_pos = [int(width * x) for x in [0.05, 0.3, 0.55]]
        y_pos = [int(height * y) for y in [0.24, 0.33, 0.80]]
        wid = [int(width * x) for x in [0.15, 0.05, 0.04]]
        hei = [int(height * y) for y in [0.09, 0.44, 0.09]]
        i = 0

        for mode in self.mode:
            font.setPixelSize(int(height * 0.07))
            exec(f"self.{mode}_power_title = QtWidgets.QLabel(self)")
            exec(f"self.{mode}_power_title.setFont(font)")
            exec(f"self.{mode}_power_title.setAlignment(QtCore.Qt.AlignCenter)")
            exec(f"self.{mode}_power_title.setText('{self.mode_nl[self.mode.index(mode)]}')")
            exec(f"self.{mode}_power_title.setGeometry(QtCore.QRect({x_pos[i]}, {y_pos[0]}," 
                                                                  f"{wid[0]}, {hei[0]}))")

            font.setPixelSize(int(height * 0.03))
            exec(f"self.{mode}_power_value = QtWidgets.QLCDNumber(self)")
            exec(f"self.{mode}_power_value.setGeometry({x_pos[i]}, {y_pos[2]}, {wid[0]}, {hei[2]})")
            exec(f"self.{mode}_power_value.setFont(font)")
            exec(f"self.{mode}_power_value.setDigitCount(3)")
            exec(f"self.{mode}_power_value.display(0)")

            exec(f"self.{mode}_power_slider = QtWidgets.QSlider(self)")
            exec(f"self.{mode}_power_slider.setMaximum(100)")
            exec(f"self.{mode}_power_slider.setOrientation(QtCore.Qt.Vertical)")
            exec(f"self.{mode}_power_slider.setGeometry({x_pos[i]}, {y_pos[1]}," 
                                                      f"{wid[0]}, {hei[1]})")
            exec(f"self.{mode}_power_slider.valueChanged.connect(self.{mode}_power_value.display)")


            font.setPixelSize(int(height * 0.07))
            exec(f"self.{mode}_power_symb = QtWidgets.QLabel(self)")
            exec(f"self.{mode}_power_symb.setGeometry({x_pos[i] + int(width * 0.125)}, {y_pos[2]},"
                                                    f"{wid[2]}, {hei[2]})")
            exec(f"self.{mode}_power_symb.setText('%')")
            exec(f"self.{mode}_power_symb.setFont(font)")

            i += 1

    def create_buttons(self, width, height):
        """Creates the Start/Stop buttons."""
        font = QtGui.QFont()
        font.setPixelSize(int(height * 0.04))
        font.setBold(True)
        font.setWeight(75)

        buttons = ['start', 'stop']                         #pylint: disable=C0103 
        y_pos = [int(0.50 * height), int(0.61 * height)]

        for button in buttons:
            exec(f"self.{button}_button = QtWidgets.QPushButton(self)")
            exec(f"self.{button}_button.setGeometry(QtCore.QRect({int(width * 0.75)}," 
                                                               f"{y_pos[buttons.index(button)]}," 
                                                               f"{int(width * 0.2)}," 
                                                               f"{int(height * 0.09)}))")
            exec(f"self.{button}_button.setFont(font)")
            exec(f"self.{button}_button.setText('{button.capitalize()}')")
            exec(f"self.{button}_button.clicked.connect(self.update_data_manager)")
        
        self.stop_button.setStyleSheet("QPushButton {background-color: rgba(255, 0, 0, 200);" 
                                                    "color: rgb(255, 255, 255)}"
                                       "QPushButton::hover {background-color: rgba(255, 0, 0, 220)}"
                                       "QPushButton::pressed {background-color: rgba(255, 0, 0, 255)}") #pylint: disable=C0301
                
    def update_data_manager(self):
        """Updates the data manager. 
           Is called when a Start/Stop button is pressed."""
        if self.main_window.sender().text() == 'Start':
            self.data_manager.setData('manual', 
                	                 [self.solar_power_slider.value(), 
                                      self.wind_power_slider.value(), 
                                      self.demand_power_slider.value()])
        else:
            self.data_manager.setData('stop', None)
