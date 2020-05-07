# -*- coding: utf-8 -*-

import sys
sys.path.insert(1, '../libs')

from PyQt5 import QtCore, QtGui, QtWidgets
from map_layout import map_layout
from graph_layout import graph_layout
from scenario_layout import scenario_layout
from manual_layout import manual_layout
from data_manager import DataManager
from toolbars import ToolBarTop, ToolBarBottom
from help_layout import help_layout
from second_screen_controller import SecondScreenController

class Ui_MainWindow(object):

    def __init__(self, width_1, height_1, width_2, height_2):
        self.width_1 = width_1
        self.height_1 = height_1
        self.width_2 = width_2
        self.height_2 = height_2
        self.data = DataManager()

    def setupUi_2(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(self.width_2, self.height_2)
        MainWindow.setWindowTitle("User Interface 2")

        self.centralwidget_2 = QtWidgets.QWidget(MainWindow)
        self.centralwidget_2.setStyleSheet("QWidget {background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 150, 100, 255), stop:1 rgba(0, 0, 240, 255))} "
                                         "QPushButton {background-color: rgba(0, 255, 0, 200); color: rgb(255, 255, 255)}"
                                         "QPushButton::hover {background-color: rgba(0, 255, 0, 220)}"
                                         "QPushButton::pressed {background-color: rgba(0, 250, 0, 255)}"  
                                         "QCommandLinkButton {background-color: rgba(0, 0, 0, 0); color: rgb(255, 255, 255)} "
                                         "QCommandLinkButton::hover {background-color: rgba(0, 255, 0, 80)}"
                                         "QListWidget {background-color: rgba(0, 0, 0, 0); color: rgb(255, 255, 255)}"
                                         "QLabel {background-color: rgba(0, 0, 0, 0); color: rgb(255, 255, 255)}"
                                         "QSlider {background-color: rgba(255, 255, 255, 0)}"
                                         "QLCDNumber {background-color: rgba(255, 255, 255, 0)}"
                                         "QToolButton {background-color: rgba(0, 255, 0, 180); color: rgb(255, 255, 255)}"
                                         "QToolButton::hover {background-color: rgba(255, 0, 0, 210); color: rgb(255, 255, 255)}"
                                         "QToolButton::pressed {background-color: rgba(255, 0, 0, 255); color: rgb(255, 255, 255)}"
                                         "QToolBar {background-color: rgba(0, 255, 0, 255)}")

        self.stackedWidget_2 = QtWidgets.QStackedWidget(self.centralwidget_2)
        self.stackedWidget_2.setGeometry(QtCore.QRect(0, 0, self.width_2, self.height_2))
        self.stackedWidget_2.setFrameShape(QtWidgets.QFrame.NoFrame)

        #self.graph_lay_2 = graph_layout(self.data, MainWindow, 2)
        self.graphs_2 = graph_layout(self.data, MainWindow, 2, self.stackedWidget_2)
        #self.data.connect(self.graphs_2.new_mode)
        self.graphs.updater(self.graphs_2.update_graph_2)
        self.stackedWidget_2.addWidget(self.graphs_2)

        #self.map_lay_2 = map_layout(MainWindow)
        self.map_2 = map_layout(MainWindow, self.stackedWidget_2)
        self.graphs_2.connect_for_current_values(self.map_2.get_current_values)
        self.stackedWidget_2.addWidget(self.map_2)

        MainWindow.setCentralWidget(self.centralwidget_2)
        self.stackedWidget_2.setCurrentIndex(0)

        self.MW_2 = MainWindow

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def setupUi_1(self, MainWindow):

        self.current_page = 4

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 562)
        MainWindow.setWindowTitle("User Interface 1")
        MainWindow.setStyleSheet("QWidget {background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 150, 100, 255), stop:1 rgba(0, 0, 240, 255))} "
                                         "QPushButton {background-color: rgba(0, 255, 0, 200); color: rgb(255, 255, 255)}"
                                         "QPushButton::hover {background-color: rgba(0, 255, 0, 220)}"
                                         "QPushButton::pressed {background-color: rgba(0, 250, 0, 255)}"  
                                         "QCommandLinkButton {background-color: rgba(0, 0, 0, 0); color: rgb(255, 255, 255)} "
                                         "QCommandLinkButton::hover {background-color: rgba(0, 255, 0, 80)}"
                                         "QListWidget {background-color: rgba(0, 0, 0, 0); color: rgb(255, 255, 255); border: none}"
                                         "QLabel {background-color: rgba(0, 0, 0, 0); color: rgb(255, 255, 255)}"
                                         "QSlider {background-color: rgba(255, 255, 255, 0)}"
                                         "QLCDNumber {background-color: rgba(255, 255, 255, 0)}"
                                         )
        self.toolbar = ToolBarTop(self.width_1, self.height_1)
        MainWindow.addToolBar(self.toolbar)
        self.toolbar_2 = ToolBarBottom(self.width_1, self.height_1, self.data)
        MainWindow.addToolBar(QtCore.Qt.BottomToolBarArea, self.toolbar_2)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setGeometry(QtCore.QRect(0, 0, self.width_1, self.height_1 - self.toolbar.height() - self.toolbar_2.height()))
        #self.centralwidget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        #print(self.centralwidget.height())
        #print(self.centralwidget.width())
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(0, 0, self.width_1, self.height_1 - self.toolbar.height() - self.toolbar_2.height()))
        #self.stackedWidget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        #print(self.stackedWidget.height())
        #print(self.stackedWidget.width())
        self.stackedWidget.setFrameShape(QtWidgets.QFrame.NoFrame)
        
        # First page: the graphs. Main part of the lay-out is done in graph_layout(). 
        #self.graph_lay = graph_layout(self.data, MainWindow, 1, self.width_1, self.height_1)
        self.graphs = graph_layout(self.data, MainWindow, 1, self.stackedWidget)
        self.stackedWidget.addWidget(self.graphs)

        # Second page: the map. Main part is done in map_layout(). 
        #self.map_lay = map_layout(MainWindow)
        self.map = map_layout(MainWindow, self.stackedWidget)
        self.stackedWidget.addWidget(self.map)

        self.graphs.connect_for_current_values(self.map.get_current_values)
        
        # Third page: scenarios. 
        #self.scen_lay = 
        self.scenarios = scenario_layout(self.data, MainWindow, self.stackedWidget)
        self.stackedWidget.addWidget(self.scenarios)

        # Fourth page: the manual control page. 
        self.manual_control = manual_layout(self.data, MainWindow, self.stackedWidget)
        self.stackedWidget.addWidget(self.manual_control)

        # Fifth page: Help page
        self.help_page = help_layout(self.stackedWidget)
        self.stackedWidget.addWidget(self.help_page)

        # Sixth page: the second screen controller
        self.second_screen = SecondScreenController(self.stackedWidget)
        self.stackedWidget.addWidget(self.second_screen)

        MainWindow.setCentralWidget(self.centralwidget)
        self.stackedWidget.setCurrentIndex(4)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.connect_pages_to_buttons()
        
    def connect_pages_to_buttons(self):   

        self.toolbar.graphs_button.triggered.connect(self.goToGraphPage)
        self.toolbar.scenario_button.triggered.connect(self.goToScenariosPage)
        self.toolbar.map_button.triggered.connect(self.goToMapPage)
        self.toolbar.manual_control_button.triggered.connect(self.goToManualControlPage)
        self.toolbar.help_button.triggered.connect(self.goToHelp) 
        self.toolbar.screen_button.triggered.connect(self.goToSecondScreenPage)

        #self.scenarios.run_button.clicked.connect(self.man_layout.update_status_text)
        #self.help_page.continue_button.clicked.connect(self.return_to_page)
        self.second_screen.accept_button.clicked.connect(self.changeScreen)
        #self.data.connect(self.scenarios.update_info_text)
        #self.data.connect(self.manual_control.update_status_text)
        self.data.connect(self.toolbar_2.update_text)
        self.data.connect(self.graphs.new_mode)


    def goToGraphPage(self):
        self.stackedWidget.setCurrentIndex(0)
        self.current_page = 0
    
    def goToMapPage(self):
        self.stackedWidget.setCurrentIndex(1)
        self.current_page = 1

    def goToScenariosPage(self):
        self.stackedWidget.setCurrentIndex(2)
        self.current_page = 2
    
    def goToManualControlPage(self):
        self.stackedWidget.setCurrentIndex(3)
        self.current_page = 3
    
    def goToSecondScreenPage(self):
        self.stackedWidget.setCurrentIndex(5)
        self.current_page = 5
    
    def return_to_page(self):
        if self.current_page != 4:
            self.stackedWidget.setCurrentIndex(self.current_page)
        else:
            self.stackedWidget.setCurrentIndex(0)
    
    def goToHelp(self):
        self.stackedWidget.setCurrentIndex(4)
    
    def changeScreen(self):

        self.stackedWidget_2.setCurrentIndex(self.second_screen.get_selected_item())
    

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    desktop = app.desktop()
    screen = desktop.screenCount()

    monitor_1 = QtWidgets.QDesktopWidget().screenGeometry(0)
    monitor_2 = QtWidgets.QDesktopWidget().screenGeometry(1)

    
    ui = Ui_MainWindow(monitor_1.width(), monitor_1.height(), monitor_2.width(), monitor_2.height())

    MainWindow_1 = QtWidgets.QMainWindow()
    ui.setupUi_1(MainWindow_1)    
    MainWindow_1.showFullScreen()

    MainWindow_2 = QtWidgets.QMainWindow()
    ui.setupUi_2(MainWindow_2)
    
    if screen == 2:
        MainWindow_2.move(monitor_2.left(), monitor_2.top())
        MainWindow_2.showFullScreen()
    
    sys.exit(app.exec_())
