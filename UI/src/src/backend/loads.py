"""This module deals with all the loads for the system."""

#pip3 install adafruit-circuitpython-neopixel
#wire LED on D18 (only on D18!)

import time
try:
    import board
    import neopixel
    import RPi.GPIO as IO
except NotImplementedError:
    from ..dummy import dummy_board as board                   #pylint: disable=relative-beyond-top-level
    from ..dummy import dummy_pixel as neopixel                #pylint: disable=relative-beyond-top-level
    from ..dummy import dummy_io as IO                         #pylint: disable=relative-beyond-top-level 


#neopixel stick
#NUM_PIXELS = 8
#LED_PIXELS_PIN = board.D18
#ORDER = neopixel.GRB
#pixels = neopixel.NeoPixel(
#    LED_PIXELS_PIN, NUM_PIXELS, brightness=0.2, auto_write=False, pixel_order=ORDER)



#led strips
LED_PWM_PINS = [27,22]

IO.setmode(IO.BCM)
for pin in LED_PWM_PINS:
    IO.setup(pin, IO.OUT)
NUM_PIXELS = len(LED_PWM_PINS)
pwm_lights = [IO.PWM(pin, 100) for pin in LED_PWM_PINS]
for pwm in pwm_lights:
    pwm.start(0)


PERC_PER_PIXEL = 100/NUM_PIXELS


def load_light_set(pixel_index, set_value):
    if set_value>99: set_value = 100
    elif set_value<1: set_value = 0
    
    #pixels[pixel_index] = (255, 255, 255)*set_value/100
    pwm_lights[pixel_index].ChangeDutyCycle(set_value)

    #print('light', pixel_index, set_value)

def load_set(set_value):
    """Input a value between 0 and 100 and the LEDs will show the load accordingly."""

    #pixels.clear()
    leds_on = set_value/PERC_PER_PIXEL
    amount_pixels_fully_on = int(leds_on)
    #print(amount_pixels_fully_on, ' leds fully on, ', leds_on, ' total')
    
    for pixel_index in range(NUM_PIXELS):
        if pixel_index < amount_pixels_fully_on:  #set first pixels fully on
            load_light_set(pixel_index, 100)         
        elif pixel_index == amount_pixels_fully_on:     #set 1 pixel partly on
            intensity_of_half_one = int((leds_on - amount_pixels_fully_on) * 100)
            load_light_set(pixel_index, intensity_of_half_one)         
        else: #set rest of pixels fully off
            load_light_set(pixel_index, 0)        

    print('load', set_value)
    
    #pixels.show()

if __name__ == '__main__':
    for p in range(100):
        load_set(p)
        time.sleep(1)

    print('done')
