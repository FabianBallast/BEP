"""This module represents a non-working serial connection."""

def flush():
    pass

def write(bytes):
    pass

in_waiting = [0] * 4

def read(place): #'zonI', 'windI', 'loadI', 'EL_I',     'PS_I', 'FC_I', 'OptWindI', 'EV_U', 'FC_U','gridU', 'loopT']
    vals = dict(zonI = 2, 
                windI = 2, 
                loadI = 2,
                EL_I = 2,
                PS_I = 2,
                FC_I = 2,
                windU = 7,
                fan = 2,
                EV_U = 2,
                FC_U = 2,
                gridU = 2,
                loopT = 2,
                dummy_serial = 2)
                
    return str(vals)

def reset_input_buffer():
    pass

def reset_output_buffer():
    pass