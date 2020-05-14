#define COMM_SIZE_A 3
#define COMM_SIZE_P 12


uint8_t comm_received[COMM_SIZE_A]; 
uint8_t data_to_send[COMM_SIZE_P] = {255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 254};     //index 0 and -1 are for communication protocal, DO NOT CHANGE
                                    //0   1  2  3  4  5  6  7  8  9 10   11
void serial_setup(){
  Serial.begin(9600);
  Serial.flush();
  
}

void comm_send(){
    Serial.write(data_to_send, COMM_SIZE_P);
}

int comm_read(){
   if (Serial.available() >= COMM_SIZE_A) {
    for (int n=0; n<COMM_SIZE_A; n++){
      comm_received[n] = Serial.read();
    }
    return 1;
  }
  return 0;
}
