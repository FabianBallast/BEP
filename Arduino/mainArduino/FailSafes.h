
//A1-A6 wordt gebruikt voor currentsensors

#define ELECTROLYZER_VOLTAGE_READ = A7;
#define FUEL_CELL_VOLTAGE_READ = A8;
#define MAX_READING_ELECTROLYZER   (2.0/5.0)*2014
#define MIN_READING_ELECTROLYZER   (0.9/5.0)*2014

uint16_t electrolyzer_voltage; 
uint16_t fuel_cell_voltage; 

void check_H2_voltages(){

    electrolyzer_voltage = analogRead(A7); 
    fuel_cell_voltage    = analogRead(A8);

    //failsafe Electrolyzer:
    if (electrolyzer_voltage>MAX_READING_ELECTROLYZER){
        //set_electrolyzer(0);
        electrolyzer_voltage=2;
    }

    if (fuel_cell_voltage<MIN_READING_ELECTROLYZER){
       // set_fuel_cell(0);
        fuel_cell_voltage=2;
    }
    
}
