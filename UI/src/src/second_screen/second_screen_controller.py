"""This module deals with the second (not-touch) screen. 
   It handles the 'second screen' page on the UI."""
from PyQt5 import QtWidgets, QtCore, QtGui

from ..graphs.graph_layout import GraphLayout
from ..map.map_layout import MapLayout
from ..system.system import System

class SecondScreenController(QtWidgets.QWidget):
    """This class inherits from a QWidget.
       It contains all components on the 'second screen' page."""

    def __init__(self, parent):
        super().__init__()

        width = parent.width()
        height = parent.height()
        
        self.create_page_images(width, height)
        self.create_list(width, height)
        self.create_select_button(width, height)
        
    
    def create_list(self, width, height):
        """Creates a list with the different options for the second screen."""
        font = QtGui.QFont()
        font.setPixelSize(int(height * 0.05))

        self.scenarios_list = QtWidgets.QListWidget(self)
        self.scenarios_list.setGeometry(QtCore.QRect(int(width * 0.25), int(height * 0.05), 
                                                     int(width * 0.50), int(height * 0.76)))
        self.scenarios_list.setFont(font)
        self.scenarios_list.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scenarios_list.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        item_graph = QtWidgets.QListWidgetItem("Grafieken", self.scenarios_list)
        item_graph.setSizeHint(QtCore.QSize(int(width * 0.8), int(height * 0.25)))
        item_map = QtWidgets.QListWidgetItem("Map", self.scenarios_list)
        item_map.setSizeHint(QtCore.QSize(int(width * 0.8), int(height * 0.25)))
        item_figures = QtWidgets.QListWidgetItem("Cijfers", self.scenarios_list)
        item_figures.setSizeHint(QtCore.QSize(int(width * 0.8), int(height * 0.25)))

    def create_select_button(self, width, height):
        """Create a button to confirm the new widget on the second screen."""
        font = QtGui.QFont()
        font.setPixelSize(int(height * 0.035))
        font.setBold(True)
        font.setWeight(75)

        self.accept_button = QtWidgets.QPushButton(self)
        self.accept_button.setText("Verander Scherm")
        self.accept_button.setFont(font)
        self.accept_button.setGeometry(QtCore.QRect(int(width * 0.375), int(height * 0.85), 
                                                    int(width * 0.25), int(height * 0.1)))

    def create_page_images(self, width, height):
        """Create the images to visualize the different screens that could be seelcted."""
        main_window = 'Does Nothing'
        self.graph_widget = QtWidgets.QWidget(self)
        self.graph_widget.setStyleSheet("background: rgba(0, 0, 0, 0)")
        self.graph_widget.setGeometry(QtCore.QRect(int(width * 0.50), int(height * 0.05), 
                                                   int(width * 0.20), int(height * 0.25)))
        GraphLayout(main_window, 2, self.graph_widget)
        #self.graph_widget.raise_()
     
        self.map_widget = QtWidgets.QWidget(self)
        self.map_widget.setStyleSheet("background: rgba(0, 0, 0, 0)")
        self.map_widget.setGeometry(QtCore.QRect(int(width * 0.50), int(height * 0.30), 
                                                 int(width * 0.20), int(height * 0.25)))
        MapLayout(main_window, self.map_widget)
        self.map_widget.raise_()

        self.figure_widget = QtWidgets.QWidget(self)
        self.figure_widget.setStyleSheet("background: rgba(0, 0, 0, 0)")
        self.figure_widget.setGeometry(QtCore.QRect(int(width * 0.50), int(height * 0.55), 
                                                    int(width * 0.20), int(height * 0.25)))
        System(self.figure_widget, preview_version=True)
        #self.figure_widget.raise_()


    def get_selected_item(self):
        """Returns the current row that is selected in the list."""
        return self.scenarios_list.currentRow()
