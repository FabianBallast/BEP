#include "ACdimmer.h" 
#include "SerialComm.h"
#include "CurrentSensors.h"
#include "ControlMosfets.h"
#include "FailSafes.h"

#define MULTIPLIER_SOLAR     3
#define MULTIPLIER_WIND      3
#define MULTIPLIER_FUEL_CELL 1

float mismatch; 

void setup() {
  mosfets_setup();
  fan_setup();
  serial_setup();
  ammeters_setup();
  pinMode(13, OUTPUT);
  digitalWrite(13, HIGH);
}


void loop() {
  if (comm_read()){ // data received, handle accordingly
    set_fan_power(comm_received[0]);
    /// TODO add turn off possiblity for fuel cell + electrolyzer
  }
  
  read_ammeters();
  
  set_power_supply(current_to_add());
 
  controlGrid();
  
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
  data_to_send[10]= 0;
  
  comm_send();
  delay(200);
}




float current_to_add(){
    return current_solar_panels * (MULTIPLIER_SOLAR - 1) + current_wind_turbines * (MULTIPLIER_WIND - 1) + current_fuel_cell * (MULTIPLIER_FUEL_CELL - 1);
}

void controlGrid(){
    mismatch = current_solar_panels + current_wind_turbines + current_power_supply - current_ledload;
    if (mismatch>0){
         set_electrolyzer(mismatch);
         set_fuel_cell(0);  
    }
    if (mismatch<0){
         set_electrolyzer(0);
         set_fuel_cell(-mismatch);
    }
    return mismatch;
}
