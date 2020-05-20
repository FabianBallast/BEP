#include "ACdimmer.h" 
//#include "CurrentSensors.h"
#include "CurrentSensorBackup.h"
#include "ControlMosfets.h"
#include "FailSafes.h"

//#include "SerialComm.h"
#include "SerialCommN.h"




void setup() {
  mosfets_setup(); //set to off state for calibrating
  fan_setup();
  serial_setup();
  ammeters_setup();


  fan_start();
  pinMode(13, OUTPUT);
  digitalWrite(13, HIGH);
}


void loop() {
  if (comm_read()){ // data received, handle accordingly
    set_fan_power(comm_received[0]);
    /// TODO add turn off possiblity for fuel cell + electrolyzer
  }
  
  read_ammeters();

  control_value = controlGrid(11.9);
  
  check_H2_voltages();

  //collect all data to send
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
  delay(10);
}
