"""This class handles the sensor for reading the tank level."""

import time



Kp_grid = 20
Ki_grid = 0
Kd_grid = 0

class gridControlMultiply:

    def __init__(self):
        self.current_PS_current = 0
        self.current_error = 0
        self.prev_error = 0
        self.cum_error = 0                               #pylint: disable=invalid-name
        self.prev_time = time.time()
        self.prev_error = 0
        
    def controlPSmultiply(self, readings):
        current_to_add_target = readings['curr_to_add']
        grid_control_value = -current_to_add_target/20
        #grid_control_value = self.gridPID(current_to_add_target, readings['PS_I'])

        return grid_control_value
    
    def gridPID(self, target_current, current_current):
        newTime = time.time()
        elapsedTime = newTime - self.prev_time
        
        self.current_error = current_current - target_current
        self.cum_error += self.current_error*elapsedTime
        if abs(self.cum_error)*Ki_grid > 30:
            self.cum_error = np.sign(self.cum_error)*30/Ki_grid
        self.rate_error = (self.current_error - self.prev_error)/elapsedTime
        
        self.prev_time = newTime
        self.prev_error = self.current_error

        grid_control_value = Kp_grid* self.current_error +  Ki_grid* self.cum_error + Kd_grid* self.rate_error
            #self.printer.print("")
        return grid_control_value


if __name__ == '__main__':
    mppt = gridControlMultiply()
    time.sleep(10)
    
