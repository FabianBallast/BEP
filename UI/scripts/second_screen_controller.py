# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from graph_layout import graph_layout
from map_layout import map_layout
from data_manager import DataManager

class SecondScreenController(QtWidgets.QWidget):

    def __init__(self, parent):
        super().__init__()

        width = parent.width()
        height = parent.height()
        
        self.create_page_images(width, height)
        self.create_list(width, height)
        self.create_select_button(width, height)
        
    
    def create_list(self, width, height):
        font = QtGui.QFont()
        font.setPixelSize(int(height * 0.05))

        self.scenarios_list = QtWidgets.QListWidget(self)
        self.scenarios_list.setGeometry(QtCore.QRect(int(width * 0.25), int(height * 0.1), int(width * 0.5), int(height * 0.61)))
        self.scenarios_list.setFont(font)
        self.scenarios_list.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scenarios_list.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        item_graph = QtWidgets.QListWidgetItem("Grafieken", self.scenarios_list)
        item_graph.setSizeHint(QtCore.QSize(int(width * 0.8), int(height * 0.3)))
        item_map = QtWidgets.QListWidgetItem("Map", self.scenarios_list)
        item_map.setSizeHint(QtCore.QSize(int(width * 0.8), int(height * 0.3)))

    def create_select_button(self, width, height):
        font = QtGui.QFont()
        font.setPixelSize(int(height * 0.035))
        font.setBold(True)
        font.setWeight(75)

        self.accept_button = QtWidgets.QPushButton(self)
        self.accept_button.setText("Verander Scherm")
        self.accept_button.setFont(font)
        self.accept_button.setGeometry(QtCore.QRect(int(width * 0.375), int(height * 0.75), int(width * 0.25), int(height * 0.1)))

    def create_page_images(self, width, height):
        
        MainWindow = 'Does Nothing'
        self.graph_widget = QtWidgets.QWidget(self)
        self.graph_widget.setStyleSheet("background: rgba(0, 0, 0, 0)")
        self.graph_widget.setGeometry(QtCore.QRect(int(width * 0.45), int(height*0.11), int(width * 0.3), int(height * 0.3)))
        graph_layout(DataManager(), MainWindow, 2, self.graph_widget)
     
        self.map_widget = QtWidgets.QWidget(self)
        self.map_widget.setStyleSheet("background: rgba(0, 0, 0, 0)")
        self.map_widget.setGeometry(QtCore.QRect(int(width * 0.45), int(height*0.41), int(width * 0.3), int(height * 0.3)))
        map_layout(MainWindow, self.map_widget)


    def get_selected_item(self):
        return self.scenarios_list.currentRow()

