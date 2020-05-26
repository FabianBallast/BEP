"""This module deals with the figures page of the UI."""

from PyQt5 import QtCore, QtWidgets, QtGui
import pyqtgraph as pg
from numpy import linspace, cos, sin, radians
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

    def __init__(self, parent):
        super().__init__(parent)
        self.create_fonts(parent.height())   
        self.create_source_text(parent.width(), parent.height())
        self.create_hydrogen_text(parent.width(), parent.height())
        self.create_load_text(parent.width(), parent.height())
        self.create_arrows(parent, parent.width(), parent.height())

        self.lastTimeE = millis()
        self.lastTimeL = millis()
        self.lastTimeF = millis()

        self.animTimeE = 0
        self.animTimeL = 0
        self.animTimeF = 0

    def create_arrow(self,angle,row,col, center=False):
        vb1 = self.pw2.addViewBox(row=row,col=col, enableMouse=False)
        vb1.setBackgroundColor(None)
        vb1.setAutoPan(False,False)
        if center:
            arrow_right = MyArrowItem(angle=angle, tipAngle=60, tailLen=80,tailWidth=40, headLen=80, pen=None, brush='fc0303')
        else:
            arrow_right = pg.ArrowItem(angle=angle, tipAngle=60, tailLen=80,tailWidth=40, headLen=80, pen=None, brush='fc0303')
        vb1.addItem(arrow_right)
        vb1.setRange(xRange=(-10,10),yRange=(-10,10))

        # animation = QtCore.QPropertyAnimation(self.button, "geometry")
        # animation.setDuration(10000)
        # animation.setStartValue(QtCore.QRect(0,0,0,0))
        # animation.setEndValue(QtCore.QRect(0,0,200,200))
        # animation.start()

        # self.animation = animation


        return arrow_right
    
    def create_anim_arrow1(self):
        self.vb1 = self.pw2.addViewBox(row=0,col=1, enableMouse=False)
        self.vb1.setBackgroundColor(None)
        self.vb1.setAutoPan(False,False)

        x = [-7, 12]
        y = [5, 5]
        self.curve1 = pg.PlotCurveItem(x=x, y=y)
        
        self.arrow_ledloads = pg.CurveArrow(self.curve1)
        self.arrow_ledloads.setStyle(tipAngle=60, tailLen=80,tailWidth=40, headLen=80, pen=None, brush='fc0303')
        self.vb1.addItem(self.arrow_ledloads)
        self.anim_ledloads = self.arrow_ledloads.makeAnimation(loop=-1)
        self.anim_ledloads.start()
        self.vb1.setRange(xRange=(-10,10),yRange=(-10,10))
        return self.arrow_ledloads

    def create_anim_arrow2(self):
        self.vb2 = self.pw2.addViewBox(row=1,col=2, enableMouse=False)
        self.vb2.setBackgroundColor(None)
        self.vb2.setAutoPan(False,False)
        
        x = [-17, -3]
        y = [1, 13]
        self.curve2 = pg.PlotCurveItem(x=x, y=y)
        
        self.arrow_fuelcell = pg.CurveArrow(self.curve2)
        self.arrow_fuelcell.setStyle(tipAngle=60, tailLen=80,tailWidth=40, headLen=80, pen=None, brush='fc0303')
        self.vb2.addItem(self.arrow_fuelcell)
        self.anim_fuelcell = self.arrow_fuelcell.makeAnimation(loop=-1)
        self.anim_fuelcell.start()
        self.vb2.setRange(xRange=(-10,10),yRange=(-10,10))
        return self.arrow_fuelcell
    
    def create_anim_arrow3(self):
        self.vb3 = self.pw2.addViewBox(row=1,col=0, enableMouse=False)
        self.vb3.setBackgroundColor(None)
        self.vb3.setAutoPan(False,False)
        
        x = [1, 13]
        y = [10, -4]
        self.curve3 = pg.PlotCurveItem(x=x, y=y)

        self.arrow_electrolyzer = pg.CurveArrow(self.curve3)
        self.arrow_electrolyzer.setStyle(tipAngle=60, tailLen=80,tailWidth=40, headLen=80, pen=None, brush='fc0303')
        self.vb3.addItem(self.arrow_electrolyzer)
        self.anim_electrolyzer = self.arrow_electrolyzer.makeAnimation(loop=-1)
        self.anim_electrolyzer.setDuration(1000)
        self.anim_electrolyzer.start()



        self.vb3.setRange(xRange=(-10,10),yRange=(-10,10))
        return self.arrow_electrolyzer

    def create_arrows(self,parent,width, height):
        self.pw2 = pg.GraphicsLayoutWidget(self)
        self.pw2.setGeometry(QtCore.QRect(0, 0, width, height))
        self.pw2.setBackground(None)

        # self.arrow_ledloads = self.create_arrow(225,1,0, True)
        # self.arrow_ledloads.setPos(7,7)
        # self.arrow_fuelcell = self.create_arrow(135,1,2, True)
        # self.arrow_fuelcell.setPos(-7,7)
        #self.arrow_electrolyzer = self.create_arrow(180,0,1, center=True)
        self.arrow_ledloads =    self.create_anim_arrow1()
        self.arrow_fuelcell = self.create_anim_arrow2()
        self.arrow_electrolyzer        = self.create_anim_arrow3()

        self.label1 = self.pw2.addLabel("",row=0,col=0, color='ffffff',size='20pt')
        self.label2 = self.pw2.addLabel("", row=0,col=2, color='ffffff',size='20pt')
        self.label3 = self.pw2.addLabel("", row=1,col=1, color='ffffff',size='20pt')
    

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
    
    def update_text(self, input_data, sensor_data):
        """Update the text."""
        solar = sensor_data.get('solar_current')/20
        wind = sensor_data.get('wind_current')/20
        load = sensor_data.get('load_current')/20
        elek = solar + wind - load
        tank = sensor_data.get('tank_level')
        self.source_figures_curr.setText(f"{solar:.2f}W\n{wind:.2f}W")
        self.source_figures_per.setText(f"{input_data[0]:.1f}%\n{input_data[1]:.1f}%")
        self.hydrogen_figures.setText(f"{elek:.2f}W\n{tank:.2f}%")
        self.load_figures_curr.setText(f"{load:.2f}W\n0.00W")
        self.load_figures_per.setText(f"{input_data[2]:.1f}%\n0.0%")
        
        currTime = millis()
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
        
        
        
        if elek>0:
            self.arrow_fuelcell.hide()
            self.arrow_electrolyzer.show()
            if currTime - self.lastTimeE >= self.animTimeE:
                self.animTimeE = 4000/abs(elek)
                self.anim_electrolyzer.setDuration(self.animTimeE)
                self.lastTimeE = millis()
            if currTime - self.lastTimeL >= self.animTimeL:
                if load>0:
                    self.animTimeL = 4000/abs(load)
                    self.anim_ledloads.setDuration(self.animTimeL)
                    self.lastTimeL = millis()

        elif elek<0:
            self.arrow_electrolyzer.hide()
            self.arrow_fuelcell.show()
            
            if currTime - self.lastTimeF >= self.animTimeF:
                self.animTimeF = 4000/abs(elek)
                self.anim_fuelcell.setDuration(self.animTimeF)
                self.lastTimeF = millis()
            if currTime - self.lastTimeL >= self.animTimeL:
                self.animTimeL = 4000/abs(solar+wind)
                self.anim_ledloads.setDuration(self.animTimeL)
                self.lastTimeL = millis()    

        if self.animTimeF > 2000:   self.animTimeF = 2000
        if self.animTimeL > 2000:   self.animTimeL = 2000
        if self.animTimeE > 2000:   self.animTimeE = 2000
