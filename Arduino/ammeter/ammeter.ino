
const int voltageSensorAnalogRead = A1;
const int analogInPin = A0;
const int pwm_out = 6;

//const int avgSamples = 10;
#define numReadings 50         //max = 63, see below

int16_t sensorValue = 0; //int16_t
float avg_reading = 0;

int16_t readings[numReadings];  //int16_t    // the readings from the analog input, 10 bits reading (max=1024) so 16 bits needed instead of 8; always positive so u
byte readIndex = 0;           //uint8_t   // the index of the current reading, 8 bits as its not a high number, always positive so u (unsigned)
double total = 0;                 //int32_t  // the running total. Max value of uint16_t=65535 --> max(numReadings) = 65535/1024 = 63

float sensor_value_zero_load = 367.5; 
float sensitivity = 500.0 *4.88/ 500.0; 

void setup() {
  Serial.begin(9600);

  analogWrite(pwm_out, 255);
  
  ///discard first few
  Serial.print("Calibrating... discarding first 100 values");
  for (int i = 0; i < 100; i++)
  {
    analogRead(analogInPin);
    delay(5);
  }



  //start actual calibrating
  
  //find average zero value: DO NOT CONNECT FOR FIRST (delay*numReadings-->2) second after boot
  for (int i = 0; i < numReadings; i++)
  {
    sensorValue = analogRead(analogInPin);
    total += sensorValue;
    Serial.println(sensorValue);
    delay(5);
  }
  sensor_value_zero_load = total / numReadings;
  Serial.print("Zero value:");
  Serial.print(sensor_value_zero_load);
  Serial.print("\n");
  total = 0;
}

void loop() {
    sensorValue = analogRead(analogInPin);   // This is the raw sensor value, not very useful without some calculations
    //10 bits: max 1024 --> max(total) = 1024*numReadings=40 000
 

    /////////////////FILTER\\\\\\\\\\\\\\\\\\
    //remove oldest reading, add the new reading to the total:
    total = total +  sensorValue  -  readings[readIndex];
    readings[readIndex] = sensorValue;

  // advance to the next position in the array:
    readIndex++;
    if (readIndex >= numReadings) {
      readIndex = 0;
    }
    avg_reading = total / numReadings;
    ////////////////////////////////////////

    ////calc current
    //float voltage = 4.88 * avg_reading; //in mV   // The on-board ADC is 10-bits -> 2^10 = 1024 -> 5V / 1024 ~= 4.88mV
    float current = (avg_reading - sensor_value_zero_load) *sensitivity; //in mA          //calibrate sensitivity


  // Serial.print(voltage);
  // Serial.print("mV");

    
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
    delay(2);
}
