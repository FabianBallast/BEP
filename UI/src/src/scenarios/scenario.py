"""This module handles everything for a single scenario."""
import pyqtgraph as pg

class Scenario():
    """This class represents a scenario."""

    def __init__(self, name, summary, data):

        self.name = name
        self.summary = summary
        self.time = data[0]
        self.solar = data[1]
        self.wind = data[2]
        self.demand = data[3]
    
    def get_name(self):
        """Return the name of this scenario."""
        return self.name
    
    def plot_scenario(self, plot_widget):
        """Plot this scenario in the passed widget."""
        plot_widget.clear()
        plot_widget.getLegend().clearLegend()
        plot_widget.plot(self.time, self.solar, pen=pg.mkPen('w', width=2), name="Zon")
        plot_widget.plot(self.time, self.wind, pen=pg.mkPen('r', width=2), name="Wind")
        plot_widget.plot(self.time, self.demand, pen=pg.mkPen('y', width=2), name="Vraag")
    
    def get_length(self):
        """Return the length of the arrays of this scenario."""
        return len(self.solar)
    
    def get_graphs(self):
        """Return the different arrays for solar, wind en demand."""
        return self.solar, self.wind, self.demand
    
    def summary_scenario(self, label):
        """Changes the text of the label to the summary of this scenario."""
        label.setText(self.summary)
    
    def __str__(self):
        return self.name
        