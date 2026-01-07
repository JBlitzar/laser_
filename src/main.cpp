#include <Arduino.h>
#include <Servo.h>

Servo servo1;
Servo servo2;

void setup() {
  Serial.begin(115200);
  servo1.attach(13); // D13
  servo2.attach(14); // D14
  Serial.println("Two servos ready!");
}

void loop() {
  // Move both servos to 0°
  servo1.write(0);
  servo2.write(0);
  delay(1000);

  // Move both to 90°
  servo1.write(90);
  servo2.write(90);
  delay(1000);

  // Move both to 180°
  servo1.write(180);
  servo2.write(180);
  delay(1000);
}
