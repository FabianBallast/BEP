"""This module deals with the figures page of the UI."""

from PyQt5 import QtCore, QtWidgets, QtGui
import pyqtgraph as pg
import numpy as np
from random import randint
from time import time

millis = lambda: int(round(time() * 1000))

class MyArrowItem(pg.ArrowItem):
    def paint(self, p, *args):
        p.translate(-self.boundingRect().center())
        pg.ArrowItem.paint(self, p, *args)

class System(QtWidgets.QWidget):
    """This class inherits from a QWidget.
       It contains all components on the 'figures' page."""

    def __init__(self, parent, preview_version=False):
        super().__init__(parent)

        self.update_i  = 0
        self.curves = []
        self.animations = []
        self.viewBoxes = []
        self.arrows = []
        self.preview = preview_version

        self.create_fonts(parent.height())   
        self.create_source_text(parent.width(), parent.height())
        self.create_hydrogen_text(parent.width(), parent.height())
        self.create_load_text(parent.width(), parent.height())
        self.create_arrows(parent, parent.width(), parent.height())



    def create_arrow(self, angle, row, col, center=False):
        """"Create arrow."""
        vb1 = self.pw2.addViewBox(row=row, col=col, enableMouse=False)
        vb1.setBackgroundColor(None)
        vb1.setAutoPan(False, False)
        if center:
            arrow_right = MyArrowItem(angle=angle, tipAngle=60, tailLen=80,tailWidth=40, headLen=80, pen=None, brush='fc0303')
        else:
            arrow_right = pg.ArrowItem(angle=angle, tipAngle=60, tailLen=80,tailWidth=40, headLen=80, pen=None, brush='fc0303')
        vb1.addItem(arrow_right)
        vb1.setRange(xRange=(-10,10),yRange=(-10,10))

        return arrow_right
    
    def create_anim_arrow1(self):       #ledloads
        """Create moving arrow 1."""
        direction = np.array([[1],[0]])
        zero      = np.array([[0],[7]])
        t         = np.array([[-2.5,4]])
        curv = zero + direction.dot(t)
        return self.create_arrow(curv, 0, 1)

    def create_anim_arrow2(self):   #fuel cell
        """Create moving arrow 2."""
        direction = np.array([[1],[2]])
        zero      = np.array([[4],[-4]])
        t         = np.array([[-0.1,4.6]])
        curv = zero + direction.dot(t)
        return self.create_arrow(curv, 1, 2)
    
    def create_anim_arrow3(self):  #electrolyzer
        """Create moving arrow 3."""
        direction = np.array([[1], [-2]])
        zero      = np.array([[-3], [-3]])
        t         = np.array([[-2.7, 1.5]])
        curv = zero + direction.dot(t)
        return self.create_arrow(curv, 1, 0)

    def create_arrow(self, curv, row, col):
        """"Create all the arrows."""
        self.curves.append(pg.PlotCurveItem(x=curv[0], y=curv[1]))
        self.arrows.append(pg.CurveArrow(self.curves[-1]))
        self.arrows[-1].setStyle(tipAngle=60, tailLen=20,tailWidth=10, headLen=20, pen=None, brush='fc0303')
        
        self.vb.addItem(self.arrows[-1])
        self.animations.append(self.arrows[-1].makeAnimation(loop=-1))
        self.animations[-1].setDuration(1000)
        if not self.preview:
            self.animations[-1].start()
       
        return len(self.arrows)-1

    def create_arrows(self,parent,width, height):
        """Create the arrows."""
        self.pw2 = pg.GraphicsLayoutWidget(self)
        self.pw2.setGeometry(QtCore.QRect(0, 0, width, height))
        self.pw2.setBackground(None)

        self.vb = self.pw2.addViewBox(enableMouse=False)
        self.vb.setBackgroundColor(None)
        self.vb.setAutoPan(False,False)
        
        self.vb.setRange(xRange=(-10,10),yRange=(-10,10))

        self.arrow_ledloads = self.create_anim_arrow1()
        self.arrow_fuelcell = self.create_anim_arrow2()
        self.arrow_electrolyzer = self.create_anim_arrow3()

        #self.label1 = self.pw2.addLabel("",row=0,col=0, color='ffffff',size='20pt')
        #self.label2 = self.pw2.addLabel("", row=0,col=2, color='ffffff',size='20pt')
        #self.label3 = self.pw2.addLabel("", row=1,col=1, color='ffffff',size='20pt')
    

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
        self.load_figures_curr.setGeometry(QtCore.QRect(int(width * 0.80), int(height * 0.10),
                                                        int(width * 0.08), int(height * 0.15)))
        self.load_figures_curr.setAlignment(QtCore.Qt.AlignTop|QtCore.Qt.AlignRight)

        self.load_figures_per = QtWidgets.QLabel(self)
        self.load_figures_per.setFont(self.text_font)
        self.load_figures_per.setText("0%\n0%")
        self.load_figures_per.setGeometry(QtCore.QRect(int(width * 0.87), int(height * 0.10),
                                                       int(width * 0.10), int(height * 0.15)))
        self.load_figures_per.setAlignment(QtCore.Qt.AlignTop|QtCore.Qt.AlignRight)
    
    def setArrow(self, arrowIndex, val):
        self.arrows[arrowIndex].setStyle(tipAngle=60, tailLen=20*val,tailWidth=10*val, headLen=20*val, pen=None, brush='fc0303')

    def update_text(self, input_data, sensor_data):
        """Update the text."""
        solar = sensor_data.get('zonPower')
        wind = sensor_data.get('windPower')
        load = sensor_data.get('loadPower')
        elek = solar + wind - load  +sensor_data.get('curr_to_add')     #sensor_data.get('flowTot')

        tank = sensor_data.get('tank_level')
        
        self.source_figures_curr.setText(f"{solar:.2f} \n{wind:.2f} ")
        self.source_figures_per.setText(f"{input_data[0]:.1f}%\n{input_data[1]:.1f}%")
        self.hydrogen_figures.setText(f"{elek:.2f} \n{tank:.2f}%")
        self.load_figures_curr.setText(f"{load:.2f} \n0.00 ")
        self.load_figures_per.setText(f"{input_data[2]:.1f}%\n0.0%")
        
        # self.update_i+=1
        # if self.update_i > 10:
        #     self.update_i = 0
        self.arrows[self.arrow_electrolyzer].setStyle()
        if elek>0:
            self.arrows[self.arrow_fuelcell].hide()
            self.arrows[self.arrow_electrolyzer].show()

            self.setArrow(self.arrow_electrolyzer, abs(elek))
            self.setArrow(self.arrow_ledloads, abs(load))

        elif elek<0:
            self.arrows[self.arrow_electrolyzer].hide()
            self.arrows[self.arrow_fuelcell].show()

            self.setArrow(self.arrow_fuelcell, abs(elek))
            self.setArrow(self.arrow_ledloads, abs(solar+wind))
        
        
        
        # currTime = millis()
        # if currTime - self.lastTimeE > 1000:
        #     self.lastTimeE = currTime
        #     if elek>0:
        #         self.arrow_fuelcell.hide()
        #         self.arrow_electrolyzer.show()
        #         self.anim_electrolyzer.setDuration(4000/abs(elek))
        #         if load>0:
        #             self.anim_ledloads.setDuration(4000/abs(load))
        #     elif elek<0:
        #         self.arrow_electrolyzer.hide()
        #         self.arrow_fuelcell.show()
        #         self.anim_fuelcell.setDuration(4000/abs(elek))
        #         self.anim_ledloads.setDuration(4000/abs(solar+wind))
        
        
        
        # if elek>0:
        #     self.arrow_fuelcell.hide()
        #     self.arrow_electrolyzer.show()
        #     if currTime - self.lastTimeE >= self.animTimeE:
        #         self.animTimeE = 4000/abs(elek)
        #         self.anim_electrolyzer.setDuration(self.animTimeE)
        #         self.lastTimeE = millis()
        #     if currTime - self.lastTimeL >= self.animTimeL:
        #         if load>0:
        #             self.animTimeL = 4000/abs(load)
        #             self.anim_ledloads.setDuration(self.animTimeL)
        #             self.lastTimeL = millis()

        # elif elek<0:
        #     self.arrow_electrolyzer.hide()
        #     self.arrow_fuelcell.show()
            
        #     if currTime - self.lastTimeF >= self.animTimeF:
        #         self.animTimeF = 4000/abs(elek)
        #         self.anim_fuelcell.setDuration(self.animTimeF)
        #         self.lastTimeF = millis()
        #     if currTime - self.lastTimeL >= self.animTimeL:
        #         self.animTimeL = 4000/abs(solar+wind)
        #         self.anim_ledloads.setDuration(self.animTimeL)
        #         self.lastTimeL = millis()    

        # if self.animTimeF > 2000:   self.animTimeF = 2000
        # if self.animTimeL > 2000:   self.animTimeL = 2000
        # if self.animTimeE > 2000:   self.animTimeE = 2000
