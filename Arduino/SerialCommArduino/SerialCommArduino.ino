#include "ACdimmer.h" 

#define COMM_SIZE_A 3
#define COMM_SIZE_P 4


uint8_t comm_received[COMM_SIZE_A];
uint8_t comm_sent[COMM_SIZE_P];

void setup() {
  Serial.begin(9600);
  Serial.flush();
  fan_setup();

  comm_sent[0] = 255;  //for communication protocal, DO NOT CHANGE
  comm_sent[1] = 0;
  comm_sent[2] = 0;
  comm_sent[3] = 254; //for communication protocal, DO NOT CHANGE
}
void loop() {
//  comm_array[0] = 2;
//  comm_array[1] = 1;
//  comm_array[2] = 3;
 
 comm_sent[1] = 0;
 if (Serial.available() >= COMM_SIZE_A) {
    for (int n=0; n<COMM_SIZE_A; n++){
      comm_received[n] = Serial.read();
    }
    set_fan_power(comm_received[0]);
    comm_sent[2] = 1;
   }
  
  
  
  comm_sent[1] = get_fan_power();
  
  Serial.write(comm_sent, COMM_SIZE_P);
  delay(100);
}
