#define ELECTROLYZER_MOSFET_PIN 5
#define FUEL_CELL_MOSFET_PIN    6
#define POWER_SUPPLY_MOSFET_PIN 7

byte pwm_value_electrolyzer;
byte pwm_value_fuel_cell;
byte pwm_value_power_supply;

void mosfets_setup(){
    pinMode(ELECTROLYZER_MOSFET_PIN, OUTPUT);
    pinMode(FUEL_CELL_MOSFET_PIN,    OUTPUT);
    pinMode(POWER_SUPPLY_MOSFET_PIN, OUTPUT);
}

void set_electrolyzer(float usage){
    //insert mapping 
    pwm_value_electrolyzer = 0;
    analogWrite(ELECTROLYZER_MOSFET_PIN, pwm_value_electrolyzer);
}

void set_fuel_cell(float production){
    //insert mapping 

    pwm_value_fuel_cell = 0;
    analogWrite(FUEL_CELL_MOSFET_PIN, pwm_value_fuel_cell);
}


void set_power_supply(float current_to_add){
    //insert mapping
    
    pwm_value_power_supply = 0;
    analogWrite(POWER_SUPPLY_MOSFET_PIN, pwm_value_power_supply);
}
