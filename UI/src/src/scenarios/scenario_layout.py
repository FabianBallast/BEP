"""This module handles the scenario page of the UI."""
from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg
from ..scenarios.scenario_creator import ScenarioCreator

class ScenarioLayout(QtWidgets.QWidget):
    """This class inherits from a QWidget.
       It contains all components on the 'scenario' page."""

    def __init__(self, dataManager, MainWindow, parent):
        super().__init__()
        #self.setStyleSheet("QGraphicsView {background-color: rgba(255, 255, 255, 0)} ")

        self.data_manager = dataManager
        self.main_window = MainWindow

        width = parent.width()
        height = parent.height()
       
        self.create_description(width, height)  
        self.create_graph(width, height)
        self.create_scenarios() 
        self.create_list(width, height)
        self.create_buttons(width, height)     
        self.create_title(width, height)

        self.scenarios_list.setCurrentRow(0)

    def create_scenarios(self):
        """Create all the different scenarios."""
        self.scenarios = ScenarioCreator(self.graph, self.scenario_description)
        #self.data_manager.add_scenarios(self.scenarios)
    
    def create_list(self, width, height):
        """Create a list with all the possible scenarios."""
        font = QtGui.QFont()
        font.setPixelSize(int(height * 0.06))

        self.scenarios_list = QtWidgets.QListWidget(self)
        self.scenarios_list.setGeometry(QtCore.QRect(int(width * 0.05), int(height * 0.21), 
                                                     int(width * 0.37), int(height * 0.7)))
        self.scenarios_list.setFont(font)
        self.scenarios_list.currentRowChanged.connect(self.scenarios.update_current_scenario)

        for scenario in self.scenarios.get_scenario_list():
            QtWidgets.QListWidgetItem(scenario.get_name(), self.scenarios_list)

    def create_description(self, width, height):
        """Create a label for the summary of each scenario."""
        font = QtGui.QFont()
        font.setPixelSize(int(height * 0.03))

        self.scenario_description = QtWidgets.QLabel(self)
        self.scenario_description.setGeometry(QtCore.QRect(int(width * 0.5), int(height * 0.125), 
                                                           int(width * 0.46), int(height * 0.09)))
        self.scenario_description.setFont(font)
        self.scenario_description.setAlignment(QtCore.Qt.AlignHCenter)
        self.scenario_description.setAlignment(QtCore.Qt.AlignTop)
        self.scenario_description.setWordWrap(True)
    
    def create_buttons(self, width, height):
        """Create Start/Stop buttons."""
        font = QtGui.QFont()
        font.setPixelSize(int(height * 0.04))
        font.setBold(True)
        font.setWeight(75)

        self.run_button = QtWidgets.QPushButton(self)
        self.run_button.setGeometry(QtCore.QRect(int(width * 0.46), int(height * 0.85), 
                                                 int(width * 0.11), int(height * 0.07)))
        self.run_button.setFont(font)
        self.run_button.setText("Start")
        self.run_button.clicked.connect(self.update_data_manager)

        self.stop_button = QtWidgets.QPushButton(self)
        self.stop_button.setGeometry(QtCore.QRect(int(width * 0.59), int(height * 0.85), 
                                                  int(width * 0.11), int(height * 0.07)))
        self.stop_button.setFont(font)
        self.stop_button.setText("Stop")
        self.stop_button.clicked.connect(self.update_data_manager)
        self.stop_button.setStyleSheet("QPushButton {background-color: rgba(255, 0, 0, 200);" 
                                                    "color: rgb(255, 255, 255)}"
                                       "QPushButton::hover {background-color: rgba(255, 0, 0, 220)}"
                                       "QPushButton::pressed {background-color: rgba(255, 0, 0, 255)}")   #pylint: disable=C0301

    def create_title(self, width, height):
        """Create a label for the title of this page."""
        font = QtGui.QFont()
        font.setPixelSize(int(height * 0.05))
        font.setBold(True)
        font.setWeight(75)
        self.scenario_title = QtWidgets.QLabel(self)
        self.scenario_title.setGeometry(QtCore.QRect(int(width * 0.050), int(height * 0.09), 
                                                     int(width * 0.371), int(height * 0.09)))
        self.scenario_title.setFont(font)
        self.scenario_title.setAlignment(QtCore.Qt.AlignHCenter)
        self.scenario_title.setText("Scenario's")
    
    def create_graph(self, width, height):
        """Create a graph to show the data from scenario."""
        self.graph = pg.PlotWidget(self)
        self.graph.setGeometry(QtCore.QRect(int(width * 0.46), int(height * 0.23), 
                                            int(width * 0.51), int(height * 0.6)))
        self.graph.setBackground(None)
        self.graph.getPlotItem().getAxis('left').setPen('w')
        self.graph.getPlotItem().getAxis('bottom').setPen('w')
        self.graph.setAntialiasing(True)
        self.graph.enableAutoRange('x', True)
        self.graph.setYRange(0, 6)
        self.graph.addLegend(size=(int(width * 0.14), int(height * 0.18)), offset=(-1, 1))

    def update_data_manager(self):
        """If the buttons are pressed, the DataManager object should be updated."""
        if self.main_window.sender().text() == 'Start':
            self.data_manager.setData('scenario', self.scenarios.get_current_scenario())
        else:
            self.data_manager.setData('stop', None)
