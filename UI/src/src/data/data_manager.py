"""This module will handle all the data and the connection between the Pi and Arduino."""

class DataManager():
    """This class contains all data."""
    def __init__(self):
        self.mode = ''
        self.scenario = ''
        self.manual = [0, 0, 0]

        self.handlers = []
        self.storage_cal = 0

    def set_mode(self, mode, mode_details):
        """Update the mode in which the system is running."""
        self.mode = mode

        if mode == 'manual':
            self.manual = mode_details
        elif mode == 'scenario':
            self.scenario = mode_details
        elif mode == 'stop':
            pass
        else:
            raise ValueError(f"Mode should be either 'manual', 'scenario' or 'stop',"
                             f"but was equal to '{mode}'")
        
        self.mode_changed()
    
    def get_mode(self):
        """Update the mode."""
        if self.mode == 'manual':
            return self.mode, self.manual
        elif self.mode == 'scenario':
            return self.mode, self.scenario
        else: 
            return self.mode, None

    def mode_changed(self):
        """Execute all the connected functions."""
        for handler in self.handlers:
            handler() 
    
    def connect_for_mode_change(self, handler):
        """Add function that will be executed when the mode changes."""
        self.handlers.append(handler)
    
    def set_storage_value(self, val):
        """Update the value with the calibrated value."""
        self.storage_cal = val
