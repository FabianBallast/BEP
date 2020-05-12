"""This module deals with all the loads for the system."""

#pip3 install adafruit-circuitpython-neopixel
#wire LED on D18 (only on D18!)

import time
import board
import neopixel


LED_PIXELS_PIN = board.D18
NUM_PIXELS = 8
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    LED_PIXELS_PIN, NUM_PIXELS, brightness=0.2, auto_write=False, pixel_order=ORDER)

PERC_PER_PIXEL = 100/NUM_PIXELS

def load_set(set_value):
    """Input a value between 0 and 100 and the LEDs will show the load accordingly."""

    #pixels.clear()
    leds_on = set_value/PERC_PER_PIXEL
    amount_pixels_fully_on = int(leds_on)
    #print(amount_pixels_fully_on, ' leds fully on, ', leds_on, ' total')
    #set first pixels fully on
    for pixel_index in range(NUM_PIXELS):
        if pixel_index < amount_pixels_fully_on:
            pixels[pixel_index] = (255, 255, 255)
            #print('LED', pixel_index, 'on')

        elif pixel_index == amount_pixels_fully_on:     #set 1 pixel partly on
            intensity_of_half_one = int((leds_on - amount_pixels_fully_on) * 255)
            pixels[pixel_index] = (intensity_of_half_one, intensity_of_half_one, intensity_of_half_one) #pylint: disable=C0301
            #print('LED', pixel_index, 100*(leds_on-amount_pixels_fully_on), '% on')

        else: #set rest of pixels fully off
            pixels[pixel_index] = (0, 0, 0)
            #print('LED', pixel_index, 'off')

    #print('load', set_value)
    pixels.show()

if __name__ == '__main__':
    for p in range(100):
        load_set(p)
        time.sleep(1)

    print('done')
