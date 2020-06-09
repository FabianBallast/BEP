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

#define MULTIPLIER_SOLAR     6
#define MULTIPLIER_WIND      8
#define MULTIPLIER_FUEL_CELL 14

unsigned long curr_time, prev_time;
float elapsedTime;

//float opt_wind_current = 10;

void setup() {
  serial_setup();
  fan_setup();   //MOET ALS EERSTE; KAN NIET EERST NOG IETS GEPRINT WORDEN OVER SERIAL
  setup_voltage_sensors();
  
  Serial.print("Setting up \n");
  mosfets_setup(); //set to off state for calibrating
  
  ammeters_setup(); //CALIBRATES; ONLY USE WHEN MOSFETS ARE IN OFF-STATE


  fan_start();

  Serial.print("Setup done \n");
}


void loop() {
  if (comm_read()){ // data received, handle accordingly
    set_fan_power(comm_received[0]);
    //opt_wind_current = comm_received[1]; ///add scaling;
    
    /// TODO add turn off possiblity for fuel cell + electrolyzer
  }
  
  read_ammeters();
  
  /////////////////CONTROL SYSTEM WITH PID'S
  curr_time = millis();
  elapsedTime = (float)(curr_time - prev_time);

  //METHOD 1: CONTROL VOLTAGE
//  grid_control_value = controlGrid(11.9);
 /// controlPowerSupply(current_to_add());
  
  //METHOD 2: CONTROL CURRENT
  //tot_curr = 
  //mismatch = tot_curr - current_electrolyzer - current_ledload;
  
  grid_control_value = controlGridCurrent(current_total());
  read_ammeters();
  processControlValue(grid_control_value);
  read_ammeters();
//  controlWind(opt_wind_current);
  read_ammeters();
  
  prev_time = curr_time;
 // processControlValue(control_value);
 
  //////////////////////////////////
  check_H2_voltages();
  read_ammeters();

  //collect all data to send
  comm_send();
  
}

float current_total(){
    return current_solar_panels * MULTIPLIER_SOLAR + current_wind_turbines * MULTIPLIER_WIND + current_fuel_cell * MULTIPLIER_FUEL_CELL;
}
float current_to_add(){
    return current_solar_panels * (MULTIPLIER_SOLAR - 1) + current_wind_turbines * (MULTIPLIER_WIND - 1) + current_fuel_cell * (MULTIPLIER_FUEL_CELL - 1);
}
