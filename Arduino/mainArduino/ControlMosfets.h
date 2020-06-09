#define voltage_measurer A7

#define ELECTROLYZER_MOSFET_PIN 5
#define FUEL_CELL_MOSFET_PIN    6
#define POWER_SUPPLY_MOSFET_PIN 7
#define TURIBNE_MOSFET_PIN      10
#define VALVE_PIN               12

#define valveOpenTime           50

#define MAX_READING_ELECTROLYZER   (2.0/5.0)*2014.0
#define MIN_READING_ELECTROLYZER   (0.9/5.0)*2014.0


bool valveOpen = false;
unsigned long lastValveSwitch;
int valveMillOpenFreq = 100;

extern float elapsedTime;

extern float electrolyzer_voltage, fuel_cell_voltage;


//GRID PID VOLTage
byte Kp_grid = 3;
byte Ki_grid = 2;
byte Kd_grid = 1;

extern float grid_voltage; 
float curr_flow_error, prev_flow_error;
float grid_control_value;
float cum_flow_error, rate_flow_error;
byte fuel_cell_pwm;
byte electrolyzer_pwm;

//extern float grid_voltage; 
//float curr_volt_error, prev_volt_error;
//float grid_control_value;
//float cum_volt_error, rate_volt_error;
//byte fuel_cell_pwm;
//byte electrolyzer_pwm;

//GRID PID CURRENT
//byte Kp_ps_h2 = 3;
//byte Ki_ps_h2 = 2;
//byte Kd_ps_h2 = 1;


//TURBINE PID
//byte Kp_wind = 3;
//byte Ki_wind = 2;
//byte Kd_wind = 1;
//extern float current_wind_turbines;
//float curr_wind_error, prev_wind_error;
//float wind_control_value;
//float cum_wind_error, rate_wind_error;
//byte turbine_pwm;

//POWER SUPPLY PID
//byte Kp_ps = 0.03;
//byte Ki_ps = 0.02;
//byte Kd_ps = 0.01;
//extern float current_power_supply;
//float curr_ps_error, prev_ps_error;
//float ps_control_value;
//float cum_ps_error, rate_ps_error;
//byte pwm_value_power_supply;




void mosfets_setup(){
    pinMode(ELECTROLYZER_MOSFET_PIN, OUTPUT);
    pinMode(FUEL_CELL_MOSFET_PIN,    OUTPUT);
    pinMode(POWER_SUPPLY_MOSFET_PIN, OUTPUT);
    pinMode(TURIBNE_MOSFET_PIN,      OUTPUT);

 

    analogWrite(ELECTROLYZER_MOSFET_PIN, 0);
    analogWrite(FUEL_CELL_MOSFET_PIN, 0);
    analogWrite(POWER_SUPPLY_MOSFET_PIN, 0);
    analogWrite(TURIBNE_MOSFET_PIN, 0);
    digitalWrite(VALVE_PIN, LOW);

    lastValveSwitch = millis();
}

float controlGridFlow(float grid_flow, float target_flow){
    curr_flow_error = target_flow - grid_flow;
    cum_flow_error += curr_flow_error * elapsedTime;
    rate_flow_error = (curr_flow_error - prev_flow_error)/elapsedTime;
    
    grid_control_value = Kp_grid*curr_flow_error + Ki_grid*cum_flow_error + Kd_grid*rate_flow_error;

    prev_flow_error = curr_flow_error;
    return grid_control_value;
}
//
//
//float controlGridCurrent(float target_current_ps){
////    pwm_value_power_supply = 255;
////    analogWrite(POWER_SUPPLY_MOSFET_PIN, pwm_value_power_supply);
//  
//    curr_ps_error = target_current_ps - current_power_supply;
//    cum_ps_error += curr_ps_error * elapsedTime;
//    rate_ps_error = (curr_ps_error - prev_ps_error)/elapsedTime;
//    
//    grid_control_value = Kp_ps_h2*curr_ps_error + Ki_ps_h2*cum_ps_error + Kd_ps_h2*rate_ps_error;
//    
//    prev_ps_error = curr_ps_error;
//    return grid_control_value;
//}

//float controlWind(float target_current){
//    analogWrite(TURBINE_START_PIN, 255);
//    
//    curr_wind_error = target_current - current_wind_turbines;
//    cum_wind_error += curr_wind_error * elapsedTime;
//    rate_wind_error = (curr_wind_error - prev_wind_error)/elapsedTime;
//    
//    wind_control_value = Kp_wind*curr_wind_error + Ki_wind*cum_wind_error + Kd_wind*rate_wind_error;
//    turbine_pwm = map(wind_control_value, -100, 100, 0, 255);
//    if (turbine_pwm<=0)
//       turbine_pwm = 0;
//    if (turbine_pwm>=255)
//       turbine_pwm = 255;
//
//    prev_wind_error = curr_wind_error;
//
//    if (get_fan_power() < 5)
//      analogWrite(TURBINE_START_PIN, 0);
//    else
//      analogWrite(TURBINE_START_PIN, 255);
//
//    analogWrite(TURIBNE_MOSFET_PIN, turbine_pwm);
//    return wind_control_value, turbine_pwm;
//}


//float controlPowerSupply(float target_current_ps){
//    curr_ps_error = target_current_ps - current_power_supply;
//    cum_ps_error += curr_ps_error * elapsedTime;
//    rate_ps_error = (curr_ps_error - prev_ps_error)/elapsedTime;
//    
//    ps_control_value = Kp_ps*curr_ps_error + Ki_ps*cum_ps_error + Kd_ps*rate_ps_error;
//    pwm_value_power_supply = map(ps_control_value, -100, 100, 0, 255);
//    if (pwm_value_power_supply<=0)
//       pwm_value_power_supply = 0;
//    if (pwm_value_power_supply>=255)
//       pwm_value_power_supply = 255;
//
//    prev_ps_error = curr_ps_error;
//
//    pwm_value_power_supply = 255;
//
//    analogWrite(POWER_SUPPLY_MOSFET_PIN, pwm_value_power_supply);
//    return ps_control_value, pwm_value_power_supply;
//}

void controlValve(){
        
      if (!valveOpen && (lastValveSwitch - millis() > valveMillOpenFreq)){
          valveOpen = true;
          lastValveSwitch = millis();
          digitalWrite(VALVE_PIN, HIGH);
      }
      else if (valveOpen && (lastValveSwitch - millis() > valveOpenTime)){
          valveOpen = false;
          lastValveSwitch = millis();
          digitalWrite(VALVE_PIN, LOW);
      }
}

void processControlValue(float control_value){
    if (control_value>0){
      //fuel_cell_pwm = map(control_value,..., ...., ...,...);
      fuel_cell_pwm = 255;

     valveMillOpenFreq = map(fuel_cell_pwm,0,255,100, 0);
     controlValve();
     
      
    }
    else if (control_value<0){
      //electrolyzer_pwm = map(..., ...., ...,...);
      electrolyzer_pwm = 255;
    }

    if (electrolyzer_voltage>MAX_READING_ELECTROLYZER){
      electrolyzer_pwm = 0;
    }
    if (fuel_cell_voltage<MIN_READING_ELECTROLYZER){
        fuel_cell_pwm  = 0;
    }
    
    analogWrite(FUEL_CELL_MOSFET_PIN,   fuel_cell_pwm);
    analogWrite(ELECTROLYZER_MOSFET_PIN,electrolyzer_pwm);
}
