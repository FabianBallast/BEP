#include "CompentsHfiles/FuelCell.h"
#include "CompentsHfiles/Loads.h"


void setup() {
  pinMode(5, OUTPUT);
  led_setup();
}

void loop() {
  analogWrite(5, 100);
  for (byte i = 0; i <= 100; i++) {\
    //analogWrite(5, i);
    load_set(i);
    delay(50);
  }
}
