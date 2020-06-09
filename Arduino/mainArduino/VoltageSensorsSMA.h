#define N_FILTER_VOLTAGE 40
//A1-A6 wordt gebruikt voor currentsensors

//#define NOT USED  A7
//#define NOT USED  A8
#define GRID_VOLTAGE_READ1       A9
#define GRID_VOLTAGE_READ2       A10

#define ELECTROLYZER_VOLTAGE_READ_PLUS       A11
#define ELECTROLYZER_VOLTAGE_READ_MIN       A12

#define SOLAR_VOLTAGE_READ       A13
#define WIND_VOLTAGE_READ        A14
#define FUEL_CELL_VOLTAGE_READ   A15


int filter_readIndex_volt = 0; 

float electrolyzer_voltage; 
float fuel_cell_voltage; 
float wind_voltage;
float grid_voltage; 
float solar_voltage;

float current_solar_panels;
float current_wind_turbines;
float current_fuel_cell;



int rawEL   [N_FILTER_VOLTAGE];     
int rawFC   [N_FILTER_VOLTAGE];     
int rawWind [N_FILTER_VOLTAGE];     
int rawGrid [N_FILTER_VOLTAGE];     
int rawSolar[N_FILTER_VOLTAGE];     

float sumEL = 0;
float sumFC = 0;
float sumWind = 0;
float sumGrid = 0;
float sumSolar= 0;

uint16_t valueEL;
uint16_t valueFC;
uint16_t valueWind;
uint16_t valueGrid;
uint16_t valueSolar;


void setup_voltage_sensors(){
  pinMode(GRID_VOLTAGE_READ1,         INPUT);
  pinMode(GRID_VOLTAGE_READ2,         INPUT);
  pinMode(ELECTROLYZER_VOLTAGE_READ_PLUS, INPUT);
  pinMode(ELECTROLYZER_VOLTAGE_READ_MIN,  INPUT);
  pinMode(FUEL_CELL_VOLTAGE_READ,     INPUT);
  pinMode(SOLAR_VOLTAGE_READ,         INPUT);
pinMode(WIND_VOLTAGE_READ,          INPUT);

  

//  sumEL =  electrolyzer_voltage * N_FILTER_VOLTAGE;
//  sumFC =  fuel_cell_voltage    * N_FILTER_VOLTAGE;
//  sumWind  = wind_voltage         * N_FILTER_VOLTAGE;
//  sumGrid  = grid_voltage         * N_FILTER_VOLTAGE;
//  sumSolar = solar_voltage       * N_FILTER_VOLTAGE;
}

void check_H2_voltages(){

    valueEL = analogRead(ELECTROLYZER_VOLTAGE_READ_PLUS) - analogRead(ELECTROLYZER_VOLTAGE_READ_MIN); //na step down, direct naar electrolyzer
    valueFC    = analogRead(FUEL_CELL_VOLTAGE_READ); //na step down, direct naar fuel cell
    valueWind  = analogRead(WIND_VOLTAGE_READ);
    valueGrid =      0.0168*analogRead(GRID_VOLTAGE_READ1) - 0.0151*analogRead(GRID_VOLTAGE_READ2);
    valueSolar = analogRead(SOLAR_VOLTAGE_READ);


    sumEL = sumEL - rawEL[filter_readIndex_volt] + valueEL;
    sumFC = sumFC - rawFC[filter_readIndex_volt]  + valueFC;
    sumWind = sumWind - rawWind[filter_readIndex_volt] + valueWind;
    sumGrid = sumGrid - rawGrid[filter_readIndex_volt] + valueGrid;
    sumSolar = sumSolar -  rawSolar[filter_readIndex_volt] + valueSolar;



    rawEL[filter_readIndex_volt]    = valueEL;
    rawFC[filter_readIndex_volt]    = valueFC;
    rawWind[filter_readIndex_volt]  = valueWind;
    rawGrid[filter_readIndex_volt]  = valueGrid;
    rawSolar[filter_readIndex_volt] = valueSolar;
    


    // advance to the next position in the array:
    filter_readIndex_volt = filter_readIndex_volt + 1;
    if (filter_readIndex_volt >= N_FILTER_VOLTAGE) {
      filter_readIndex_volt = 0;
    }

    electrolyzer_voltage = sumEL / N_FILTER_VOLTAGE    /1000;
    fuel_cell_voltage = sumFC / N_FILTER_VOLTAGE       /1000;
    wind_voltage = sumWind / N_FILTER_VOLTAGE          /1000;
    grid_voltage = sumGrid / N_FILTER_VOLTAGE          /1000;
    solar_voltage = sumSolar / N_FILTER_VOLTAGE       /1000;        

    current_solar_panels = solar_voltage*3;
    current_wind_turbines = wind_voltage*3;
    current_fuel_cell     = fuel_cell_voltage*3;
    
    
}
