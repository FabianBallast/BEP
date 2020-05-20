"""This module is focused on creating the different scenarios."""

import numpy as np
import xlrd
import xlwt
from ..scenarios.scenario_handler import ScenarioHandler
from ..scenarios.scenario import Scenario


class ScenarioCreator():
    """This object creates all different scenarios and adds them to the scenario handler."""
    def __init__(self, plotWidget, summary_label):

        self.handler = ScenarioHandler(plotWidget, summary_label)

        self.steps = 250
        self.scenario_file = 'UI/scenarios.xlsx'

        #self.create_scenarios()

        self.create_scenario_1()
        self.create_scenario_2()
        #self.create_scenario_3()
        #self.create_scenario_4()
        #self.create_scenario_5()

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
        wb = xlrd.open_workbook(self.scenario_file) 
        sheet = wb.sheet_by_index(0)

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

    def create_scenario_1(self):
        """Create the first scenario: the day-night cycle."""

        
        title = 'Dag-nachtcyclus'
        summary = 'Dit is een simulatie van een gemiddelde dag.'
        graph_t = np.linspace(0, 24, self.steps)

        omega_sol = np.pi * 4 / 24
        amp_sol = 2

        omega_wind = np.pi * 2 / 24
        amp_wind = 0.5
        offset_wind = 1.5

        omega_dem = np.pi * 6 / 24
        amp_dem = 1
        offset_dem = 2.5

        graph_sol = []
        graph_wind = []
        graph_demand = []

        for i in range(self.steps):

            if graph_t[i] >= 6 and graph_t[i] < 18:
                graph_sol.append(amp_sol * np.cos(omega_sol * graph_t[i]) + amp_sol)
            else:
                graph_sol.append(0)
            
            graph_wind.append(amp_wind * np.cos(omega_wind * graph_t[i]) + amp_wind + offset_wind)

            if graph_t[i] <= 8:
                graph_demand.append(amp_dem * np.cos(omega_dem * graph_t[i]) - amp_dem + offset_dem)           #pylint: disable=C0301
            elif graph_t[i] >= 16:
                graph_demand.append(-1 * amp_dem * np.cos(omega_dem * graph_t[i]) + 1 * amp_dem + offset_dem)  #pylint: disable=C0301
            else:
                graph_demand.append(offset_dem)
        
        
        scen = Scenario(title, summary, [graph_t, graph_sol, graph_wind, graph_demand])
        self.handler.add_scenario(scen)
    
    def create_scenario_2(self):
        """Create the second scenario: the year cycle."""
        title = 'Jaarcyclus'
        summary = """Dit is een simulatie van het gemiddelde jaar.
                     Tijdens de verschillende seizoenen verandert
                     zowel de productie als de vraag naar energie."""
        graph_t = np.linspace(0, 365, self.steps)
        wb = xlwt.Workbook()
        sheet = wb.add_sheet('values')

        omega_sol = 2 * np.pi / 365
        amp_sol = 2
        offset_sol = 1

        omega_wind = 2 * np.pi * 4 / 365
        amp_wind = 0.5
        offset_wind = 3

        graph_sol = []
        graph_wind = []
        graph_demand = []

        for i in range(self.steps):

            graph_sol.append(-amp_sol * np.cos(omega_sol * graph_t[i]) + amp_sol + offset_sol)
            graph_wind.append(amp_wind * np.cos(omega_wind * graph_t[i]) + amp_wind + offset_wind)
            graph_demand.append(2.5)
        
        for index in range(len(graph_t)):
            sheet.write(0, index, graph_t[index])
            sheet.write(1, index, graph_sol[index])
            sheet.write(2, index, graph_wind[index])
            sheet.write(3, index, graph_demand[index])
        
        wb.save('UI/temp.xls')


        scen = Scenario(title, summary, [graph_t, graph_sol, graph_wind, graph_demand])
        self.handler.add_scenario(scen)
    
    def create_scenario_3(self):
        """Create the third scenario: storing hydrogen."""
        title = 'Waterstof opslaan'
        summary = "Deze modus probeert de waterstoftank zo snel mogelijk op te slaan."
        graph_sol = [5, 5, 5, 5]
        graph_wind = [5, 5, 5, 5]
        graph_demand = [0, 0, 0, 0]
        graph_t = [1, 2, 3, 4]

        scen = Scenario(title, summary, [graph_t, graph_sol, graph_wind, graph_demand])
        self.handler.add_scenario(scen)
    
    def create_scenario_4(self):
        """"Create the fourth scenario: using hydrogen."""
        title = 'Waterstof gebruiken'
        summary = "Deze modus probeert de waterstoftank zo snel mogelijk leeg te laten lopen."
        graph_sol = [0, 0, 0, 0]
        graph_wind = [0, 0, 0, 0]
        graph_demand = [5, 5, 5, 5]
        graph_t = [1, 2, 3, 4]

        scen = Scenario(title, summary, [graph_t, graph_sol, graph_wind, graph_demand])
        self.handler.add_scenario(scen)
    
    def create_scenario_5(self):
        """Create the fifth scenario: random sines."""
        title = 'Random Test Sinusoïden.'
        summary = "Deze modus heeft enkele willekeurige sinuoïden."
        graph_t = np.linspace(0, 2 * np.pi, self.steps)

        graph_sol = []
        graph_wind = []
        graph_demand = []

        for i in range(self.steps):

            graph_sol.append(1.3 * np.cos(graph_t[i]) + 1.5)
            graph_wind.append(np.sin(graph_t[i]) + 1)
            graph_demand.append(graph_sol[i] + graph_wind[i])

        scen = Scenario(title, summary, [graph_t, graph_sol, graph_wind, graph_demand])
        self.handler.add_scenario(scen)
