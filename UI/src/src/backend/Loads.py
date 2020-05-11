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
PERC_PER_PIXEL = 100/num_pixels


def load_set (set_value):
    #input a value between 0 and 100

    #pixels.clear()
    leds_on = set_value/PERC_PER_PIXEL
    amount_pixels_fully_on = int(leds_on)
    print(amount_pixels_fully_on, ' leds fully on, ', leds_on, ' total')
    #set first pixels fully on
    for pixel_index in range(num_pixels):
        if (pixel_index <amount_pixels_fully_on):
            pixels[pixel_index] = (255, 255, 255)
            print('LED', pixel_index, ' on' )

        elif (pixel_index == amount_pixels_fully_on):     #set 1 pixel partly on
            intensity_of_half_one = int((leds_on-amount_pixels_fully_on) * 255)
            pixels[pixel_index] = (intensity_of_half_one, intensity_of_half_one, intensity_of_half_one)
            print('LED', pixel_index,100*(leds_on-amount_pixels_fully_on), ' % on' )

        else: #set rest of pixels fully off
            pixels[pixel_index] = (0, 0, 0)
            print('LED', pixel_index, ' off' )

    print('load' ,set_value)
    pixels.show()

if __name__ == '__main__':
    for p in range(100):
        load_set(p)
        time.sleep(1)

    print(' done' )

