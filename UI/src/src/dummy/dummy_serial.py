"""This module represents a non-working serial connection."""

def flush():
    pass

def write(bytes):
    pass

in_waiting = [0] * 4

def read(place):
    vals = dict(solar_current = 2, 
                wind_current = 2, 
                load_current = 2,
                elektrolyzer_current = 2,
                power_supply_current = 2,
                fuel_cell_current = 2,
                dummy_serial = 2)
                
    return str(vals)

def reset_input_buffer():
    pass

def reset_output_buffer():
    pass