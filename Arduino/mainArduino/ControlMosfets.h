#define voltage_measurer A7

#define ELECTROLYZER_MOSFET_PIN 5
#define FUEL_CELL_MOSFET_PIN    6
#define POWER_SUPPLY_MOSFET_PIN 7

byte pwm_value_electrolyzer;
byte pwm_value_fuel_cell;
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
