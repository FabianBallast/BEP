#define voltage_measurer A7

#define ELECTROLYZER_MOSFET_PIN 5
#define FUEL_CELL_MOSFET_PIN    6
#define POWER_SUPPLY_MOSFET_PIN 7

#define VALVE_PIN 8

byte electrolyzer_pwm;
byte fuel_cell_pwm;
byte pwm_value_power_supply;

byte Kp = 3;
byte Ki = 2;
byte Kd = 1;

unsigned long curr_time, prev_time;
float elapsedTime;
float curr_volt;
float curr_volt_error, prev_volt_error;
float control_value;
float cum_volt_error, rate_volt_error;


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
    curr_volt = analogRead(voltage_measurer) * 5/1024;
    curr_time = millis();
    elapsedTime = (float)(curr_time - prev_time);
    curr_volt_error = target_volt - curr_volt;
    cum_volt_error += curr_volt_error * elapsedTime;
    rate_volt_error = (curr_volt_error - prev_volt_error)/elapsedTime;
    
    control_value = Kp*curr_volt_error + Ki*cum_volt_error + Kd*rate_volt_error;

    prev_volt_error = curr_volt_error;
    prev_time = curr_time;
    return control_value;
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
