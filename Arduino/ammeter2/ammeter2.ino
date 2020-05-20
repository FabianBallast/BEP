
const int voltageSensorAnalogRead = A1;
const int analogInPin = A0;
const int pwm_out = 6;

//const int avgSamples = 10;
#define delayT 3

int16_t sensorValue = 0; //int16_t


float smoothed_value = 0;                 //the running total
float smooth_alpha = 0.05;

float sensor_value_zero_load = 517.81; 
float sensitivity = 17;  //13.42; 

void setup() {
  Serial.begin(9600);
  analogWrite(pwm_out, 255);
  ///////////////////CALIBRATION\\\\\\\\\\\\\\\\\\\\ DO NOT CONNECT LOAD
  
  ///discard first few
  Serial.print("Calibrating... discarding first values");
  float total = 0;
  int numReadings = 300;
  
  for (int i = 0; i < 2*numReadings; i++)
  {
    analogRead(analogInPin);
    delay(delayT);
  }

  //start actual calibrating

  for (int i = 0; i < numReadings; i++)
  {
    sensorValue = analogRead(analogInPin);
    total += sensorValue;
    Serial.println(sensorValue);
    delay(delayT);
  }
  smoothed_value = total / numReadings;
  sensor_value_zero_load = smoothed_value;
  Serial.print("Done calibrating, Zero value:");
  Serial.print(sensor_value_zero_load);
  Serial.print("\n");
  //////////////////////////////////////////////

}

void loop() {
    sensorValue = analogRead(analogInPin);   // This is the raw sensor value, not very useful without some calculations
    //10 bits: max 1024 --> max(total) = 1024*numReadings=40 000
 

    /////////////////FILTER\\\\\\\\\\\\\\\\\\
    //remove oldest reading, add the new reading to the total:
    smoothed_value = smoothed_value*(1-smooth_alpha) +sensorValue*smooth_alpha;
    ////////////////////////////////////////

    ////calc current
    float current = (smoothed_value - sensor_value_zero_load) *sensitivity; //in mA          //calibrate sensitivity

    
    Serial.print(current);
  //  Serial.print("mA, index: ");
   // Serial.print(readIndex);
    Serial.print(" mA, raw: ");
    Serial.print(sensorValue);
   // Serial.print(", all: ");
  //  Serial.print(readings[0]);
   // Serial.print(readings[1]);
   // Serial.print(", total: ");
  //  Serial.print(total);
    Serial.print(" mA, smoothed value ");
    Serial.print(smoothed_value);
    Serial.print(", voltage analog read: ");
    Serial.print(analogRead(voltageSensorAnalogRead));
    Serial.print("\n");
    delay(delayT);
}
