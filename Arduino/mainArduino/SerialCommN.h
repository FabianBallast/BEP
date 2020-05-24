#define COMM_SIZE_A 3
#define COMM_SIZE_P 13


uint8_t comm_received[COMM_SIZE_A]; 
uint8_t data_to_send[COMM_SIZE_P] = {255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 254};     //index 0 and -1 are for communication protocal, DO NOT CHANGE
                                    //0   1  2  3  4  5  6  7  8  9  10 11  12
void serial_setup(){
  Serial.begin(9600);
  Serial.flush();
  
}

void comm_send(){
  Serial.print("newdata={");
  
  Serial.print("\"solar_current\":");          Serial.print(current_solar_panels);
  Serial.print(", \"wind_current\":");         Serial.print(current_wind_turbines);
  Serial.print(", \"load_current\":");         Serial.print(current_ledload);
  Serial.print(", \"electrolyzer_current\":"); Serial.print(current_electrolyzer);
  Serial.print(", \"power_supply_current\":"); Serial.print(current_power_supply);
  Serial.print(", \"fuel_cell_current\":");    Serial.print(current_fuel_cell);          
  Serial.print(", \"fan_power\":");            Serial.print(get_fan_power());      
  Serial.print(", \"electrolyzer_voltage\":"); Serial.print(electrolyzer_voltage);        
  Serial.print(", \"fuel_cell_voltage\":");    Serial.print(fuel_cell_voltage);   
  Serial.print(", \"control_value\":");        Serial.print(control_value);   
    
  Serial.println("}enddata");
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
