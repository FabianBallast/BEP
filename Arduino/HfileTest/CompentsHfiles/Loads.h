
// #ifndef _LOADS_H_
// #define _LOADS_H_

#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
#include <avr/power.h> // Required for 16 MHz Adafruit Trinket
#endif



#define LED_PIN      6


#define NUMPIXELS 8

#define DELAYVAL 500 // Time (in milliseconds) to pause between pixels
#define MODULOCORRECTION 255 / (100/NUMPIXELS)

Adafruit_NeoPixel pixels(NUMPIXELS, LED_PIN, NEO_GRB + NEO_KHZ800);

byte amount_pixels_fully_on;
byte intensity_of_half_one;

void led_setup() {
    pinMode(LED_PIN, OUTPUT);
    pixels.begin();
    pixels.clear();
    pixels.setBrightness(100); //max op 255
    pixels.show();
}

void load_set(byte set_value) {
    //input a value between 0 and 100

    pixels.clear();
    byte modulo = set_value % NUMPIXELS;
    byte amount_pixels_fully_on = (set_value-modulo)/NUMPIXELS;

    //set first pixels fully on
    for (byte pixel_index = 0; pixel_index <= NUMPIXELS; pixel_index++) {
        if (pixel_index <=amount_pixels_fully_on) {
            pixels.setPixelColor(pixel_index, pixels.Color(255, 255, 255));
        }
        else if (pixel_index == amount_pixels_fully_on+1){ // //set 1 pixel partly on
            intensity_of_half_one = modulo * MODULOCORRECTION;
            pixels.setPixelColor(amount_pixels_fully_on+1, pixels.Color(intensity_of_half_one, intensity_of_half_one, intensity_of_half_one));
        }
        else {//set rest of pixels fully off
            pixels.setPixelColor(pixel_index, pixels.Color(0, 0, 0));
        }
    }
    pixels.show();
}


// #endif // _LOADS_H_ 
