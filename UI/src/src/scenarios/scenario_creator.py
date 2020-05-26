"""This module is focused on creating the different scenarios."""

import xlrd
from ..scenarios.scenario_handler import ScenarioHandler
from ..scenarios.scenario import Scenario


class ScenarioCreator():
    """This object creates all different scenarios and adds them to the scenario handler."""
    def __init__(self, plotWidget, summary_label):

        self.handler = ScenarioHandler(plotWidget, summary_label)

        self.steps = 250
        self.scenario_file = 'UI/scenarios.xlsx'

        self.create_scenarios()


    def get_scenario_list(self):
        """Return the scenario handler with all the scenarios."""
        return self.handler.scenario_list
    
    def update_current_scenario(self, ind):
        """Update which scenario is selected."""
        self.handler.set_current_scenario(ind)
    
    def get_current_scenario(self):
        """Return the scenario currently selected."""
        return self.handler.get_current_scenario()
    
    def create_scenarios(self):
        """Read from file and create scenarios accordingly."""
        workbook = xlrd.open_workbook(self.scenario_file) 
        sheet = workbook.sheet_by_index(0)

        curr_row = 0
        while curr_row < sheet.nrows:
            if sheet.cell_value(curr_row, 0) != '':

                name = self.find_name(sheet, curr_row)
                summary = self.find_summary(sheet, curr_row + 1)
                time = self.find_time_arr(sheet, curr_row + 2)
                solar = self.find_solar_arr(sheet, curr_row + 3)
                wind = self.find_wind_arr(sheet, curr_row + 4)
                demand = self.find_demand_arr(sheet, curr_row + 5)
                
                scen = Scenario(name, summary, [time, solar, wind, demand])
                self.handler.add_scenario(scen)

                curr_row += 6
            else:
                curr_row += 1



    def find_name(self, sheet, row):
        """Find the name of the scenario."""
        name = sheet.cell_value(row, 1)

        if name != 'Naam':
            raise ValueError(f"Expected cell named 'Naam', but found {name}")

        return sheet.cell_value(row, 2)
    
    def find_summary(self, sheet, row):
        """Find the name of the scenario."""
        summary = sheet.cell_value(row, 1)

        if summary != 'Samenvatting':
            raise ValueError(f"Expected cell named 'Samenvatting', but found {summary}")

        return sheet.cell_value(row, 2)
    
    def find_solar_arr(self, sheet, row):
        """Retrieve the solar array from the given row."""
        solar_name = sheet.cell_value(row, 1)
        solar_arr = []
        if solar_name != 'Zon':
            raise ValueError(f"Expected cell named 'Zon', but found {solar_name}")
        else:
            solar_arr = list(filter(str, sheet.row_values(row)))
            del solar_arr[0]
        
        return solar_arr

    def find_wind_arr(self, sheet, row):
        """Retrieve the solar array from the given row."""
        wind_name = sheet.cell_value(row, 1)
        wind_arr = []
        if wind_name != 'Wind':
            raise ValueError(f"Expected cell named 'Wind', but found {wind_name}")
        else:
            wind_arr = list(filter(str, sheet.row_values(row)))
            del wind_arr[0]
        
        return wind_arr
    
    def find_demand_arr(self, sheet, row):
        """Retrieve the solar array from the given row."""
        demand_name = sheet.cell_value(row, 1)
        demand_arr = []
        if demand_name != 'Vraag':
            raise ValueError(f"Expected cell named 'Vraag', but found {demand_name}")
        else:
            demand_arr = list(filter(str, sheet.row_values(row)))
            del demand_arr[0]
    
        return demand_arr
    
    def find_time_arr(self, sheet, row):
        """Retrieve the solar array from the given row."""
        time_name = sheet.cell_value(row, 1)
        time_arr = []
        if time_name != 'Tijd':
            raise ValueError(f"Expected cell named 'Tijd', but found {time_name}")
        else:
            time_arr = list(filter(str, sheet.row_values(row)))
            del time_arr[0]
        
        return time_arr
