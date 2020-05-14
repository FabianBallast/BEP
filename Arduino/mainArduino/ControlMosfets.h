#define ELECTROLYZER_MOSFET_PIN 5
#define FUEL_CELL_MOSFET_PIN    6
#define POWER_SUPPLY_MOSFET_PIN 7

void mosfets_setup(){
    pinMode(ELECTROLYZER_MOSFET_PIN, OUTPUT);
    pinMode(FUEL_CELL_MOSFET_PIN,    OUTPUT);
    pinMode(POWER_SUPPLY_MOSFET_PIN, OUTPUT);
}

void set_electrolyzer(byte set_value){
    analogWrite(ELECTROLYZER_MOSFET_PIN, set_value);
}

void set_fuel_cell(byte set_value){
    analogWrite(FUEL_CELL_MOSFET_PIN, set_value);
}


void set_power_supply(byte set_value){
    analogWrite(POWER_SUPPLY_MOSFET_PIN, set_value);
}
