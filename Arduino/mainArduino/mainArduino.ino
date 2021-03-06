#include "ACdimmer.h" 
#include "VoltageSensorsSMA.h"
#include "ControlMosfets.h"


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

#define MULTIPLIER_SOLAR     20.0
#define MULTIPLIER_WIND      0.3
#define MULTIPLIER_FUEL_CELL 14.0


#define TURIBNE_MOSFET_PIN      10

unsigned long curr_time, prev_time;
float elapsedTime;

byte wind_mosfet;
int H2Ref = 0;
byte fanRef;
float current_to_add;

// float grid_control_value;

//float opt_wind_current = 10;

void setup() {
  serial_setup();
  fan_setup();   //MOET ALS EERSTE; KAN NIET EERST NOG IETS GEPRINT WORDEN OVER SERIAL
  setup_voltage_sensors();
  
  Serial.print("Setting up \n");
  mosfets_setup(); //set to off state for calibrating
  
  ammeters_setup(); //CALIBRATES; ONLY USE WHEN MOSFETS ARE IN OFF-STATE

  //calibrates, now turn on power supply
  analogWrite(POWER_SUPPLY_MOSFET_PIN, 255);
 // analogWrite(6, 0);
  fan_start();

  Serial.print("Setup done \n");
}


void loop() {
  analogWrite(7, 255);   ///change later
  
  if (comm_read()){ // data received, handle accordingly
    
    fanRef = comm_received[0];
    H2Ref = (int)comm_received[1] - 128;
    set_fan_power(fanRef);
    wind_mosfet = comm_received[2];
    analogWrite(TURIBNE_MOSFET_PIN, wind_mosfet);

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
  read_ammeters();
  read_ammeters();
  
  //grid_control_value = H2Ref - 50; ///delete later
  processControlValue(H2Ref);
//  controlWind(opt_wind_current);

  
  prev_time = curr_time;
 // processControlValue(control_value);
 
  //////////////////////////////////
  check_voltages();

  comm_send();
  
}
