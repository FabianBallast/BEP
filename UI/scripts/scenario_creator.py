# -*- coding: utf-8 -*-

from scenario_handler import scenario_handler
from scenario import scenario
import numpy as np

class scenario_creator():
    def __init__(self, plotWidget, summary_label):

        self.handler = scenario_handler(plotWidget, summary_label)

        self.steps = 1000

        self.create_scenario_1()
        self.create_scenario_2()
        self.create_scenario_3()
        self.create_scenario_4()
        self.create_scenario_5()

    def get_scenario_list(self):
        return self.handler.scenario_list
    
    def update_current_scenario(self, ind):
        self.handler.set_current_scenario(ind)
    
    def get_current_scenario(self):
        return self.handler.get_current_scenario()
    
    def create_scenario_1(self):
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
                graph_demand.append(amp_dem * np.cos(omega_dem * graph_t[i]) - amp_dem + offset_dem)
            elif graph_t[i] >= 16:
                graph_demand.append(-1 * amp_dem * np.cos(omega_dem * graph_t[i]) + 1 * amp_dem + offset_dem)
            else:
                graph_demand.append(offset_dem)

        scen = scenario(title, summary, graph_sol, graph_wind, graph_demand, graph_t)
        self.handler.add_scenario(scen)
    
    def create_scenario_2(self):
        title = 'Jaarcyclus'
        summary = "Dit is een simulatie van het gemiddelde jaar. Tijdens de verschillende seizoenen verandert zowel de productie als de vraag naar energie. "
        graph_t = np.linspace(0, 365, self.steps)

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

        scen = scenario(title, summary, graph_sol, graph_wind, graph_demand, graph_t)
        self.handler.add_scenario(scen)
    
    def create_scenario_3(self):
        title = 'Waterstof opslaan'
        summary = "Deze modus probeert de waterstoftank zo snel mogelijk op te slaan."
        graph_sol = [5, 5, 5, 5]
        graph_wind = [5, 5, 5, 5]
        graph_demand = [0, 0, 0, 0]
        graph_t = [1, 2, 3, 4]

        scen = scenario(title, summary, graph_sol, graph_wind, graph_demand, graph_t)
        self.handler.add_scenario(scen)
    
    def create_scenario_4(self):
        title = 'Waterstof gebruiken'
        summary = "Deze modus probeert de waterstoftank zo snel mogelijk leeg te laten lopen."
        graph_sol = [0, 0, 0, 0]
        graph_wind = [0, 0, 0, 0]
        graph_demand = [5, 5, 5, 5]
        graph_t = [1, 2, 3, 4]

        scen = scenario(title, summary, graph_sol, graph_wind, graph_demand, graph_t)
        self.handler.add_scenario(scen)
    
    def create_scenario_5(self):
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

        scen = scenario(title, summary, graph_sol, graph_wind, graph_demand, graph_t)
        self.handler.add_scenario(scen)
