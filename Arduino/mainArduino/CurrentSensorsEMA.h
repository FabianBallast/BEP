#define filter_numReadings_calibrate 100   
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

float smooth_alpha = 0.05;

float sensor_value_zero_load_1 = 517.81; 
float sensor_value_zero_load_2 = 517.81; 
float sensor_value_zero_load_3 = 517.81; 
float sensor_value_zero_load_4 = 517.81; 
float sensor_value_zero_load_5 = 517.81; 
float sensor_value_zero_load_6 = 517.81; 

int sensorValue1 = 0;
int sensorValue2 = 0;
int sensorValue3 = 0;
int sensorValue4 = 0;
int sensorValue5 = 0;
int sensorValue6 = 0;

float smoothed_value1 = 0;
float smoothed_value2;
float smoothed_value3;
float smoothed_value4 = 0;
float smoothed_value5 = 0;
float smoothed_value6 = 0;


float    current_solar_panels;
float    current_wind_turbines;
float    current_ledload;
float    current_electrolyzer;
float    current_power_supply;
float    current_fuel_cell;


void ammeters_setup(){
    //CALIBRATE
   Serial.print("skipping first values (using EMA filter)... \n");
   for (int filter_readIndex = 0; filter_readIndex < filter_numReadings_calibrate; filter_readIndex++) {
        analogRead(A1);
        analogRead(A2);
        analogRead(A3);
        analogRead(A4);
        analogRead(A5);
        analogRead(A6);

        delay(sampleTime);
    }
    
      ///find average zero load value
    Serial.print("Starting calibration... \n");  
    for (int filter_readIndex = 0; filter_readIndex < filter_numReadings_calibrate; filter_readIndex++) {
        smoothed_value1 += analogRead(A1);
        smoothed_value2 += analogRead(A2);
        smoothed_value3 += analogRead(A3);
        smoothed_value4 += analogRead(A4);
        smoothed_value5 += analogRead(A5);
        smoothed_value6 += analogRead(A6);

        delay(sampleTime);
    }
    
    sensor_value_zero_load_1 = smoothed_value1/filter_numReadings_calibrate;
    sensor_value_zero_load_2 = smoothed_value2/filter_numReadings_calibrate;
    sensor_value_zero_load_3 = smoothed_value3/filter_numReadings_calibrate;
    sensor_value_zero_load_4 = smoothed_value4/filter_numReadings_calibrate;
    sensor_value_zero_load_5 = smoothed_value5/filter_numReadings_calibrate;
    sensor_value_zero_load_6 = smoothed_value6/filter_numReadings_calibrate;

    smoothed_value1 = sensor_value_zero_load_1;
    smoothed_value2 = sensor_value_zero_load_2;
    smoothed_value3 = sensor_value_zero_load_3;
    smoothed_value4 = sensor_value_zero_load_4;
    smoothed_value5 = sensor_value_zero_load_5;
    smoothed_value6 = sensor_value_zero_load_6;
    

    Serial.print("A1 zero load: ");
    Serial.print(sensor_value_zero_load_1);
    Serial.print(", Done calibrating \n");
}


void read_ammeters(){
    sensorValue1 = analogRead(A1);
    sensorValue2 = analogRead(A2);
    sensorValue3 = analogRead(A3);
    sensorValue4 = analogRead(A4);
    sensorValue5 = analogRead(A5);
    sensorValue6 = analogRead(A6);
    
   /////////////////FILTER/////////////////
    smoothed_value1 = smoothed_value1*(1-smooth_alpha) + sensorValue1*smooth_alpha;
    smoothed_value2 = smoothed_value2*(1-smooth_alpha) + sensorValue2*smooth_alpha;
    smoothed_value3 = smoothed_value3*(1-smooth_alpha) + sensorValue3*smooth_alpha;
    smoothed_value4 = smoothed_value4*(1-smooth_alpha) + sensorValue4*smooth_alpha;
    smoothed_value5 = smoothed_value5*(1-smooth_alpha) + sensorValue5*smooth_alpha;
    smoothed_value6 = smoothed_value6*(1-smooth_alpha) + sensorValue6*smooth_alpha;
    /////////////////////////////



    current_solar_panels  = (smoothed_value1  - sensor_value_zero_load_1)*sensitivity_1;
    current_wind_turbines = (smoothed_value2  - sensor_value_zero_load_2)*sensitivity_2;
    current_ledload       = (smoothed_value3  - sensor_value_zero_load_3)*sensitivity_3;
    current_electrolyzer  = (smoothed_value4  - sensor_value_zero_load_4)*sensitivity_4;
    current_power_supply  = (smoothed_value5  - sensor_value_zero_load_5)*sensitivity_5;
    current_fuel_cell     = (smoothed_value6  - sensor_value_zero_load_6)*sensitivity_6;

//    Serial.print("A1 zero load: ");
//    Serial.print(sensor_value_zero_load_1);
//    Serial.print(", current smoothed: ");
//    Serial.print(smoothed_value1);
//    Serial.print(", current sensorValue: ");
//    Serial.print(sensorValue1);
//    Serial.print(", current current");
//    Serial.print(current_solar_panels);
//    Serial.print("\n");
    
}
