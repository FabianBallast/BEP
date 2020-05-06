# -*- coding: utf-8 -*-

import pyqtgraph as pg

class scenario():

    def __init__(self, name, summary, solar_data, wind_data, demand_data, time_data):

        self.name = name
        self.summary = summary
        self.time = time_data
        self.solar = solar_data
        self.wind = wind_data
        self.demand = demand_data
    
    def get_name(self):
        return self.name
    
    def plot_scenario(self, plot_widget):
        plot_widget.clear()
        plot_widget.getLegend().clearLegend()
        plot_widget.plot(self.time, self.solar, pen=pg.mkPen('w', width=2), name="Zon")
        plot_widget.plot(self.time, self.wind, pen=pg.mkPen('r', width=2), name="Wind")
        plot_widget.plot(self.time, self.demand, pen=pg.mkPen('y', width=2), name="Vraag")
    
    def get_length(self):
        return len(self.solar)
    
    def get_graphs(self):
        return self.solar, self.wind, self.demand
    
    def summary_scenario(self, label):
        label.setText(self.summary)
    
    def __str__(self):
        return self.name
        