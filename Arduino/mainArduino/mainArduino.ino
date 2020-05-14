#include "ACdimmer.h" 
#include "SerialComm.h"
#include "CurrentSensors.h"
#include "ControlMosfets.h"
#include "FailSafes.h"

void setup() {
  mosfets_setup();
  fan_setup();
  serial_setup();
  ammeters_setup();
  pinMode(13, OUTPUT);
  digitalWrite(13, HIGH);
}


void loop() {
  if (comm_read()){ // then data received
    set_fan_power(comm_received[0]);
    ///add turn off possiblity for fuel cell + electrolyzer
  }
  
  
  read_ammeters();
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

  set_electrolyzer(20);
  set_fuel_cell(20);
  set_power_supply(20);
  
  comm_send();
  delay(200);
}
