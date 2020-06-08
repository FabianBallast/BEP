#define COMM_SIZE_A 3
#define COMM_SIZE_P 13


extern float    current_solar_panels,  current_wind_turbines,  current_ledload, current_electrolyzer, current_power_supply, current_fuel_cell;
extern float elapsedTime;
extern byte turbine_pwm;
extern byte electrolyzer_pwm;
extern byte fuel_cell_pwm;

extern float grid_voltage;

int i_send = -1;

uint8_t comm_received[COMM_SIZE_A]; 
uint8_t data_to_send[COMM_SIZE_P] = {255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 254};     //index 0 and -1 are for communication protocal, DO NOT CHANGE
                                    //0   1  2  3  4  5  6  7  8  9  10 11  12
void serial_setup(){
  Serial.begin(9600);
  Serial.flush();
  
}

void comm_send(){
  switch (i_send){
    case 0:
      Serial.print("newdata={");
      break;
    case 1:
      Serial.print("\"solar_current\":");          Serial.print(current_solar_panels);
      break;
    case 2:
      Serial.print(", \"wind_current\":");         Serial.print(current_wind_turbines);
      break;
    case 3:
      Serial.print(", \"load_current\":");         Serial.print(current_ledload);
      break;
    case 4:
      Serial.print(", \"opt_wind_current\":");     Serial.print(opt_wind_current);
      break;
    case 5:
      Serial.print(", \"electrolyzer_current\":"); Serial.print(current_electrolyzer);
      break;
    case 6:
      Serial.print(", \"power_supply_current\":"); Serial.print(current_power_supply);
      break;
    case 7:
      Serial.print(", \"fuel_cell_current\":");    Serial.print(current_fuel_cell);          
      break;
    case 8:
      Serial.print(", \"fan_power\":");            Serial.print(get_fan_power());      
      break;
    case 9:
      Serial.print(", \"electrolyzer_voltage\":"); Serial.print(electrolyzer_voltage);        
      break;
    case 10:
      Serial.print(", \"fuel_cell_voltage\":");    Serial.print(fuel_cell_voltage);   
      break;
    case 11:
      Serial.print(", \"grid_voltage\":");         Serial.print(grid_voltage);   
      break;
    case 12:
      Serial.print(", \"loop_time\":");            Serial.print(elapsedTime);
      break;
    case 13:
      Serial.print(", \"grid_control_value\":");   Serial.print(grid_control_value);
      break;
    case 14:
      Serial.print(", \"wind_control_value\":");   Serial.print(wind_control_value);   
      break;
    case 15:
      Serial.print(", \"wind_control_pwm\":");     Serial.print(turbine_pwm);
      break;
    case 16:
      Serial.print(", \"fuel_cell_pwm\":");        Serial.print(fuel_cell_pwm);
      break;
    case 17:
      Serial.print(", \"electrolyzer_pwm\":");        Serial.print(electrolyzer_pwm);
      break;      
    case 18:
      Serial.println("}enddata");
      i_send = -1;
      break;
  }  
  i_send++;
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
