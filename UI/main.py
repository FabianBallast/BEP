"""This module is the main part of the UI.
   It handles all windows and pages."""
from PyQt5 import QtCore, QtWidgets

from src.src.map.map_layout import MapLayout
from src.src.graphs.graph_layout import GraphLayout
from src.src.scenarios.scenario_layout import ScenarioLayout
from src.src.manual.manual_layout import ManualLayout
from src.src.data.data_manager import DataManager
from src.src.toolbar.toolbars import ToolBarTop, ToolBarBottom
from src.src.help.help_layout import HelpLayout
from src.src.second_screen.second_screen_controller import SecondScreenController
from src.src.figures.figures import Figures
import src.style.style_sheets as sheet

class UiMainWindow(object):
    """Class for both screens (if there are two screens connected)."""
    def __init__(self, geometry_1, geometry_2, main_window_1, main_window_2):

        self.data = DataManager()
        self.set_main_windows(geometry_1, geometry_2, main_window_1, main_window_2)
        self.add_toolbars_to_window(geometry_1, main_window_1)
        self.create_central_stacked_widgets(geometry_1, geometry_2, main_window_1, main_window_2)
        self.create_pages(main_window_1, main_window_2)
        self.connect_special_actions()
        self.connect_pages_to_buttons()

    def set_main_windows(self, geometry_1, geometry_2, main_window_1, main_window_2):
        """Change the main windows to the desired format and settings."""
        main_window_1.resize(geometry_1[0], geometry_1[1])
        main_window_1.setWindowTitle("User Interface 1")
        main_window_1.setStyleSheet(sheet.WINDOW_1)

        main_window_2.resize(geometry_2[0], geometry_2[1])
        main_window_2.setWindowTitle("User Interface 2")
        main_window_2.setStyleSheet(sheet.WINDOW_2)

    def add_toolbars_to_window(self, geometry, main_window):
        """Add the toolbars to the main window."""
        self.toolbar_top = ToolBarTop(geometry[1])
        main_window.addToolBar(self.toolbar_top)
        self.toolbar_bottom = ToolBarBottom(geometry[0], geometry[1], self.data)
        main_window.addToolBar(QtCore.Qt.BottomToolBarArea, self.toolbar_bottom)
    
    def create_central_stacked_widgets(self, geometry_1, geometry_2, main_window_1, main_window_2):
        """Create the central and stacked widgets and add them to the windows."""
        height = geometry_1[1] - self.toolbar_top.height() - self.toolbar_bottom.height()
        central_widget_1 = QtWidgets.QWidget(main_window_1)
        central_widget_1.setGeometry(QtCore.QRect(0, 0, geometry_1[0], height))
        self.stacked_widget_1 = QtWidgets.QStackedWidget(central_widget_1)
        self.stacked_widget_1.setGeometry(QtCore.QRect(0, 0, geometry_1[0], height))
        main_window_1.setCentralWidget(central_widget_1)

        central_widget_2 = QtWidgets.QWidget(main_window_2)
        central_widget_2.setGeometry(QtCore.QRect(0, 0, geometry_2[0], geometry_2[1]))
        self.stacked_widget_2 = QtWidgets.QStackedWidget(central_widget_2)
        self.stacked_widget_2.setGeometry(QtCore.QRect(0, 0, geometry_2[0], geometry_2[1]))
        main_window_2.setCentralWidget(central_widget_2)

        
    
    def create_pages(self, main_window_1, main_window_2):
        """Create the different pages for both screens."""
        self.graphs_1 = GraphLayout(main_window_1, 1, self.stacked_widget_1)
        self.map_1 = MapLayout(main_window_1, self.stacked_widget_1) 
        self.scenarios = ScenarioLayout(self.data, main_window_1, self.stacked_widget_1)
        self.manual_control = ManualLayout(self.data, main_window_1, self.stacked_widget_1)
        self.help_page = HelpLayout(self.data, self.stacked_widget_1)
        self.second_screen = SecondScreenController(self.stacked_widget_1)
        self.figures = Figures(self.stacked_widget_1)

        self.stacked_widget_1.addWidget(self.graphs_1)
        self.stacked_widget_1.addWidget(self.map_1)
        self.stacked_widget_1.addWidget(self.scenarios)
        self.stacked_widget_1.addWidget(self.manual_control)
        self.stacked_widget_1.addWidget(self.help_page)
        self.stacked_widget_1.addWidget(self.second_screen)
        self.stacked_widget_1.addWidget(self.figures)
        self.stacked_widget_1.setCurrentIndex(4)

        self.graphs_2 = GraphLayout(main_window_2, 2, self.stacked_widget_2)
        self.map_2 = MapLayout(main_window_2, self.stacked_widget_2)
        self.stacked_widget_2.addWidget(self.graphs_2)
        self.stacked_widget_2.addWidget(self.map_2)
    
    def connect_special_actions(self):
        """Connect specific actions to each other."""
        self.second_screen.accept_button.clicked.connect(self.change_screen)
        
        self.graphs_1.updater(self.graphs_2.update_graph_2)
        self.toolbar_bottom.exit_button.triggered.connect(self.close_app)
        
        self.data.connect_for_mode_change(self.toolbar_bottom.update_text)
        self.data.connect_for_sensor_readings(self.map_1.get_current_values)
        self.data.connect_for_sensor_readings(self.graphs_1.update_graph_1)
        self.data.connect_for_control_values(self.figures.update_input)
        self.data.connect_for_sensor_readings(self.figures.update_system)
        self.graphs_1.reset_button.clicked.connect(self.data.time_running.restart)


    def connect_pages_to_buttons(self):   
        """Connect the buttons from the toolbar to change page."""
        self.toolbar_top.graphs_button.triggered.connect(lambda: self.stacked_widget_1.setCurrentIndex(0))              #pylint: disable=C0301
        self.toolbar_top.map_button.triggered.connect(lambda: self.stacked_widget_1.setCurrentIndex(1))                 #pylint: disable=C0301
        self.toolbar_top.scenario_button.triggered.connect(lambda: self.stacked_widget_1.setCurrentIndex(2))            #pylint: disable=C0301  
        self.toolbar_top.manual_control_button.triggered.connect(lambda: self.stacked_widget_1.setCurrentIndex(3))      #pylint: disable=C0301
        self.toolbar_top.help_button.triggered.connect(lambda: self.stacked_widget_1.setCurrentIndex(4))                #pylint: disable=C0301
        self.toolbar_top.screen_button.triggered.connect(lambda: self.stacked_widget_1.setCurrentIndex(5))              #pylint: disable=C0301
        self.toolbar_top.figure_button.triggered.connect(lambda: self.stacked_widget_1.setCurrentIndex(6))              #pylint: disable=C0301

    def change_screen(self):
        """Change the page on the second screen."""
        self.stacked_widget_2.setCurrentIndex(self.second_screen.get_selected_item())
    
    def close_app(self):
        """Close app when button is pressed."""
        reply = QtWidgets.QMessageBox.warning(
            self.stacked_widget_1, 
            "Exit Application", 
            "Wil je afsluiten?", 
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, 
            QtWidgets.QMessageBox.No
        )

        if reply == QtWidgets.QMessageBox.Yes:
            sys.exit()
    

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    desktop = app.desktop()
    screen = desktop.screenCount()

    monitor_1 = QtWidgets.QDesktopWidget().screenGeometry(0)
    monitor_2 = QtWidgets.QDesktopWidget().screenGeometry(1)
    MainWindow_1 = QtWidgets.QMainWindow()
    MainWindow_2 = QtWidgets.QMainWindow()
    
    ui = UiMainWindow([monitor_1.width(), monitor_1.height()], 
                      [monitor_2.width(), monitor_2.height()],
                      MainWindow_1, MainWindow_2)
 
    MainWindow_1.showFullScreen()
    
    if screen == 2:
        MainWindow_2.move(monitor_2.left(), monitor_2.top())
        MainWindow_2.showFullScreen()
    
    sys.exit(app.exec_())
