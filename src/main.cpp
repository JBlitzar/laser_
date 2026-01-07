#include <Arduino.h>
#include <Servo.h>

Servo servo1;
Servo servo2;

void setup() {
  Serial.begin(115200);
  servo1.attach(13); // Servo 1 signal pin
  servo2.attach(14); // Servo 2 signal pin
  Serial.println("ESP32 Servo Controller Ready!");
}

void loop() {
  // Check if serial data is available
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n'); // Read until newline
    command.trim(); // Remove whitespace

    // Expect command format: "S1:90" or "S2:45"
    if (command.startsWith("S1:")) {
      int pos = command.substring(3).toInt();
      pos = constrain(pos, 0, 180);
      servo1.write(pos);
      Serial.print("Servo 1 moved to ");
      Serial.println(pos);
    } else if (command.startsWith("S2:")) {
      int pos = command.substring(3).toInt();
      pos = constrain(pos, 0, 180);
      servo2.write(pos);
      Serial.print("Servo 2 moved to ");
      Serial.println(pos);
    }
  }
}
