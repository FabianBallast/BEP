#include "ACdimmer.h" 

#include "ControlMosfets.h"
#include "FailSafes.h"

//USE ONLY ONE OF THE TWO BELOW
//#include "SerialComm.h"
#include "SerialCommN.h"

//USE ONLY ONE OF THE TWO BELOW
//#include "CurrentSensorsEMA.h"
#include "CurrentSensorSMA.h"

//########################
//#include <RBDdimmer.h>
//#define dimmer_outPin  8 // D8 / D9 voor 2e output    
//#define zerocross  2 // (NOT CHANGABLE)   
//dimmerLamp FanDimmer(dimmer_outPin); 

#define PRINT_EACH_X_LOOPS 1

#define MULTIPLIER_SOLAR     3
#define MULTIPLIER_WIND      3
#define MULTIPLIER_FUEL_CELL 1

unsigned long curr_time, prev_time;
float elapsedTime;

float opt_wind_current = 10;

void setup() {
  serial_setup();
  fan_setup();   //MOET ALS EERSTE; KAN NIET EERST NOG IETS GEPRINT WORDEN OVER SERIAL

  Serial.print("Setting up \n");
  mosfets_setup(); //set to off state for calibrating
  
//  ammeters_setup(); //CALIBRATES; ONLY USE WHEN MOSFETS ARE IN OFF-STATE


  fan_start();

  Serial.print("Setup done \n");
}

int i_send = 0;

void loop() {
  if (comm_read()){ // data received, handle accordingly
  //  set_fan_power(comm_received[0]);
    opt_wind_current = comm_received[1]; ///add scaling;
    
    /// TODO add turn off possiblity for fuel cell + electrolyzer
  }
  
  read_ammeters();

  /////////////////CONTROL SYSTEM WITH PID'S
  curr_time = millis();
  elapsedTime = (float)(curr_time - prev_time);

  //METHOD 1: CONTROL VOLTAGE
  //grid_control_value = controlGrid(11.9);
  //controlPowerSupply(current_to_add());
  
  //METHOD 2: CONTROL CURRENT
  //grid_control_value = controlGridCurrent(current_total());
  
  //controlWind(opt_wind_current);

  
  prev_time = curr_time;
 // processControlValue(control_value);
 
  //////////////////////////////////
  check_H2_voltages();

  //collect all data to send
  i_send++;

  if (i_send == PRINT_EACH_X_LOOPS){
    i_send = 0;
    comm_send();
  }
}

float current_total(){
    return current_solar_panels * MULTIPLIER_SOLAR + current_wind_turbines * MULTIPLIER_WIND + current_fuel_cell * MULTIPLIER_FUEL_CELL;
}
float current_to_add(){
    return current_solar_panels * (MULTIPLIER_SOLAR - 1) + current_wind_turbines * (MULTIPLIER_WIND - 1) + current_fuel_cell * (MULTIPLIER_FUEL_CELL - 1);
}
