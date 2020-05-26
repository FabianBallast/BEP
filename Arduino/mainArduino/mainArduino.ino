#include "ACdimmer.h" 
#include "ControlMosfets.h"
#include "FailSafes.h"

//USE ONLY ONE OF THE TWO BELOW
//#include "SerialComm.h"
#include "SerialCommN.h"

//USE ONLY ONE OF THE TWO BELOW
//#include "CurrentSensorsEMA.h"
#include "CurrentSensorSMA.h"


#define PRINT_EACH_X_LOOPS 1

unsigned long curr_time, prev_time;
float elapsedTime;

float opt_wind_current = 10;

void setup() {
  serial_setup();
  Serial.print("Setting up \n");
  mosfets_setup(); //set to off state for calibrating
  //fan_setup();   ///WORKS ONLY WHEN FAN IS CONNECTED

  ammeters_setup(); //CALIBRATES; ONLY USE WHEN MOSFETS ARE IN OFF-STATE


 // fan_start();
 // pinMode(13, OUTPUT);
 // digitalWrite(13, HIGH);

  Serial.print("Setup done \n");
}

int i_send = 0;

void loop() {
  if (comm_read()){ // data received, handle accordingly
    set_fan_power(comm_received[0]);
    opt_wind_current = comm_received[1]; ///add scaling;
    
    /// TODO add turn off possiblity for fuel cell + electrolyzer
  }
  
  read_ammeters();

  curr_time = millis();
  elapsedTime = (float)(curr_time - prev_time);
  
  grid_control_value = controlGrid(11.9);
  controlWind(opt_wind_current);
  
  prev_time = curr_time;
 // processControlValue(control_value);
  
  check_H2_voltages();

  //collect all data to send
  i_send++;

  if (i_send == PRINT_EACH_X_LOOPS){
    i_send = 0;
    comm_send();
  }
}
