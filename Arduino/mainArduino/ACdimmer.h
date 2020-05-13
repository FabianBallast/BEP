
#ifndef _ACDIMMER_H_
#define _ACDIMMER_H_


#include <RBDdimmer.h>

#define dimmer_outPin  8 // D8 / D9 voor 2e output    
#define zerocross  2 // (NOT CHANGABLE)   

dimmerLamp FanDimmer(dimmer_outPin); 


void fan_setup() {
  FanDimmer.begin(NORMAL_MODE, ON); 
  FanDimmer.setPower(80);
  FanDimmer.setState(ON);
}

void set_fan_power(byte set_value){
  set_value = map(set_value, 0, 100, 15, 95);
  FanDimmer.setPower(set_value);
}

uint8_t get_fan_power(){
    return FanDimmer.getPower();
}

#endif // _ACDIMMER_H_ 
