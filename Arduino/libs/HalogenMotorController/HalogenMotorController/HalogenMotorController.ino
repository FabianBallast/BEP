/*  Arduino DC Motor Control - PWM | H-Bridge | L298N  -  Example 01

    by Dejan Nedelkovski, www.HowToMechatronics.com
*/

#define enA 3
#define in1 6
#define in2 7


void setup() {
  pinMode(enA, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  // Set initial rotation direction
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
}

void loop() {
  analogWrite(enA, 255); // Send PWM signal to L298N Enable pin
  delay(1000);
  analogWrite(enA, 50); // Send PWM signal to L298N Enable pin
  delay(1000);
}
