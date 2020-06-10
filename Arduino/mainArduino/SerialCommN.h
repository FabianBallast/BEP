#define COMM_SIZE_A 4
#define COMM_SIZE_P 13


// extern float    current_solar_panels,  current_wind_turbines;
extern float current_ledload, current_electrolyzer, current_power_supply, current_fuel_cell;
extern float elapsedTime;
extern float current_to_add;
//extern byte turbine_pwm;
extern byte electrolyzer_pwm;
extern byte fuel_cell_pwm;
extern float wind_voltage;
extern float grid_voltage;

int i_send = -1;

extern byte wind_mosfet;
extern float grid_control_value;


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
      Serial.print("\"zonU\":");          Serial.print(solar_voltage);
      break;
    case 2:
      Serial.print(", \"loadI\":");         Serial.print(current_ledload);
      break;
    case 3:
      Serial.print(", \"windU\":");         Serial.print(wind_voltage);
      break;
    case 4:
      Serial.print(", \"FC_U\":");    Serial.print(fuel_cell_voltage);   
      break;
    case 5:
      Serial.print(", \"FC_Y\":");        Serial.print(fuel_cell_pwm);
      break;
    case 6:
      Serial.print(", \"EL_U\":"); Serial.print(electrolyzer_voltage);        
      break;
    case 7:
      Serial.print(", \"EL_I\":"); Serial.print(current_electrolyzer);
      break;
    case 8:
      Serial.print(", \"EL_Y\":");        Serial.print(electrolyzer_pwm);
      break;
    case 9:
      Serial.print(", \"gridU\":");         Serial.print(grid_voltage);   
      break;
    case 10:
      Serial.print(", \"gridX\":");   Serial.print(grid_control_value);
      break;
    case 11:
      Serial.print(", \"loopT\":");            Serial.print(elapsedTime);
      break;
    case 12:
      Serial.print(", \"PS_I\":"); Serial.print(current_power_supply);
      break;
    case 13:
      Serial.print(", \"fan\":");            Serial.print(get_fan_power());      
      break;      
    case 14:
      Serial.print(", \"windY\":");            Serial.print(wind_mosfet);      
      break;   
    case 15:
      Serial.print(", \"currAdd\":");            Serial.print(current_to_add);      
      break;   
    case 16:
      Serial.println("}ed");
      i_send = -1;
      break;
  }  
  i_send++;

//    case 4:
//      Serial.print(", \"OptWindI\":");     Serial.print(opt_wind_current);
//      break;
//      case 14:
//      Serial.print(", \"windX\":");   Serial.print(wind_control_value);   
//      break;
//    case 15:
//      Serial.print(", \"windY\":");     Serial.print(turbine_pwm);
//      break;
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
