#define filter_numReadings 100   //max = 63, see below
#define corr_factor (5/1024)/filter_numReadings
#define sampleTime 3
#define discardNloops 3

//const int amm_pin_solar_panels = A1;
//const int amm_pin_wind_turbines  = A2;
//const int amm_pin_ledload = A3;
//const int amm_pin_electrolyzer = A4;
//const int amm_pin_power_supply = A5;
//const int amm_pin_fuel_cell = A6;

float zero_load_min = 500.0*filter_numReadings; 
float zero_load_max = 550.0*filter_numReadings; 


#define sensitivity_1 -11.5   / filter_numReadings; 
#define sensitivity_2 -11.5   / filter_numReadings; 
#define sensitivity_3 -11.5   / filter_numReadings; 
#define sensitivity_4 -11.5   / filter_numReadings; 
#define sensitivity_5 -11.5   / filter_numReadings; 
#define sensitivity_6 -11.5   / filter_numReadings; 

float sensor_value_zero_load_1 = 513.975*filter_numReadings; 
float sensor_value_zero_load_2 = 513.975*filter_numReadings; 
float sensor_value_zero_load_3 = 513.975*filter_numReadings;  
float sensor_value_zero_load_4 = 513.975*filter_numReadings; 
float sensor_value_zero_load_5 = 513.975*filter_numReadings; 
float sensor_value_zero_load_6 = 513.975*filter_numReadings; 

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
    Serial.print("max");
    Serial.print(zero_load_max);
  
   Serial.print("skipping first values (using SMA filter)... \n");
    /////////////////////////////CALIBRATE
     //////////discard first values
   for (filter_readIndex = 0; filter_readIndex < discardNloops*filter_numReadings; filter_readIndex++) {
        analogRead(A1);
        analogRead(A2);
        analogRead(A3);
        analogRead(A4);
        analogRead(A5);
        analogRead(A6);
        //Serial.println(analogRead(A1));
        delay(sampleTime);

//        raw_readings_1[filter_readIndex]=0;      
//        raw_readings_2[filter_readIndex]=0;     
//        raw_readings_3[filter_readIndex]=0;     
//        raw_readings_4[filter_readIndex]=0;     
//        raw_readings_5[filter_readIndex]=0;     
//        raw_readings_6[filter_readIndex]=0;   
    }
    Serial.print("Starting calibration... \n");
      ///find average zero load value
    for (filter_readIndex = 0; filter_readIndex < filter_numReadings; filter_readIndex++) {

        sensorValue1 = analogRead(A1);
        sensorValue2 = analogRead(A2);
        sensorValue3 = analogRead(A3);
        sensorValue4 = analogRead(A4);
        sensorValue5 = analogRead(A5);
        sensorValue6 = analogRead(A6);
        runningSum1 += sensorValue1;
        runningSum2 += sensorValue2;
        runningSum3 += sensorValue3;
        runningSum4 += sensorValue4;
        runningSum5 += sensorValue5;
        runningSum6 += sensorValue6;

        raw_readings_1[filter_readIndex] = sensorValue1;
        raw_readings_2[filter_readIndex] = sensorValue2;
        raw_readings_3[filter_readIndex] = sensorValue3;
        raw_readings_4[filter_readIndex] = sensorValue4;
        raw_readings_5[filter_readIndex] = sensorValue5;
        raw_readings_6[filter_readIndex] = sensorValue6;

        delay(sampleTime);
    }

    //make sure the system calibrates on the right values (off state)

    Serial.print("Running1   ");
    Serial.print(runningSum1);
    Serial.print("max");
    Serial.print(zero_load_max);
    if((runningSum1>zero_load_min)&&(runningSum1<zero_load_max)) {// reality check
      Serial.print("yeah");
      sensor_value_zero_load_1 = runningSum1;
    }
    if((runningSum2>zero_load_min)&&(runningSum2<zero_load_max)) {// reality check
      sensor_value_zero_load_2 = runningSum2;
    }
    if((runningSum3>zero_load_min)&&(runningSum3<zero_load_max)) // reality check
      sensor_value_zero_load_3 = runningSum3;
    if((runningSum4>zero_load_min)&&(runningSum4<zero_load_max)) // reality check
      sensor_value_zero_load_4 = runningSum4;
    if((runningSum5>zero_load_min)&&(runningSum5<zero_load_max)) // reality check
      sensor_value_zero_load_5 = runningSum5;
    if((runningSum6>zero_load_min)&&(runningSum6<zero_load_max)) // reality check
      sensor_value_zero_load_6 = runningSum6;

    Serial.print("Done calibrating \n");
    Serial.print("zero loads: ");
    Serial.print(sensor_value_zero_load_1);
    Serial.print(", ");
    Serial.print(sensor_value_zero_load_2);
    Serial.print(", ");
    Serial.print(sensor_value_zero_load_3);
    Serial.print(", ");
    Serial.print(sensor_value_zero_load_4);
    Serial.print(", ");
    Serial.print(sensor_value_zero_load_5);
    Serial.print(", ");
    Serial.print(sensor_value_zero_load_6);
    Serial.print(", ");
//    runningSum1 = 0;
//    runningSum2 = 0;
//    runningSum3 = 0;
//    runningSum4 = 0;
//    runningSum5 = 0;
//    runningSum6 = 0;


//    raw_readings_1[0]=runningSum1;      
//    raw_readings_2[0]=runningSum2;     
//    raw_readings_3[0]=runningSum3;     
//    raw_readings_4[0]=runningSum4;     
//    raw_readings_5[0]=runningSum5;     
//    raw_readings_6[0]=runningSum6;   

    filter_readIndex = 0;
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

//    Serial.print("A1 zero load: ");
//    Serial.print(sensor_value_zero_load_1);
//    Serial.print(", runnin sum 1: ");
//    Serial.print(runningSum1);
//    Serial.print(", current sensorValue: ");
//    Serial.print(sensorValue1);
//    Serial.print(", current current");
//    Serial.print(current_solar_panels);
//    Serial.print("\n");
}
