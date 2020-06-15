"""This module handles the graph page of the UI."""

from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg

MAX_TANK = 80    /100
MAX_SOLAR = 70  /100
MAX_WIND  = 150  /100
MAX_LOAD = 4200 /100

class GraphLayout(QtWidgets.QWidget):
    """This class inherits from a QWidget.
       It contains all components on the 'graph' page."""

    def __init__(self, MainWindow, screen_number, parent):

        super().__init__(parent)
           
        self.main_window = MainWindow
        self.send_values = lambda x, y, z: x+y+z
        self.plot_in_other = lambda x, y, z: x+y+z
                   
        self.mode = ['solar', 'wind', 'demand', 'storage']
        self.mode_nl = ['zon', 'wind', 'vraag', 'opslag']
        self.colors = ['255, 255, 255', '255, 0, 0', '255, 255, 0', '0, 255, 0']
        self.opa = ['255', '255', '255', '255']
        self.width = '5'
        self.prev_mode = ''

        width = parent.width()
        height = parent.height()
        
        if screen_number == 1:
            self.create_checks(width, height)
            self.create_reset_button(width, height)

        self.create_plots(width, height, screen_number)
    
    def create_checks(self, width, height):
        """Create checkboxes to show/hide graphs."""
        font = QtGui.QFont()
        font.setPixelSize(int(height * 0.045))

        x, y = int(width * 0.775), [int(height * 0.30), int(height * 0.40),             #pylint: disable=C0103
                                    int(height * 0.50), int(height * 0.60)]
        w, h = int(width * 0.2), int(height * 0.1)                                      #pylint: disable=C0103

        for i in range(len(self.mode)):
            exec(f"self.{self.mode[i]}_power_check = QtWidgets.QCheckBox(self)")
            exec(f"self.{self.mode[i]}_power_check.setFixedWidth({int(width * 0.2)})")
            exec(f"self.{self.mode[i]}_power_check.setFont(font)")
            exec(f"self.{self.mode[i]}_power_check.setText('{self.mode_nl[i].capitalize()}')")
            exec(f"self.{self.mode[i]}_power_check.setChecked(True)")
            exec(f"self.{self.mode[i]}_power_check.setObjectName('solar_power_check')")
            exec(f"self.{self.mode[i]}_power_check.clicked.connect(self.check_changed)")
            exec(f"self.{self.mode[i]}_power_check.setGeometry(QtCore.QRect({x}, {y[i]}," 
                                                                          f"{w}, {h}))")

    def create_plots(self, width, height, screen_number):
        """"Create a plot to show all the graphs."""

        self.graph = pg.PlotWidget(self) 
        self.graph.showGrid(x=True, y=True, alpha=1)
        self.graph.getPlotItem().getAxis('left').setPen('w')
        self.graph.getPlotItem().getAxis('bottom').setPen('w')
        if screen_number == 1:
            self.graph.setGeometry(QtCore.QRect(0, int(height * 0.015), 
                                                int(width * 0.775), int(height * 0.95)))
        else:
            self.graph.setGeometry(QtCore.QRect(0, int(height * 0.015), 
                                                int(width * 0.95), int(height * 0.975)))
        #self.graph.enableAutoRange('y', False)
        self.graph.enableAutoRange('x', True)
        self.graph.setYRange(0, 104)
        self.graph.setBackground(None)
        self.graph.addLegend(size=(int(width * 0.14), int(height * 0.20)), offset=(-1, 1))

        for i in range(len(self.mode)):
            pen = f"""pg.mkPen(color=({self.colors[i] + ', ' + self.opa[i]}),  
                               width={self.width}),
                               name='{self.mode_nl[i].capitalize()}'"""

            exec(f"self.{self.mode[i]}_graph = self.graph.plot(pen = {pen})")

        self.x_curr = []
        self.solar = []
        self.wind = []
        self.demand = []
        self.storage = []
        self.scen_ind = 0
        self.max_len = 400

        if screen_number == 1:

            self.time_past = QtCore.QTime()
            self.time_past.start()
    
    def create_reset_button(self, width, height):
        """Create a reset button to reset the plot."""
        self.reset_button = QtWidgets.QPushButton(self)
        self.reset_button.setGeometry(QtCore.QRect(int(width * 0.775), int(height * 0.70), 
                                                   int(width * 0.2), int(height * 0.09)))
        self.reset_button.setText("Reset")
        self.reset_button.setStyleSheet("QPushButton {background-color: rgba(0, 255, 0, 180);" 
                                                     "color: rgb(255, 255, 255)}"
                                        "QPushButton::hover {background-color: rgba(0, 255, 0, 215)}"    #pylint: disable=C0301
                                        "QPushButton::pressed {background-color: rgba(0, 255, 0, 255)}") #pylint: disable=C0301
        font = QtGui.QFont()
        font.setPixelSize(int(height * 0.05))
        font.setBold(True)
        self.reset_button.setFont(font)

    def update_graph(self, readings):
        """Update the graph on the main screen with new data."""

        if len(self.x_curr) == self.max_len:
            del self.x_curr[0], self.solar[0], self.wind[0], self.demand[0], self.storage[0]
        
        if len(self.x_curr) > 0 and self.x_curr[-1] > readings['time']:
            self.reset_graph()
            
        
        self.x_curr.append(readings['time'])
        self.solar.append(readings['zonPower'] / MAX_SOLAR)  
        self.wind.append(readings['windPower'] / MAX_WIND )  
        self.demand.append(readings['loadPower'] / MAX_LOAD) 
        self.storage.append(readings['tank_level'] /  MAX_TANK)

        self.solar_graph.setData(self.x_curr, self.solar)
        self.wind_graph.setData(self.x_curr, self.wind)
        self.demand_graph.setData(self.x_curr, self.demand)
        self.storage_graph.setData(self.x_curr, self.storage)    

    def reset_graph(self):
        """Clear the graph and all the data."""

        self.solar = []
        self.wind = []
        self.demand = []
        self.storage = []
        self.x_curr = []
        self.scen_ind = 0

    def check_changed(self):
        """When a checkbox is checked/unchecked, the graph is updated."""

        origin = self.main_window.sender().text().split()[0].lower()
        ind = self.mode_nl.index(origin)
    
        exec(f"self.opa[{str(ind)}] = '0' if self.opa[{str(ind)}] == '255' else '255'")
        exec(f"self.{self.mode[ind]}_graph.setPen(color=({self.colors[ind]}, {self.opa[ind]}),"
                                                f"width={self.width})")
    
    def connect_for_current_values(self, handler):
        """Current data will be send according to the funtion from 'handler'."""

        self.send_values = handler

    def updater(self, handler):
        """Current data is send to the second screen."""

        self.plot_in_other = handler 
       
