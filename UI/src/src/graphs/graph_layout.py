# -*- coding: utf-8 -*-
import sys
sys.path.insert(1, '../libs')

from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg

class graph_layout(QtWidgets.QWidget):

    def __init__(self, dataManager, MainWindow, screen_number, parent):

        super().__init__(parent)
        self.graph = pg.PlotWidget(self)    
        self.MainWindow = MainWindow
        self.dataManager = dataManager
        self.screen_number = screen_number
        self.send_values = lambda x, y, z: x+y+z

        self.setStyleSheet("QCheckBox {background-color: rgba(255, 255, 255, 0); color: rgb(255, 255, 255)}"
                                "QGraphicsView {background-color: rgba(255, 255, 255, 0); color: rgb(255, 255, 255)} ")
                   
        self.mode = ['solar', 'wind', 'demand']
        self.mode_nl = ['zon', 'wind', 'vraag']
        self.colors = ['255, 255, 255', '255, 0, 0', '255, 255, 0']
        self.opa = ['255', '255', '255']
        self.width = '2'
        self.prev_mode = ''

        width = parent.width()
        height = parent.height()
        
        if self.screen_number == 1:
            self.create_checks(width, height)
            self.create_reset_button(width, height)

        self.create_plots(width, height)
    
    def create_checks(self, width, height):

        font = QtGui.QFont()
        font.setPixelSize(int(height * 0.045))

        x, y = int(width * 0.775), [int(height * 0.30), int(height * 0.40), int(height * 0.50)]
        w, h = int(width * 0.2), int(height * 0.1)

        for i in range(len(self.mode)):
            exec(f"self.{self.mode[i]}_power_check = QtWidgets.QCheckBox(self)")
            exec(f"self.{self.mode[i]}_power_check.setFixedWidth({int(width * 0.2)})")
            exec(f"self.{self.mode[i]}_power_check.setFont(font)")
            exec(f"self.{self.mode[i]}_power_check.setText('{self.mode_nl[i].capitalize()}')")
            exec(f"self.{self.mode[i]}_power_check.setChecked(True)")
            exec(f"self.{self.mode[i]}_power_check.setObjectName('solar_power_check')")
            exec(f"self.{self.mode[i]}_power_check.clicked.connect(self.check_changed)")
            exec(f"self.{self.mode[i]}_power_check.setGeometry(QtCore.QRect({x}, {y[i]}, {w}, {h}))")

    def create_plots(self, width, height):
        
        self.graph.getPlotItem().getAxis('left').setPen('w')
        self.graph.getPlotItem().getAxis('bottom').setPen('w')
        if self.screen_number == 1:
            self.graph.setGeometry(QtCore.QRect(0, int(height * 0.015), int(width * 0.775), int(height * 0.95)))
        else:
            self.graph.setGeometry(QtCore.QRect(0, int(height * 0.015), int(width * 0.95), int(height * 0.975)))
        #self.graph.enableAutoRange('y', False)
        self.graph.enableAutoRange('x', True)
        self.graph.setYRange(0, 5.2)
        self.graph.setBackground(None)
        self.graph.addLegend(size=(int(width * 0.14), int(height * 0.18)), offset=(-1, 1))

        for i in range(len(self.mode)):
            exec(f"self.{self.mode[i]}_graph = self.graph.plot(pen = pg.mkPen(color=({self.colors[i] + ', ' + self.opa[i]}), width={self.width}), name='{self.mode_nl[i].capitalize()}')")

        self.x_curr = []
        self.solar = []
        self.wind = []
        self.demand = []
        self.ind = 0
        self.scen_ind = 0
        self.max_len = 400

        if self.screen_number == 1:

            self.time_past = QtCore.QTime()
            self.time_past.start()

            self.timer = QtCore.QTimer()
            self.timer.timeout.connect(self.update_graph_1)
            self.timer.start(50)
    
    def create_reset_button(self, width, height):
        
        self.reset_button = QtWidgets.QPushButton(self)
        self.reset_button.setGeometry(QtCore.QRect(int(width * 0.775), int(height * 0.65), int(width * 0.2), int(height * 0.09)))
        self.reset_button.setText("Reset")
        self.reset_button.setStyleSheet("QPushButton {background-color: rgba(0, 255, 0, 180); color: rgb(255, 255, 255)}"
                                        "QPushButton::hover {background-color: rgba(0, 255, 0, 215)}"
                                        "QPushButton::pressed {background-color: rgba(0, 255, 0, 255)}")
        font = QtGui.QFont()
        font.setPixelSize(int(height * 0.05))
        font.setBold(True)
        self.reset_button.setFont(font)
        self.reset_button.clicked.connect(self.reset_graph)

    def update_graph_1(self):
        mode, details = self.dataManager.get_data()
        t = self.time_past.elapsed() / 1000 #in s. 

        if mode == 'manual':
            x = t
            sol = details[0] / 20
            wind = details[1] / 20 
            demand = details[2] / 20 
        elif mode == 'scenario':
            (solar_graph, wind_graph, demand_graph) = details.get_graphs()
            x = t
            sol = solar_graph[self.scen_ind]
            wind = wind_graph[self.scen_ind]
            demand = demand_graph[self.scen_ind]

            if self.scen_ind < details.get_length() - 1:
                self.scen_ind += 1
            else:
                self.scen_ind = 0
        else:
            x = 0
            sol = 0
            wind = 0
            demand = 0

        if len(self.x_curr) == self.max_len:
            del self.x_curr[0], self.solar[0], self.wind[0], self.demand[0]

        self.send_values(sol, wind, demand)

        self.x_curr.append(x)
        self.solar.append(sol)
        self.wind.append(wind)
        self.demand.append(demand)

        self.plot_in_other(self.x_curr, self.solar, self.wind, self.demand)

        if self.ind < self.max_len - 1:
            self.ind += 1
        else:
            self.ind = 0

        self.solar_graph.setData(self.x_curr, self.solar)
        self.wind_graph.setData(self.x_curr, self.wind)
        self.demand_graph.setData(self.x_curr, self.demand)
    
    def update_graph_2(self, x, solar, wind, demand):
         
        self.solar_graph.setData(x, solar)
        self.wind_graph.setData(x, wind)
        self.demand_graph.setData(x, demand)
    

    def reset_graph(self):
        self.solar = []
        self.wind = []
        self.demand = []
        self.x_curr = []
        self.ind = 0
        self.scen_ind = 0
        self.time_past.restart()
    
    def new_mode(self):
        
        mode, details = self.dataManager.get_data()

        if self.prev_mode != mode or mode != 'manual':
            self.reset_graph()
        
        self.prev_mode = mode


    def check_changed(self):

        origin = self.MainWindow.sender().text().split()[0].lower()
        ind = self.mode.index(origin)
    
        exec(f"self.opa[{str(ind)}] = '0' if self.opa[{str(ind)}] == '255' else '255'")
        exec(f"self.{origin}_graph.setPen(color=({self.colors[ind]}, {self.opa[ind]}), width={self.width})")
    
    def connect_for_current_values(self, handler):
        self.send_values = handler

    def updater(self, handler):
        self.plot_in_other = handler 
        

       