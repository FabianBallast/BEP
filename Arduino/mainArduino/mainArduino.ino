#include "ACdimmer.h" 
#include "SerialComm.h"
#include "CurrentSensors.h"


void setup() {
  fan_setup();
  serial_setup();
}


void loop() {
  if (comm_read()){ 
    //data received
    set_fan_power(comm_received[0]);
  }
  
  //collect all data to send
  
  data_to_send[1] = get_current_solar_panels();
  data_to_send[2] = get_current_wind_turbine();
  data_to_send[3] = get_current_fuel_cell();
  data_to_send[4] = get_fan_power();

  
  
  
  comm_send();
  delay(100);
}
