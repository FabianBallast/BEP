
//A1-A6 wordt gebruikt voor currentsensors

#define ELECTROLYZER_VOLTAGE_READ  A7
#define FUEL_CELL_VOLTAGE_READ  A8
#define GRID_VOLTAGE_READ1       A9
#define GRID_VOLTAGE_READ2       A10
#define TURBINE_VOLTAGE_READ      A8
#define MAX_READING_ELECTROLYZER   (2.0/5.0)*2014
#define MIN_READING_ELECTROLYZER   (0.9/5.0)*2014

uint16_t electrolyzer_voltage; 
uint16_t fuel_cell_voltage; 
float wind_voltage;
float grid_voltage; 

void setup_voltage_sensors(){
  pinMode(ELECTROLYZER_VOLTAGE_READ, INPUT);
  pinMode(FUEL_CELL_VOLTAGE_READ,    INPUT);
  pinMode(GRID_VOLTAGE_READ1,         INPUT);
  pinMode(GRID_VOLTAGE_READ2,         INPUT);
  pinMode(TURBINE_VOLTAGE_READ,       INPUT);
}

void check_H2_voltages(){

    electrolyzer_voltage = analogRead(ELECTROLYZER_VOLTAGE_READ); //na step down, direct naar electrolyzer
    fuel_cell_voltage    = analogRead(FUEL_CELL_VOLTAGE_READ); //na step down, direct naar fuel cell
    wind_voltage         = analogRead(TURBINE_VOLTAGE_READ);

    grid_voltage = 0.0168*analogRead(GRID_VOLTAGE_READ1) - 0.0151*analogRead(GRID_VOLTAGE_READ2);

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
