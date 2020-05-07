#include <HardwareSerial.h>
#include <SoftwareSerial.h>

int f = 5; //Hz
double delayTime = 1 / f * 1000;

Serial.println(delayTime);

int PIN_LED = 7;

void setup() {

    pinMode(PIN_LED, OUTPUT);
}

void loop() {

    digitalWrite(PIN_LED, HIGH);
    delay(delayTime);
    digitalWrite(PIN_LED, LOW);
    delay(delayTime);

}