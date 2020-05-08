
#ifndef _ACDIMMER_H_
#define _ACDIMMER_H_


#include <RBDdimmer.h>

#define outputPin  11 // D0-D1, D3-D20         
#define zerocross  2 // (NOT CHANGABLE)   

dimmerLamp FanDimmer(outputPin); 


void fan_setup() {
  FanDimmer.begin(TOGGLE_MODE, ON); 
  FanDimmer.setPower(80);
  FanDimmer.setState(ON);
}

void set_fan_power(byte set_value){
 

        FanDimmer.setPower(set_value);
   // }
}

uint8_t get_fan_power(){
    return FanDimmer.getPower();
}

#endif // _ACDIMMER_H_ 
