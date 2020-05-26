#define COMM_SIZE_A 3
#define COMM_SIZE_P 12


uint8_t comm_received[COMM_SIZE_A]; 
uint8_t data_to_send[COMM_SIZE_P] = {255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 254};     //index 0 and -1 are for communication protocal, DO NOT CHANGE
                                    //0   1  2  3  4  5  6  7  8  9  10 11  12
void serial_setup(){
  Serial.begin(9600);
  Serial.flush();
  
}

void comm_send(){
  //    data_to_send[1] = current_solar_panels;
//    data_to_send[2] = current_wind_turbines;
//    data_to_send[3] = current_ledload;
//    data_to_send[4] = current_electrolyzer;
//    data_to_send[5] = current_power_supply;
//    data_to_send[6] = current_fuel_cell;
//    data_to_send[7] = get_fan_power();
//    data_to_send[8] = electrolyzer_voltage;
//    data_to_send[9] = fuel_cell_voltage;
//    data_to_send[10]= control_value;
//    data_to_send[11]= 0;
    Serial.write(data_to_send, COMM_SIZE_P);
}

int comm_read(){
   if (Serial.available() >= COMM_SIZE_A) {
    for (int n=0; n<COMM_SIZE_A; n++){
      comm_received[n] = Serial.read();
    }
    return 1;
  }
  return 0;
}
