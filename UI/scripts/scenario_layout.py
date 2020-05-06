# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg
from scenario_creator import scenario_creator

class scenario_layout(QtWidgets.QWidget):

    def __init__(self, dataManager, MainWindow, parent):
        super().__init__()
        self.setStyleSheet("QGraphicsView {background-color: rgba(255, 255, 255, 0)} ")

        self.data_manager = dataManager
        #self.data_manager.connect(self.update_info_text)
        self.MainWindow = MainWindow

        width = parent.width()
        height = parent.height()
       
        self.create_description(width, height)  
        self.create_graph(width, height)
        self.create_scenarios() 
        self.create_list(width, height)
        self.create_buttons(width, height)     
        self.create_title(width, height)
        #self.create_info_text(width, height)

        self.scenarios_list.setCurrentRow(0)

    def create_scenarios(self):
        self.scenarios = scenario_creator(self.graph, self.scenario_description)
        self.data_manager.add_scenarios(self.scenarios)
    
    def create_list(self, width, height):

        font = QtGui.QFont()
        font.setPixelSize(int(height * 0.06))

        self.scenarios_list = QtWidgets.QListWidget(self)
        self.scenarios_list.setGeometry(QtCore.QRect(int(width * 0.05), int(height * 0.21), int(width * 0.37), int(height * 0.7)))
        self.scenarios_list.setFont(font)
        self.scenarios_list.currentRowChanged.connect(self.scenarios.update_current_scenario)

        for scenario in self.scenarios.get_scenario_list():
            QtWidgets.QListWidgetItem(scenario.get_name(), self.scenarios_list)

    def create_description(self, width, height):

        font = QtGui.QFont()
        font.setPixelSize(int(height * 0.03))

        self.scenario_description = QtWidgets.QLabel(self)
        self.scenario_description.setGeometry(QtCore.QRect(int(width * 0.5), int(height * 0.125), int(width * 0.46), int(height * 0.09)))
        self.scenario_description.setFont(font)
        self.scenario_description.setAlignment(QtCore.Qt.AlignHCenter)
        self.scenario_description.setAlignment(QtCore.Qt.AlignTop)
        self.scenario_description.setWordWrap(True)
    
    def create_buttons(self, width, height):

        font = QtGui.QFont()
        font.setPixelSize(int(height * 0.04))
        font.setBold(True)
        font.setWeight(75)

        self.run_button = QtWidgets.QPushButton(self)
        self.run_button.setGeometry(QtCore.QRect(int(width * 0.46), int(height * 0.85), int(width * 0.11), int(height * 0.07)))
        self.run_button.setFont(font)
        self.run_button.setText("Start")
        self.run_button.clicked.connect(self.update_data_manager)

        self.stop_button = QtWidgets.QPushButton(self)
        self.stop_button.setGeometry(QtCore.QRect(int(width * 0.59), int(height * 0.85), int(width * 0.11), int(height * 0.07)))
        self.stop_button.setFont(font)
        self.stop_button.setText("Stop")
        self.stop_button.clicked.connect(self.update_data_manager)
        self.stop_button.setStyleSheet("QPushButton {background-color: rgba(255, 0, 0, 200); color: rgb(255, 255, 255)}"
                                       "QPushButton::hover {background-color: rgba(255, 0, 0, 220)}"
                                       "QPushButton::pressed {background-color: rgba(255, 0, 0, 255)}" )

    def create_title(self, width, height):
        font = QtGui.QFont()
        font.setPixelSize(int(height * 0.05))
        font.setBold(True)
        font.setWeight(75)
        self.scenario_title = QtWidgets.QLabel(self)
        self.scenario_title.setGeometry(QtCore.QRect(int(width * 0.050), int(height * 0.09), int(width * 0.371), int(height * 0.09)))
        self.scenario_title.setFont(font)
        self.scenario_title.setAlignment(QtCore.Qt.AlignHCenter)
        self.scenario_title.setText("Scenario's")
    
    def create_graph(self, width, height):
        
        self.graph = pg.PlotWidget(self)
        self.graph.setGeometry(QtCore.QRect(int(width * 0.46), int(height * 0.23), int(width * 0.51), int(height * 0.6)))
        self.graph.setBackground(None)
        self.graph.getPlotItem().getAxis('left').setPen('w')
        self.graph.getPlotItem().getAxis('bottom').setPen('w')
        self.graph.setAntialiasing(True)
        self.graph.enableAutoRange('x', True)
        self.graph.setYRange(0, 6)
        self.graph.addLegend(size=(int(width * 0.14), int(height * 0.18)), offset=(-1, 1) )

    def update_data_manager(self):

        if self.MainWindow.sender().text() == 'Start':
            self.data_manager.setData('scenario', self.scenarios.get_current_scenario())
        else:
            self.data_manager.setData('stop', None)

    def create_info_text(self, width, height):
        font = QtGui.QFont()
        font.setPixelSize(int(height * 0.03))
        
        self.info_text_left = QtWidgets.QLabel(self)
        self.info_text_left.setGeometry(QtCore.QRect(int(width * 0.71), int(height * 0.85), int(width * 0.06), int(height * 0.07)))
        self.info_text_left.setAlignment(QtCore.Qt.AlignTop)
        self.info_text_left.setAlignment(QtCore.Qt.AlignRight)
        self.info_text_left.setFont(font)
        self.info_text_left.setText("Modus:")

        self.info_text_right = QtWidgets.QLabel(self)
        self.info_text_right.setGeometry(QtCore.QRect(int(width * 0.78), int(height * 0.85), int(width * 0.22), int(height * 0.14)))
        self.info_text_right.setAlignment(QtCore.Qt.AlignTop)
        self.info_text_right.setAlignment(QtCore.Qt.AlignLeft)
        self.info_text_right.setFont(font)
        self.info_text_right.setText("")
    
    def update_info_text(self):
        mode, details = self.data_manager.get_data()

        if mode == 'manual':
            self.info_text_right.setText("{:7}\nS, W, D: {:.0%}, {:.0%}, {:.0%}".format(mode.capitalize(), details[0]/100, details[1]/100, details[2]/100))
        elif mode == 'scenario':
            self.info_text_right.setText("{:7}\n{:}".format(mode.capitalize(), details.get_name()))
        elif mode == 'stop':
            self.info_text_right.setText("Stopped")
    

