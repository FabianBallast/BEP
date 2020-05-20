#define filter_numReadings 100   //max = 63, see below
#define corr_factor (5/1024)/filter_numReadings
#define sampleTime 3

//const int amm_pin_solar_panels = A1;
//const int amm_pin_wind_turbines  = A2;
//const int amm_pin_ledload = A3;
//const int amm_pin_electrolyzer = A4;
//const int amm_pin_power_supply = A5;
//const int amm_pin_fuel_cell = A6;

#define sensitivity_1 17; 
#define sensitivity_2 17; 
#define sensitivity_3 17; 
#define sensitivity_4 17; 
#define sensitivity_5 17; 
#define sensitivity_6 17; 

float sensor_value_zero_load_1 = 517.81*filter_numReadings; 
float sensor_value_zero_load_2 = 517.81*filter_numReadings; 
float sensor_value_zero_load_3 = 517.81*filter_numReadings; 
float sensor_value_zero_load_4 = 517.81*filter_numReadings; 
float sensor_value_zero_load_5 = 517.81*filter_numReadings; 
float sensor_value_zero_load_6 = 517.81*filter_numReadings; 

int filter_readIndex = 0; // the index of the current reading, 8 bits as its not a high number, always positive so u (unsigned)

// the readings from the analog input, 10 bits reading (max=1024) so 16 bits needed instead of 8; always positive so u
int raw_readings_1[filter_numReadings];      
int raw_readings_2[filter_numReadings];     
int raw_readings_3[filter_numReadings];     
int raw_readings_4[filter_numReadings];     
int raw_readings_5[filter_numReadings];     
int raw_readings_6[filter_numReadings];     

int sensorValue1 = 0;
int sensorValue2 = 0;
int sensorValue3 = 0;
int sensorValue4 = 0;
int sensorValue5 = 0;
int16_t sensorValue6 = 0;

// the running total. Max value of uint16_t=65535 --> max(numReadings) = 65535/1024 = 63
float runningSum1 = 0;
float runningSum2 = 0;
float runningSum3 = 0;
float runningSum4 = 0;
float runningSum5 = 0;
float runningSum6 = 0;

float    current_solar_panels;
float    current_wind_turbines;
float    current_ledload;
float    current_electrolyzer;
float    current_power_supply;
float    current_fuel_cell;


void ammeters_setup(){
    /////////////////////////////CALIBRATE
     //////////discard first values
   for (filter_readIndex = 0; filter_readIndex < filter_numReadings; filter_readIndex++) {
        analogRead(A1);
        analogRead(A2);
        analogRead(A3);
        analogRead(A4);
        analogRead(A5);
        analogRead(A6);

        delay(sampleTime);
    }
    
      ///find average zero load value
    for (filter_readIndex = 0; filter_readIndex < filter_numReadings; filter_readIndex++) {
        runningSum1 += analogRead(A1);
        runningSum2 += analogRead(A2);
        runningSum3 += analogRead(A3);
        runningSum4 += analogRead(A4);
        runningSum5 += analogRead(A5);
        runningSum6 += analogRead(A6);

        delay(sampleTime);
    }
    
    sensor_value_zero_load_1 = runningSum1;
    sensor_value_zero_load_2 = runningSum2;
    sensor_value_zero_load_3 = runningSum3;
    sensor_value_zero_load_4 = runningSum4;
    sensor_value_zero_load_5 = runningSum5;
    sensor_value_zero_load_6 = runningSum6;

    Serial.print("A1 zero load: ");
    Serial.print(sensor_value_zero_load_1);
    Serial.print(", Done calibrating \n");
    runningSum1 = 0;
    runningSum2 = 0;
    runningSum3 = 0;
    runningSum4 = 0;
    runningSum5 = 0;
    runningSum6 = 0;

}


void read_ammeters(){
    sensorValue1 = analogRead(A1);
    sensorValue2 = analogRead(A2);
    sensorValue3 = analogRead(A3);
    sensorValue4 = analogRead(A4);
    sensorValue5 = analogRead(A5);
    sensorValue6 = analogRead(A6);

   /////////////////FILTER
    runningSum1 = runningSum1 - raw_readings_1[filter_readIndex] + sensorValue1;
    runningSum2 = runningSum2 - raw_readings_2[filter_readIndex] + sensorValue2;
    runningSum3 = runningSum3 - raw_readings_3[filter_readIndex] + sensorValue3;
    runningSum4 = runningSum4 - raw_readings_4[filter_readIndex] + sensorValue4;
    runningSum5 = runningSum5 - raw_readings_5[filter_readIndex] + sensorValue5;
    runningSum6 = runningSum6 - raw_readings_6[filter_readIndex] + sensorValue6;

    raw_readings_1[filter_readIndex] = sensorValue1;
    raw_readings_2[filter_readIndex] = sensorValue2;
    raw_readings_3[filter_readIndex] = sensorValue3;
    raw_readings_4[filter_readIndex] = sensorValue4;
    raw_readings_5[filter_readIndex] = sensorValue5;
    raw_readings_6[filter_readIndex] = sensorValue6;

    // advance to the next position in the array:
    filter_readIndex = filter_readIndex + 1;
    if (filter_readIndex >= filter_numReadings) {
      filter_readIndex = 0;
    }

   // Serial.print("A1 zero load: ");
 //   Serial.print(sensor_value_zero_load_1);
//    Serial.print(", current sum");
//    Serial.print(runningSum1);
//    Serial.print(", current sensorValue");
//    Serial.print(sensorValue1);
//    Serial.print("\n");

    current_solar_panels  = (runningSum1  - sensor_value_zero_load_1)*sensitivity_1;
    current_wind_turbines = (runningSum2  - sensor_value_zero_load_2)*sensitivity_2;
    current_ledload       = (runningSum3  - sensor_value_zero_load_3)*sensitivity_3;
    current_electrolyzer  = (runningSum4  - sensor_value_zero_load_4)*sensitivity_4;
    current_power_supply  = (runningSum5  - sensor_value_zero_load_5)*sensitivity_5;
    current_fuel_cell     = (runningSum6  - sensor_value_zero_load_6)*sensitivity_6;
    
}
