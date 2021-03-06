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
        self.diff = []

    
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

        self.diff = []
        for i in range(len(self.wind)):
            self.diff.append(self.solar[i] + self.wind[i] - self.demand[i])

        plot_widget.plot(self.time, self.diff, pen=pg.mkPen('g', width=2), name="Netto")
    
    def get_length(self):
        """Return the length of the arrays of this scenario."""
        return len(self.solar)
    
    def get_graphs(self):
        """Return the different arrays for solar, wind en demand."""
        return self.solar, self.wind, self.demand
    
    def get_values_at(self, time):
        """Return the values from the scenario from a given time."""
        time_end = self.time[-1]
        frac = time / time_end
        ind_raw = int((frac - round(frac, 0)) * (len(self.time) - 1))
        ind = ind_raw

        all_data = [self.solar, self.wind, self.demand]
        val_raw = [mode[ind] for mode in all_data]

        final_data = []
        for x in range(len(val_raw)):
            maxx = max(all_data[x])
            if maxx==0: maxx = 100
            val = round(val_raw[x] * 100 / maxx, 0)
            final_data.append(val)

        return final_data
    
    def summary_scenario(self, label):
        """Changes the text of the label to the summary of this scenario."""
        label.setText(self.summary)
    
    def __str__(self):
        return self.name
        