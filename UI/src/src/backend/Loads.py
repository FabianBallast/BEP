
import time
import board
import neopixel


led_pixels_pin = board.D18

# The number of NeoPixels
num_pixels = 8
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    led_pixels_pin, num_pixels, brightness=1.0, auto_write=False, pixel_order=ORDER)



MODULOCORRECTION = 255 / (100/num_pixels)

# def led_setup():
#     pixels.begin()
#     pixels.clear()
#     pixels.setBrightness(100) //max op 255
#     pixels.show()

def load_set (set_value):
    #input a value between 0 and 100

    pixels.clear()
    modulo = set_value % num_pixels
    amount_pixels_fully_on = (set_value-modulo)/num_pixels

    #set first pixels fully on
    for pixel_index in range(len(num_pixels)):
        if (pixel_index <=amount_pixels_fully_on):
            pixels[pixel_index].fill((255, 255, 255))

        elif (pixel_index == amount_pixels_fully_on+1):     #set 1 pixel partly on
            intensity_of_half_one = modulo * MODULOCORRECTION
            pixels[pixel_index].fill(amount_pixels_fully_on+1, pixels.Color(intensity_of_half_one, intensity_of_half_one, intensity_of_half_one))

        else: #set rest of pixels fully off
            pixels[pixel_index].fill((0, 0, 0))


    pixels.show()
