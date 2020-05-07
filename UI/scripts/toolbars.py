# -*- coding: utf-8 -*-
import sys
sys.path.insert(1, '../libs')

from PyQt5 import QtCore, QtGui, QtWidgets

class ToolBarTop(QtWidgets.QToolBar):

    def __init__(self, width, height):
        super().__init__()
        self.setStyleSheet("QToolButton {background-color: rgba(0, 255, 0, 0); color: rgb(255, 255, 255)}"
                           "QToolButton::hover {background-color: rgba(0, 255, 0, 50); color: rgb(255, 255, 255)}"
                           "QToolButton::pressed {background-color: rgba(0, 255, 0, 100); color: rgb(255, 255, 255)}"
                           "QToolBar {background-color: rgba(0, 0, 0, 0); border: none}")
        
        #self.setGeometry(QtCore.QRect(0, 0, width, int(height * 0.1)))
        self.setFixedHeight(int(height * 0.1))
        self.setMovable(False)
        self.button_list = []
        
        self.create_font(height)
        self.create_page_buttons()
        self.create_help_button()
        self.create_screen_button()
        self.add_buttons()

    def create_font(self, height):
        self.toolbar_font = QtGui.QFont()
        self.toolbar_font.setFamily("Segoe UI")
        self.toolbar_font.setPixelSize(int(0.035 * height))
        self.toolbar_font.setBold(True)

    def create_page_buttons(self):

        self.map_button = QtWidgets.QAction('Map')
        self.map_button.setFont(self.toolbar_font)
        self.button_list.append(self.map_button)

        self.graphs_button = QtWidgets.QAction('Grafieken')
        self.graphs_button.setFont(self.toolbar_font)
        self.button_list.append(self.graphs_button)

        self.scenario_button = QtWidgets.QAction("Scenario's")
        self.scenario_button.setFont(self.toolbar_font)
        self.button_list.append(self.scenario_button)

        self.manual_control_button = QtWidgets.QAction("Handmatige Besturing")
        self.manual_control_button.setFont(self.toolbar_font)
        self.button_list.append(self.manual_control_button)
    
    def create_help_button(self):
        self.help_button = QtWidgets.QAction('Hulp')
        self.help_button.setFont(self.toolbar_font)
        self.button_list.append(self.help_button)
    
    def create_screen_button(self):
        self.screen_button = QtWidgets.QAction('Tweede Scherm')
        self.screen_button.setFont(self.toolbar_font)
        self.button_list.append(self.screen_button)
    
    def create_spacer(self):
        self.spacer_left = QtWidgets.QWidget(self)
        self.spacer_left.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

        self.spacer_right = QtWidgets.QWidget(self)
        self.spacer_right.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

    
    def add_buttons(self):

        for i in range(len(self.button_list)):
            spacer = QtWidgets.QWidget(self)
            spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
            self.addWidget(spacer)
            self.addAction(self.button_list[i])
        
        spacer = QtWidgets.QWidget(self)
        spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.addWidget(spacer)


class ToolBarBottom(QtWidgets.QToolBar):

    def __init__(self, width, height, data):
        super().__init__()
        self.setStyleSheet("QToolButton {background-color: rgba(0, 255, 0, 0); color: rgb(255, 255, 255)}"
                           "QToolButton::hover {background-color: rgba(0, 255, 0, 50); color: rgb(255, 255, 255)}"
                           "QToolButton::pressed {background-color: rgba(0, 255, 0, 100); color: rgb(255, 255, 255)}"
                           "QToolBar {background-color: rgba(0, 0, 0, 0); border: none}"
                           "QWidget {background-color: rgba(0, 0, 0, 0)}"
                           "QLabel {background-color: rgba(0, 0, 0, 0)}")
        
        #self.setGeometry(QtCore.QRect(0, int(height * 0.8), width, int(height * 0.1)))
        self.setFixedHeight(int(0.05*height))
        self.setMovable(False)
        self.data = data
        #self.setAllowedAreas(QtCore.Qt.BottomToolBarArea)
        
        self.create_font(height)
        self.create_labels(width)
        #self.create_page_buttons()
        #self.create_help_button()
        #self.create_screen_button()
        #self.add_buttons()

    def create_font(self, height):
        self.toolbar_font = QtGui.QFont()
        self.toolbar_font.setFamily("Segoe UI")
        self.toolbar_font.setPixelSize(int(0.035 * height))
        self.toolbar_font.setBold(True)
    
    def create_labels(self, width):
       
        self.mode_title_label = QtWidgets.QLabel(self)
        self.mode_title_label.setFixedWidth(int(width * 0.25))
        self.mode_title_label.setFixedHeight(self.height())
        self.mode_title_label.setText("Modus: ")
        self.mode_title_label.setFont(self.toolbar_font)
        self.mode_title_label.setAlignment(QtCore.Qt.AlignVCenter|QtCore.Qt.AlignRight)
        self.addWidget(self.mode_title_label)

        self.mode_label = QtWidgets.QLabel(self)
        self.mode_label.setFixedWidth(int(width* 0.25))
        self.mode_label.setFixedHeight(self.height())
        self.mode_label.setText("Gestopt")
        self.mode_label.setFont(self.toolbar_font)
        self.addWidget(self.mode_label)

        self.details_label = QtWidgets.QLabel(self)
        self.details_label.setFixedWidth(int(width * 0.495))
        self.details_label.setFixedHeight(self.height())
        self.details_label.setText("")
        self.details_label.setFont(self.toolbar_font)  
        self.addWidget(self.details_label)
    
    def update_text(self):

        mode, details = self.data.get_data()

        if mode == 'manual':
            self.mode_label.setText(f"{mode.capitalize()}")
            self.details_label.setText("Zon: {:.0%}, Wind: {:.0%}, Vraag: {:.0%}".format(details[0]/100, details[1]/100, details[2]/100))
        elif mode == 'scenario':
            self.mode_label.setText(f"{mode.capitalize()}")
            self.details_label.setText(f"{details}")
        elif mode == 'stop':
            self.mode_label.setText("Gestopt")
            self.details_label.setText("")
        else:
            self.mode_label.setText(f"Onbekend")
            self.details_label.setText("")