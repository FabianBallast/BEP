# -*- coding: utf-8 -*-

class DataManager():

    def __init__(self):
        self.mode = ''
        self.scenario = ''
        self.manual = [0, 0, 0]

        self.scenario_list = []

        self.handlers = []
        self.scenarios = []

    def setData(self, mode, mode_details):
        self.mode = mode

        if mode == 'manual':
            self.manual = mode_details
        elif mode == 'scenario':
            self.scenario = mode_details
        elif mode ==  'stop' or mode == 'pause':
            pass
        else:
            raise ValueError(f"Mode should be either 'manual', 'scenario', 'stop' or 'pause', but was equal to '{mode}'")
        
        self.data_changed()
    
    def get_data(self):

        if self.mode == 'manual':
            return self.mode, self.manual
        elif self.mode == 'scenario':
            return self.mode, self.scenario
        else: 
            return self.mode, None

    def data_changed(self):
        for handler in self.handlers:
            handler() 
    
    def connect(self, handler):
        self.handlers.append(handler)
    
    def add_scenarios(self, scenarios):
        self.scenarios = scenarios
