"""Class to change the plot with one with a good legend."""

import pyqtgraph as pg
from ..pg_overrides.legend import Legend

class Plot(pg.PlotItem):
    """Plot with new legend."""

    def addLegend(self, size=None, offset=(30, 30), text_size='10pt'):
        """
        Create a new LegendItem and anchor it over the internal ViewBox.
        Plots will be automatically displayed in the legend if they
        are created with the 'name' argument.
        """
        self.legend = Legend(size, offset, text_size)
        self.legend.setParentItem(self.vb)
        return self.legend