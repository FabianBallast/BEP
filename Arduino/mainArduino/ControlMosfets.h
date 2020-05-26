#define voltage_measurer A7

#define ELECTROLYZER_MOSFET_PIN 5
#define FUEL_CELL_MOSFET_PIN    6
#define POWER_SUPPLY_MOSFET_PIN 7
#define TURIBNE_MOSFET_PIN      10

#define VALVE_PIN 8

byte electrolyzer_pwm;
byte fuel_cell_pwm;
byte pwm_value_power_supply;
byte turbine_pwm;

byte Kp_grid = 3;
byte Ki_grid = 2;
byte Kd_grid = 1;

byte Kp_wind = 3;
byte Ki_wind = 2;
byte Kd_wind = 1;

extern float elapsedTime;

extern float grid_voltage; 
float curr_volt_error, prev_volt_error;
float grid_control_value;
float cum_volt_error, rate_volt_error;

extern float current_wind_turbines;

float curr_wind_error, prev_wind_error;
float wind_control_value;
float cum_wind_error, rate_wind_error;


void mosfets_setup(){
    pinMode(ELECTROLYZER_MOSFET_PIN, OUTPUT);
    pinMode(FUEL_CELL_MOSFET_PIN,    OUTPUT);
    pinMode(POWER_SUPPLY_MOSFET_PIN, OUTPUT);
 

    analogWrite(ELECTROLYZER_MOSFET_PIN, 0);
    analogWrite(FUEL_CELL_MOSFET_PIN, 0);
    analogWrite(POWER_SUPPLY_MOSFET_PIN, 0);
    digitalWrite(VALVE_PIN, LOW);
}

float controlGrid(float target_volt){
  
    curr_volt_error = target_volt - grid_voltage;
    cum_volt_error += curr_volt_error * elapsedTime;
    rate_volt_error = (curr_volt_error - prev_volt_error)/elapsedTime;
    
    grid_control_value = Kp_grid*curr_volt_error + Ki_grid*cum_volt_error + Kd_grid*rate_volt_error;

    prev_volt_error = curr_volt_error;

    return grid_control_value;
}

float controlWind(float target_current){
    //curr_volt = analogRead(voltage_measurer) * 5/1024;
    
    curr_wind_error = target_current - current_wind_turbines;
    cum_wind_error += curr_wind_error * elapsedTime;
    rate_wind_error = (curr_wind_error - prev_wind_error)/elapsedTime;
    
    wind_control_value = Kp_wind*curr_wind_error + Ki_wind*cum_wind_error + Kd_wind*rate_wind_error;
    turbine_pwm = map(wind_control_value, -100, 100, 0, 255);
    if (turbine_pwm<=0){
       turbine_pwm = 0;
    }
    if (turbine_pwm>=255){
       turbine_pwm = 255;
    }

    prev_wind_error = curr_wind_error;

    analogWrite(TURIBNE_MOSFET_PIN, turbine_pwm);
    return wind_control_value, turbine_pwm;
}

void openValve(byte valve_open_time){
    digitalWrite(VALVE_PIN, HIGH);
    delay(valve_open_time);
    digitalWrite(VALVE_PIN, LOW);
}

void processControlValue(float control_value){
    if (control_value>0){
      //fuel_cell_pwm = map(control_value,..., ...., ...,...);
      fuel_cell_pwm = 255;

      analogWrite(FUEL_CELL_MOSFET_PIN, fuel_cell_pwm);
      analogWrite(ELECTROLYZER_MOSFET_PIN,0);

      //valve_open_time = map(fuel_cell_pwm,...,...,...);
      float valve_open_time = elapsedTime*0.015;
      openValve(valve_open_time);
      
    }
    else if (control_value<0){
      //electrolyzer_pwm = map(..., ...., ...,...);
      electrolyzer_pwm = 255;
      
      analogWrite(FUEL_CELL_MOSFET_PIN, 0);
      analogWrite(ELECTROLYZER_MOSFET_PIN,electrolyzer_pwm);
    }
}
