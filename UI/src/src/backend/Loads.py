#pip3 install adafruit-circuitpython-neopixel


#wire LED on D18 (only on D18!)
import time
import board
import neopixel


led_pixels_pin = board.D18

# The number of NeoPixels
num_pixels = 8
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    led_pixels_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER)

#teste

MODULOCORRECTION = 255 / (100/num_pixels)

# def led_setup():
#     pixels.begin()
#     pixels.clear()
#     pixels.setBrightness(100) //max op 255
#     pixels.show()

def load_set (set_value):
    #input a value between 0 and 100

    #pixels.clear()
    modulo = set_value % num_pixels
    amount_pixels_fully_on = (set_value-modulo)/num_pixels

    #set first pixels fully on
    for pixel_index in range(num_pixels):
        if (pixel_index <=amount_pixels_fully_on):
            pixels[pixel_index] = (255, 255, 255)

        elif (pixel_index == amount_pixels_fully_on+1):     #set 1 pixel partly on
            intensity_of_half_one = int(modulo * MODULOCORRECTION)
            pixels[pixel_index] = (intensity_of_half_one, intensity_of_half_one, intensity_of_half_one)

        else: #set rest of pixels fully off
            pixels[pixel_index] = (0, 0, 0)

    print('load' ,set_value)
    pixels.show()

for p in range(100):
    load_set(p)
    time.sleep(1)

print(' done' )
