"""This module is a non-working version of neopixel"""

GRB = None

class NeoPixel(list):
    """Represents the NeoPixel pixel object."""

    def __init__(self, pin1, length, brightness=0, auto_write=0, pixel_order=0):
        super().__init__([0] * length)
    
    def show(self):
        pass
    