"""This module handles the different scenarios."""

class ScenarioHandler():
    """This object will handle the different scenarios."""
    def __init__(self, plotWidget, summary_label):

        self.scenario_list = []
        self.curr_scen = 0
        self.plot_widget = plotWidget
        self.summary_label = summary_label
    
    def set_current_scenario(self, ind):
        """Update which scenario is selected and the plot/label accordingly."""
        if 0 <= ind < len(self.scenario_list):
            self.curr_scen = ind
            self.update_plot()
            self.update_text()
        else:
            raise ValueError(f"'Ind' should be larger than or equal to 0" 
                             f"and not be larger than '{self.scenario_list - 1}'. It was '{ind}'")
    
    def update_plot(self):
        """Update the plot to match with the selected scenario."""
        self.scenario_list[self.curr_scen].plot_scenario(self.plot_widget)

    def update_text(self):
        """Update the summary text to match with the selected scenario."""
        self.scenario_list[self.curr_scen].summary_scenario(self.summary_label)

    def add_scenario(self, scenario):
        """Add a scenario to the handler."""
        self.scenario_list.append(scenario)
    
    def get_current_scenario(self):
        """Return the currently selected scenario."""
        return self.scenario_list[self.curr_scen]
        