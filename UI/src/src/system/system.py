"""This module deals with the figures page of the UI."""

from PyQt5 import QtCore, QtWidgets, QtGui
import pyqtgraph as pg

class MyArrowItem(pg.ArrowItem):
    def paint(self, p, *args):
        p.translate(-self.boundingRect().center())
        pg.ArrowItem.paint(self, p, *args)

class System(QtWidgets.QWidget):
    """This class inherits from a QWidget.
       It contains all components on the 'figures' page."""

    def __init__(self, parent):
        super().__init__(parent)
        self.create_fonts(parent.height())   
        self.create_source_text(parent.width(), parent.height())
        self.create_hydrogen_text(parent.width(), parent.height())
        self.create_load_text(parent.width(), parent.height())
        self.create_arrows(parent, parent.width(), parent.height())

    def create_arrow(self,angle,row,col, center=False):
        vb1 = self.pw2.addViewBox(row=row,col=col, enableMouse=False)
        vb1.setBackgroundColor(None)
        vb1.setAutoPan(False,False)
        if center:
            arrow_right = MyArrowItem(angle=angle, tipAngle=60, tailLen=40,tailWidth=20, headLen=40, pen=None, brush='b')
        else:
            arrow_right = pg.ArrowItem(angle=angle, tipAngle=60, tailLen=40,tailWidth=20, headLen=40, pen=None, brush='b')


        vb1.addItem(arrow_right)
        vb1.setRange(xRange=(-10,10),yRange=(-10,10))
    
        return arrow_right

    def create_arrows(self,parent,width, height):
        self.pw2 = pg.GraphicsLayoutWidget(self)
        self.pw2.setGeometry(QtCore.QRect(0,int(height*0.1), int(width*0.5), int(height*0.3)))
        self.pw2.setBackground(None)

        self.arrow1 = self.create_arrow(225,1,0, True)
        self.arrow1.setPos(7,7)
        self.arrow2 = self.create_arrow(135,1,2, True)
        self.arrow2.setPos(-7,7)
        self.arrow3 = self.create_arrow(180,0,1, center=True)

        self.label1 = self.pw2.addLabel("Energie-opbrengst",row=0,col=0, color='ffffff',size='20pt')
        self.label2 = self.pw2.addLabel("Waterstofsysteem", row=0,col=2, color='ffffff',size='20pt')
        self.label3 = self.pw2.addLabel("Energie-verbruik", row=1,col=1, color='ffffff',size='20pt')
    
    def create_fonts(self, height):
        """Create the fonts used for the figures."""
        self.text_font = QtGui.QFont()
        self.text_font.setPixelSize(int(height * 0.05))
    
    def create_source_text(self, width, height):
        """Create the text and values for the sources."""
        self.source_text = QtWidgets.QLabel(self)
        self.source_text.setFont(self.text_font)
        self.source_text.setText("Zon:\nWind:")
        self.source_text.setGeometry(QtCore.QRect(int(width * 0.05), int(height * 0.10),
                                                  int(width * 0.10), int(height * 0.15)))
        self.source_text.setAlignment(QtCore.Qt.AlignTop|QtCore.Qt.AlignRight)

        self.source_figures_curr = QtWidgets.QLabel(self)
        self.source_figures_curr.setFont(self.text_font)
        self.source_figures_curr.setText("0W\n0W")
        self.source_figures_curr.setGeometry(QtCore.QRect(int(width * 0.155), int(height * 0.10),
                                                          int(width * 0.07), int(height * 0.15)))
        self.source_figures_curr.setAlignment(QtCore.Qt.AlignTop)

        self.source_figures_per = QtWidgets.QLabel(self)
        self.source_figures_per.setFont(self.text_font)
        self.source_figures_per.setText("0W\n0W")
        self.source_figures_per.setGeometry(QtCore.QRect(int(width * 0.20), int(height * 0.10),
                                                         int(width * 0.10), int(height * 0.15)))
        self.source_figures_per.setAlignment(QtCore.Qt.AlignTop|QtCore.Qt.AlignRight)
    
    def create_hydrogen_text(self, width, height):
        """Create the text for the hydrogen text."""
        self.hydrogen_text = QtWidgets.QLabel(self)
        self.hydrogen_text.setFont(self.text_font)
        self.hydrogen_text.setText("Balans:\nOpslag:")
        self.hydrogen_text.setGeometry(QtCore.QRect(int(width * 0.415), int(height * 0.70),
                                                    int(width * 0.10), int(height * 0.15)))
        self.hydrogen_text.setAlignment(QtCore.Qt.AlignTop|QtCore.Qt.AlignRight)

        self.hydrogen_figures = QtWidgets.QLabel(self)
        self.hydrogen_figures.setFont(self.text_font)
        self.hydrogen_figures.setText("0W\n50%")
        self.hydrogen_figures.setGeometry(QtCore.QRect(int(width * 0.505), int(height * 0.70),
                                                       int(width * 0.10), int(height * 0.15)))
        self.hydrogen_figures.setAlignment(QtCore.Qt.AlignTop|QtCore.Qt.AlignRight)
    
    def create_load_text(self, width, height):
        """Create text for the loads"""
        self.load_text = QtWidgets.QLabel(self)
        self.load_text.setFont(self.text_font)
        self.load_text.setText("Huizen:\nIndustrie:")
        self.load_text.setGeometry(QtCore.QRect(int(width * 0.70), int(height * 0.10),
                                                int(width * 0.10), int(height * 0.15)))
        self.load_text.setAlignment(QtCore.Qt.AlignTop|QtCore.Qt.AlignRight)

        self.load_figures_curr = QtWidgets.QLabel(self)
        self.load_figures_curr.setFont(self.text_font)
        self.load_figures_curr.setText("0W\n0W")
        self.load_figures_curr.setGeometry(QtCore.QRect(int(width * 0.75), int(height * 0.10),
                                                        int(width * 0.08), int(height * 0.15)))
        self.load_figures_curr.setAlignment(QtCore.Qt.AlignTop|QtCore.Qt.AlignRight)

        self.load_figures_per = QtWidgets.QLabel(self)
        self.load_figures_per.setFont(self.text_font)
        self.load_figures_per.setText("0%\n0%")
        self.load_figures_per.setGeometry(QtCore.QRect(int(width * 0.85), int(height * 0.10),
                                                       int(width * 0.10), int(height * 0.15)))
        self.load_figures_per.setAlignment(QtCore.Qt.AlignTop|QtCore.Qt.AlignRight)
    
    def update_text(self, input_data, sensor_data):
        """Update the text."""
        self.source_figures_curr.setText(f"{(sensor_data[0]/20):.2f}W\n{(sensor_data[1]/20):.2f}W")
        self.source_figures_per.setText(f"{input_data[0]:.1f}%\n{input_data[1]:.1f}%")
        self.hydrogen_figures.setText(f"{((sensor_data[0] + sensor_data[1] - sensor_data[2])/20):.2f}W\n{sensor_data[3]:.2f}%")
        self.load_figures_curr.setText(f"{(sensor_data[2]/20):.2f}W\n0.00W")
        self.load_figures_per.setText(f"{input_data[2]:.1f}%\n0.0%")
        
        print('eijfiej')
        self.arrow1.prepareGeometryChange()
        self.arrow1.setStyle(tailWidth=randint(0, 40))
        self.arrow2.setStyle(tailWidth=randint(0, 40))
        self.arrow3.setStyle(tailWidth=randint(0, 40))
