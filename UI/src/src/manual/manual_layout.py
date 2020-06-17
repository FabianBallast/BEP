"""This module handles the manual control page of the UI."""

from PyQt5 import QtCore, QtGui, QtWidgets
from pyqtgraph import GraphicsLayoutWidget

class ManualLayout(QtWidgets.QWidget):
    """This class inherits from a QWidget.
       It contains all components on the 'manual control' page."""

    def __init__(self, dataManager, MainWindow, parent):

        super().__init__()
        self.mode_nl = ['Zon', 'Wind', 'Vraag']
        self.mode = ['solar', 'wind', 'demand']

        width = parent.width()
        height = parent.height()
        self.data_manager = dataManager
        self.create_title(width, height)
        self.create_sliders(width, height)
        self.create_buttons(width, height)
        
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
            exec(f"self.{mode}_power_slider.sliderReleased.connect(self.update_data_manager)")


            font.setPixelSize(int(height * 0.07))
            exec(f"self.{mode}_power_symb = QtWidgets.QLabel(self)")
            exec(f"self.{mode}_power_symb.setGeometry({x_pos[i] + int(width * 0.125)}, {y_pos[2]},"
                                                    f"{wid[2]}, {hei[2]})")
            exec(f"self.{mode}_power_symb.setText('%')")
            exec(f"self.{mode}_power_symb.setFont(font)")

            i += 1

        
        font.setPixelSize(int(height * 0.07))
        self.opslag_title = QtWidgets.QLabel(self)
        self.opslag_title.setFont(font)
        self.opslag_title.setAlignment(QtCore.Qt.AlignCenter)
        self.opslag_title.setText('Opslaan')
        self.opslag_title.setGeometry(QtCore.QRect(int(width * 0.8), y_pos[0],wid[0], hei[0]))
        self.opslag_title.setStyleSheet("QLabel { color : rgba(21, 255, 0, 255); }")

        self.bijspring_title = QtWidgets.QLabel(self)
        self.bijspring_title.setFont(font)
        self.bijspring_title.setAlignment(QtCore.Qt.AlignCenter)
        self.bijspring_title.setText('Verbruiken')
        self.bijspring_title.setGeometry(QtCore.QRect(int(width * 0.8), y_pos[2],wid[0], hei[0]))
        self.bijspring_title.setStyleSheet("QLabel {color : red; }")
        font.setPixelSize(int(height * 0.03))
        
        overhead3 = GraphicsLayoutWidget(self)
        overhead3.setGeometry(QtCore.QRect(int(width * 0.85), int(y_pos[1] + + 0.49*hei[1]) ,int(width * 0.05), int(0.02*hei[1])))
        overhead3.setBackground('w')
        
        self.h2_slide = QtWidgets.QSlider(self)
        self.h2_slide.setRange(-100,100)
        self.h2_slide.setOrientation(QtCore.Qt.Vertical)
        self.h2_slide.setGeometry(int(width * 0.8), y_pos[1],wid[0], hei[1])
        self.h2_slide.setStyleSheet("""QSlider {background-color: rgba(255, 255, 255, 0)}
              QSlider::handle:vertical {
                                background: black;
                                margin: 0 -80px;
                                border: 1px solid;
                                height: 10px;
                                     }
              QSlider::groove:vertical {
                                background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0             
                                                         green, stop:1 
                                                         red);
                                width: 10px;
                                margin: 0 -5px;
                                
                                     }    """)
        overhead = GraphicsLayoutWidget(self)
        overhead.setGeometry(QtCore.QRect(int(width * 0.8), y_pos[1],wid[0], hei[1]))
        overhead.setBackground(None)
        overhead2 = overhead.addViewBox(enableMouse=False)
        overhead2.setBackgroundColor(None)
        overhead2.setAutoPan(False,False)

        self.data_manager.h2_slide = self.h2_slide


    def create_buttons(self, width, height):
        """Creates the Start/Stop buttons."""
        font = QtGui.QFont()
        font.setPixelSize(int(height * 0.04))
        #font.setBold(True)
        font.setWeight(20)

        buttons = ['stop']                         #pylint: disable=C0103 
        y_pos = [int(0.1 * height), int(0.61 * height)]

        for button in buttons:
            exec(f"self.{button}_button = QtWidgets.QPushButton(self)")
            exec(f"self.{button}_button.setGeometry(QtCore.QRect({int(width * 0.8)}," 
                                                               f"{y_pos[buttons.index(button)]}," 
                                                               f"{int(width * 0.15)}," 
                                                               f"{int(height * 0.05)}))")
            exec(f"self.{button}_button.setFont(font)")
            exec(f"self.{button}_button.setText('Stop')")
            exec(f"self.{button}_button.clicked.connect(self.update_data_manager)")
        
        self.stop_button.setStyleSheet("QPushButton {background-color: rgba(255, 0, 0, 200);" 
                                                    "color: rgb(255, 255, 255)}"
                                       "QPushButton::hover {background-color: rgba(255, 0, 0, 220)}"
                                       "QPushButton::pressed {background-color: rgba(255, 0, 0, 255)}") #pylint: disable=C0301
                
    def update_data_manager(self):
        """Updates the data manager. 
           Is called when a Start/Stop button is pressed."""
        if self.main_window.sender() == self.stop_button:
            self.data_manager.set_mode('stop', None)

        # elif self.main_window.sender() == self.purge_button:    
        #     self.data_manager.purge_valve_manual()
        else:
            self.data_manager.set_mode('manual', 
                                       [self.solar_power_slider.value(), 
                                        self.wind_power_slider.value(), 
                                        self.demand_power_slider.value()])


        
            
