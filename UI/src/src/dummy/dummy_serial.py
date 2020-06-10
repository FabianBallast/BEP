"""This module represents a non-working serial connection."""

def flush():
    pass

def write(bytes):
    pass

in_waiting = [0] * 4

def read(place): #'zonI', 'windI', 'loadI', 'EL_I',     'PS_I', 'FC_I', 'OptWindI', 'EV_U', 'FC_U','gridU', 'loopT']
    vals = dict(zonU = 2, 
                loadI = 2, 
                windU = 2,
                FC_U = 2,
                FC_Y = 2,
                EL_U = 2,
                EL_I = 7,
                EL_Y = 2,
                gridU = 2,
                gridX = 2,
                loopT = 2,
                PS_I = 2,
                fan = 2,
                windY = 2,
                flowTot = 2,
                dummy_serial = 2)
                
    return str(vals)

def reset_input_buffer():
    pass

def reset_output_buffer():
    pass