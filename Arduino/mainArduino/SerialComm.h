#define COMM_SIZE_A 3
#define COMM_SIZE_P 4


uint8_t comm_received[COMM_SIZE_A];
uint8_t data_to_send[COMM_SIZE_P];

void serial_setup(){
  Serial.begin(9600);
  Serial.flush();
  
  data_to_send[0] = 255;  //for communication protocal, DO NOT CHANGE
  data_to_send[1] = 0;
  data_to_send[2] = 0;
  data_to_send[3] = 254; //for communication protocal, DO NOT CHANGE
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
