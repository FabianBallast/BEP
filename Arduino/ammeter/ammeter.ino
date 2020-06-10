
const int voltageSensorAnalogRead = A1;
const int analogInPin = A0;
const int pwm_out = 6;

//const int avgSamples = 10;
#define numReadings 100         //max = 63, see below
#define delayT 3

int16_t sensorValue = 0; //int16_t
float avg_reading = 0;

int16_t readings[numReadings];  //int16_t    // the readings from the analog input, 10 bits reading (max=1024) so 16 bits needed instead of 8; always positive so u
byte readIndex = 0;           //uint8_t   // the index of the current reading, 8 bits as its not a high number, always positive so u (unsigned)
float total = 0;                 //the running total

float sensor_value_zero_load = 517.81; 
float sensitivity = 11.5;  //13.42; 

void setup() {
  Serial.begin(9600);
  analogWrite(pwm_out, 255);
  ///////////////////CALIBRATION\\\\\\\\\\\\\\\\\\\\ DO NOT CONNECT LOAD
  
  ///discard first few
  Serial.print("Calibrating... discarding first values");
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
  sensor_value_zero_load = total / numReadings;
  Serial.print("Done calibrating, Zero value:");
  Serial.print(sensor_value_zero_load);
  Serial.print("\n");
  total = 0;
  //////////////////////////////////////////////

}

void loop() {
    sensorValue = analogRead(analogInPin);   // This is the raw sensor value, not very useful without some calculations
    //10 bits: max 1024 --> max(total) = 1024*numReadings=40 000
 

    /////////////////FILTER\\\\\\\\\\\\\\\\\\
    //remove oldest reading, add the new reading to the total:
    total = total +  sensorValue  -  readings[readIndex];
    readings[readIndex] = sensorValue;

    readIndex++;
    if (readIndex >= numReadings) {
      readIndex = 0;
    }
    avg_reading = total / numReadings;
    ////////////////////////////////////////

    ////calc current
    float current = (avg_reading - sensor_value_zero_load) *sensitivity; //in mA          //calibrate sensitivity

    
    Serial.print(current);
  //  Serial.print("mA, index: ");
   // Serial.print(readIndex);
    Serial.print(", raw: ");
    Serial.print(sensorValue);
   // Serial.print(", all: ");
  //  Serial.print(readings[0]);
   // Serial.print(readings[1]);
   // Serial.print(", total: ");
  //  Serial.print(total);
    Serial.print(" mA, average value ");
    Serial.print(avg_reading);
    Serial.print(", voltage analog read: ");
    Serial.print(analogRead(voltageSensorAnalogRead));
    Serial.print("\n");
    delay(delayT);
}
