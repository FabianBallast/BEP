"""This class overrides some functions for a nice legend and graph."""

import pyqtgraph as pg
from pyqtgraph.graphicsItems.LegendItem import ItemSample
from PyQt5 import QtCore, QtGui

class Legend(pg.LegendItem):
    """Class to make the legend more flexible. """
    def __init__(self, size=None, offset=None, text_size='10pt'):
        pg.GraphicsWidget.__init__(self)
        pg.GraphicsWidgetAnchor.__init__(self)
        self.setFlag(self.ItemIgnoresTransformations)
        self.layout = QtGui.QGraphicsGridLayout()
        self.setLayout(self.layout)
        self.items = []
        self.size = size
        self.offset = offset
        self.text_size = text_size
        if size is not None:
            self.setGeometry(QtCore.QRectF(0, 0, self.size[0], self.size[1]))
    
    def addItem(self, item, name):
        """Added size variable to funtion."""
        label = pg.LabelItem(name, color=(255, 255, 255), justify='left', size=self.text_size)
        if isinstance(item, ItemSample):
            sample = item
        else:
            sample = ItemSample(item)        
        row = self.layout.rowCount()
        self.items.append((sample, label))
        self.layout.addItem(sample, row, 0)
        self.layout.addItem(label, row, 1)
        self.updateSize()



