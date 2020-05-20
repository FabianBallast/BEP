const uint8_t filter_numReadings = 63;   //max = 63, see below
#define corr_factor (5/1024)/filter_numReadings


//const int amm_pin_solar_panels = A1;
//const int amm_pin_wind_turbines  = A2;
//const int amm_pin_ledload = A3;
//const int amm_pin_electrolyzer = A4;
//const int amm_pin_power_supply = A5;
//const int amm_pin_fuel_cell = A6;

float sensitivity_1 = 130.0 / 500.0; 
float sensitivity_2 = 130.0 / 500.0; 
float sensitivity_3 = 130.0 / 500.0; 
float sensitivity_4 = 130.0 / 500.0; 
float sensitivity_5 = 130.0 / 500.0; 
float sensitivity_6 = 130.0 / 500.0; 

float Vref_1 = 2500; 
float Vref_2 = 2500; 
float Vref_3 = 2500; 
float Vref_4 = 2500; 
float Vref_5 = 2500; 
float Vref_6 = 2500; 

uint8_t filter_readIndex = 0; // the index of the current reading, 8 bits as its not a high number, always positive so u (unsigned)

// the readings from the analog input, 10 bits reading (max=1024) so 16 bits needed instead of 8; always positive so u
uint16_t raw_readings_1[filter_numReadings];      
uint16_t raw_readings_2[filter_numReadings];     
uint16_t raw_readings_3[filter_numReadings];     
uint16_t raw_readings_4[filter_numReadings];     
uint16_t raw_readings_5[filter_numReadings];     
uint16_t raw_readings_6[filter_numReadings];     

uint16_t sensorValue1 = 0;
uint16_t sensorValue2 = 0;
uint16_t sensorValue3 = 0;
uint16_t sensorValue4 = 0;
uint16_t sensorValue5 = 0;
uint16_t sensorValue6 = 0;

// the running total. Max value of uint16_t=65535 --> max(numReadings) = 65535/1024 = 63
uint16_t runningSum1 = 0;
uint16_t runningSum2 = 0;
uint16_t runningSum3 = 0;
uint16_t runningSum4 = 0;
uint16_t runningSum5 = 0;
uint16_t runningSum6 = 0;


float    current_solar_panels;
float    current_wind_turbines;
float    current_ledload;
float    current_electrolyzer;
float    current_power_supply;
float    current_fuel_cell;


void ammeters_setup(){

  calibrate();
//    sensorValue1 = analogRead(A1);
//    sensorValue2 = analogRead(A2);
//    sensorValue3 = analogRead(A3);
//    sensorValue4 = analogRead(A4);
//    sensorValue5 = analogRead(A5);
//    sensorValue6 = analogRead(A6);
//
//    for (filter_readIndex = 0; filter_readIndex < filter_numReadings; filter_readIndex++) {
//        raw_readings_1[filter_readIndex] = sensorValue1;
//        raw_readings_2[filter_readIndex] = sensorValue2;
//        raw_readings_3[filter_readIndex] = sensorValue3;
//        raw_readings_4[filter_readIndex] = sensorValue4;
//        raw_readings_5[filter_readIndex] = sensorValue5;
//        raw_readings_6[filter_readIndex] = sensorValue6;
//    }
//    runningSum1 = filter_numReadings*sensorValue1;

}

void read_ammeters(){
    sensorValue1 = analogRead(A1);
    sensorValue2 = analogRead(A2);
    sensorValue3 = analogRead(A3);
    sensorValue4 = analogRead(A4);
    sensorValue5 = analogRead(A5);
    sensorValue6 = analogRead(A6);

   /////////////////FILTER\\\\\\\\\\\\\\\\\\
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


    current_solar_panels  = (runningSum1 * corr_factor  - Vref_1)*sensitivity_1;
    current_wind_turbines = (runningSum2 * corr_factor  - Vref_2)*sensitivity_2;
    current_ledload       = (runningSum3 * corr_factor  - Vref_3)*sensitivity_3;
    current_electrolyzer  = (runningSum4 * corr_factor  - Vref_4)*sensitivity_4;
    current_power_supply  = (runningSum5 * corr_factor  - Vref_5)*sensitivity_5;
    current_fuel_cell     = (runningSum6 * corr_factor  - Vref_6)*sensitivity_6;
    
}
