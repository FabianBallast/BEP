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
    /// TODO add turn off possiblity for fuel cell + electrolyzer
  }
  
  read_ammeters();

 // control_value = controlGrid(11.9);
 // processControlValue(control_value);
  
  check_H2_voltages();

  //collect all data to send
  i_send++;

  if (i_send == PRINT_EACH_X_LOOPS){
    i_send = 0;
    data_to_send[1] = current_solar_panels;
    data_to_send[2] = current_wind_turbines;
    data_to_send[3] = current_ledload;
    data_to_send[4] = current_electrolyzer;
    data_to_send[5] = current_power_supply;
    data_to_send[6] = current_fuel_cell;
    data_to_send[7] = get_fan_power();
    data_to_send[8] = electrolyzer_voltage;
    data_to_send[9] = fuel_cell_voltage;
    data_to_send[10]= control_value;
    data_to_send[11]= 0;
  
    comm_send();
  }
  delay(10);
}
