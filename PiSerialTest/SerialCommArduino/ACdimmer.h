#include <RBDdimmer.h>  // add via arduino IDE, import from zipfile

// RobotDyn Dimmer Library
#define outputPin  11 // D0-D1, D3-D20         
#define zerocross  2 // (NOT CHANGABLE)   

dimmerLamp FanDimmer(outputPin); //initialase port for dimmer for MEGA, Leonardo, UNO, Arduino M0, Arduino Zero

int outVal = 0;

void fan_setup() {
  FanDimmer.begin(TOGGLE_MODE, ON); //dimmer initialisation: name.begin(MODE, STATE) 
 // dimmer.setState(OFF); for turning of
}

void set_fan_power(uint8_t set_value){
    if (set_value==0) {
        FanDimmer.setState(OFF);
    }
    else{
        FanDimmer.setState(ON);
        FanDimmer.setPower(set_value);
    }
}

uint8_t get_fan_power(){
    return FanDimmer.getPower();
}
