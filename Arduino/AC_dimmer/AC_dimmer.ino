#include <RBDdimmer.h>

#define outputPin  8
#define TURBINE_START_PIN       11
#define TURBINE_MPPT_PIN       10


dimmerLamp FanDimmer(outputPin); 

int outVal = 0;

void setup() {
  
  
  
  Serial.begin(9600); 
  FanDimmer.begin(NORMAL_MODE, ON);
  Serial.println("Dimmer Program is starting...");
  Serial.println("Set value");
 
 
  pinMode(TURBINE_START_PIN,      OUTPUT);
  pinMode(TURBINE_MPPT_PIN, OUTPUT);
  analogWrite(TURBINE_START_PIN, 255);
  analogWrite(TURBINE_MPPT_PIN, 0);
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
    analogWrite(TURBINE_START_PIN,255);

  }
  delay(50);

}
