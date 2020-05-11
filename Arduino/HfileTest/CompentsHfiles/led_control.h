#include "libs/Adafruit_NeoPixel/Adafruit_NeoPixel.h"
#ifdef __AVR__
#include <avr/power.h> // Required for 16 MHz Adafruit Trinket
#endif

#define PIN      6
#define NUMPIXELS 8


Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

#define DELAYVAL 500 // Time (in milliseconds) to pause between pixels

void led_setup() {
    pixels.begin();
    pixels.clear();
    pixels.setBrightness(255); //max op 255
    pixels.setPixelColor(0, pixels.Color(255, 255, 255));
    pixels.setPixelColor(1, pixels.Color(255, 255, 255));
    pixels.setPixelColor(2, pixels.Color(255, 255, 255));
    pixels.setPixelColor(3, pixels.Color(255, 255, 255));
    pixels.setPixelColor(4, pixels.Color(255, 255, 255));
    pixels.setPixelColor(5, pixels.Color(255, 255, 255));
    pixels.setPixelColor(6, pixels.Color(255, 255, 255));
    pixels.setPixelColor(7, pixels.Color(255, 255, 255));
    pixels.setPixelColor(8, pixels.Color(255, 255, 255));
    pixels.show();
}

void led_loop() {

}
