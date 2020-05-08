#define COMM_SIZE_A 9
#define COMM_SIZE_P 3

uint8_t comm_received[COMM_SIZE_A];
uint8_t comm_sent[COMM_SIZE_P];

void setup() {
  Serial.begin(9600);
  Serial.flush();
}
void loop() {
//  comm_array[0] = 2;
//  comm_array[1] = 1;
//  comm_array[2] = 3;
  
 while (Serial.available() < COMM_SIZE_A) {}
 for (int n=0; n<COMM_SIZE_A; n++)
    comm_received[n] = Serial.read();
 
  comm_sent[0] = comm_received[0] + comm_received[1] + comm_received[2];
  comm_sent[1] = comm_received[3] + comm_received[4] + comm_received[5];
  comm_sent[2] = comm_received[6] + comm_received[7] + comm_received[8];
  
  Serial.write(comm_sent, COMM_SIZE_P);
}
