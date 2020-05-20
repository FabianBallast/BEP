"""This module is there for an central overview of the stylesheets."""

WINDOW_1 = """QWidget {background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0             
                                                         rgba(0, 150, 100, 255), stop:1 
                                                         rgba(0, 0, 240, 255))}    
              QPushButton {background-color: rgba(0, 255, 0, 200);
                           color: rgb(255, 255, 255)}
              QPushButton::hover {background-color: rgba(0, 255, 0, 220)}
              QPushButton::pressed {background-color: rgba(0, 250, 0, 255)}  
              QCommandLinkButton {background-color: rgba(0, 0, 0, 0);
                                  color: rgb(255, 255, 255)} 
              QCommandLinkButton::hover {background-color: rgba(0, 255, 0, 80)}
              QListWidget {background-color: rgba(0, 0, 0, 0);
                           color: rgb(255, 255, 255); border: none}
              QLabel {background-color: rgba(0, 0, 0, 0);
                      color: rgb(255, 255, 255)}
              QSlider {background-color: rgba(255, 255, 255, 0)}
              QSlider::handle:vertical {
                                background: green;
                                margin: 0 -80px;
                                border: 1px solid;
                                height: 80px;
                                     }
              QSlider::groove:vertical {
                                background: yellow;
                                width: 10px;
                                margin: 0 -5px;
                                
                                     }    
              QLCDNumber {background-color: rgba(255, 255, 255, 0)}
              QCheckBox {background-color: rgba(255, 255, 255, 0);
                         color: rgb(255, 255, 255)}
              QGraphicsView {background-color: rgba(255, 255, 255, 0);
                             color: rgb(255, 255, 255)} 
              QToolButton {background-color: rgba(0, 255, 0, 0);
                           color: rgb(255, 255, 255)}
              QToolButton::hover {background-color: rgba(0, 255, 0, 50); 
                                  color: rgb(255, 255, 255)}
              QToolButton::pressed {background-color: rgba(0, 255, 0, 100);
                                    color: rgb(255, 255, 255)}
              QToolBar {background-color: rgba(0, 0, 0, 50); border: none}
              QMessageBox {background-color: rgba(255, 255, 255, 50)}
              QLineEdit {background-color: rgba(0, 0, 0, 0);
                         color: rgb(255, 255, 255); border: none}
              QTextBrowser {background-color: rgba(0, 0, 0, 0);
                            color: rgb(255, 255, 255); border: none}"""

WINDOW_2 = WINDOW_1
