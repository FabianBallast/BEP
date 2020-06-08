#include <RBDdimmer.h>

#define outputPin  8

#define TURIBNE_MOSFET_PIN      11


dimmerLamp FanDimmer(outputPin); 

int outVal = 0;

void setup() {
  
  
  
  Serial.begin(9600); 
  FanDimmer.begin(NORMAL_MODE, ON);
  Serial.println("Dimmer Program is starting...");
  Serial.println("Set value");
 
 
  pinMode(TURIBNE_MOSFET_PIN,      OUTPUT);
 
  analogWrite(TURIBNE_MOSFET_PIN, 0);

  pinMode(7,      OUTPUT);
 
  analogWrite(7, 255);
}



void loop() {
  int preVal = outVal;

  if (Serial.available())
  {
    int buf = Serial.parseInt();
    if (buf != 0) {
      outVal = buf; // map(buf, 0, 100, 10, 80);
    }
    delay(200);
    FanDimmer.setPower(outVal); // setPower(0-99%);  

  }

  if (preVal != outVal)
  {
    Serial.print("lampValue -> ");

    Serial.print(FanDimmer.getPower());
    Serial.println("%");

  }
  delay(50);

}
