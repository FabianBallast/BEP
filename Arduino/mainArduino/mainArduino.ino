#include "ACdimmer.h" 
#include "SerialComm.h"
#include "CurrentSensors.h"


void setup() {
  fan_setup();
  serial_setup();
  ammeters_setup();
}


void loop() {
  if (comm_read()){ 
    //data received
    set_fan_power(comm_received[0]);
  }
  
  
  read_ammeters();

  //collect all data to send
  data_to_send[1] = current_solar_panels;
  data_to_send[2] = current_wind_turbines;
  data_to_send[3] = current_ledload;
  data_to_send[4] = current_electrolyzer;
  data_to_send[5] = current_power_supply;
  data_to_send[6] = current_fuel_cell;
  data_to_send[7] = get_fan_power();

  
  comm_send();
  delay(100);
}
