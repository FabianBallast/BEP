#define COMM_SIZE_A 3
#define COMM_SIZE_P 13

#define MULTIPLIER_SOLAR     6
#define MULTIPLIER_WIND      8
#define MULTIPLIER_FUEL_CELL 14

extern float    current_solar_panels,  current_wind_turbines,  current_ledload, current_electrolyzer, current_power_supply, current_fuel_cell;
extern float elapsedTime;
extern byte turbine_pwm;
extern byte electrolyzer_pwm;
extern byte fuel_cell_pwm;
extern float opt_wind_current;
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
      Serial.print("nd={");
      break;
    case 1:
      Serial.print("\"zonI\":");          Serial.print(current_solar_panels*MULTIPLIER_SOLAR);
      break;
    case 2:
      Serial.print(", \"windI\":");         Serial.print(current_wind_turbines*MULTIPLIER_WIND);
      break;
    case 3:
      Serial.print(", \"loadI\":");         Serial.print(current_ledload);
      break;
    case 4:
      Serial.print(", \"OptWindI\":");     Serial.print(opt_wind_current);
      break;
    case 5:
      Serial.print(", \"EL_I\":"); Serial.print(current_electrolyzer*MULTIPLIER_FUEL_CELL);
      break;
    case 6:
      Serial.print(", \"PS_I\":"); Serial.print(current_power_supply);
      break;
    case 7:
      Serial.print(", \"FC_I\":");    Serial.print(current_fuel_cell);          
      break;
    case 8:
      Serial.print(", \"fan\":");            Serial.print(get_fan_power());      
      break;
    case 9:
      Serial.print(", \"EL_U\":"); Serial.print(electrolyzer_voltage);        
      break;
    case 10:
      Serial.print(", \"FC_U\":");    Serial.print(fuel_cell_voltage);   
      break;
    case 11:
      Serial.print(", \"gridU\":");         Serial.print(grid_voltage);   
      break;
    case 12:
      Serial.print(", \"loopT\":");            Serial.print(elapsedTime);
      break;
    case 13:
      Serial.print(", \"gridX\":");   Serial.print(grid_control_value);
      break;
    case 14:
      Serial.print(", \"windX\":");   Serial.print(wind_control_value);   
      break;
    case 15:
      Serial.print(", \"windY\":");     Serial.print(turbine_pwm);
      break;
    case 16:
      Serial.print(", \"FC_Y\":");        Serial.print(fuel_cell_pwm);
      break;
    case 17:
      Serial.print(", \"EL_Y\":");        Serial.print(electrolyzer_pwm);
      break;      
    case 18:
      Serial.println("}ed");
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
