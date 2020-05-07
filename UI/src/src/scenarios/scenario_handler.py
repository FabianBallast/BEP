# -*- coding: utf-8 -*-

class scenario_handler():

    def __init__(self, plotWidget, summary_label):

        self.scenario_list = []
        self.curr_scen = 0
        self.plotWidget = plotWidget
        self.summary_label = summary_label
    
    def set_current_scenario(self, ind):

        if 0 <= ind < len(self.scenario_list):
            self.curr_scen = ind
            self.update_plot()
            self.update_text()
        else:
            raise ValueError(f"'Ind' should be larger than or equal to 0 and not be larger than '{self.scenario_list - 1}'. It was '{ind}'")
    
    def update_plot(self):
        self.scenario_list[self.curr_scen].plot_scenario(self.plotWidget)

    def update_text(self):
        self.scenario_list[self.curr_scen].summary_scenario(self.summary_label)

    def add_scenario(self, scenario):
        self.scenario_list.append(scenario)
    
    def get_current_scenario(self):
        return self.scenario_list[self.curr_scen]