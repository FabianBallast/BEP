"""This module represents a non-working serial connection."""

def flush():
    pass

def write(bytes):
    pass

in_waiting = [0] * 4

def read():
    return [255, 0, 0, 254]

def reset_input_buffer():
    pass

def reset_output_buffer():
    pass