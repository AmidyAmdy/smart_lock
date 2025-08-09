#include <Servo.h>

#define SERVO_PIN 6

Servo servo;
bool doorOpen = false;

void setup() {
  Serial.begin(9600);
  servo.attach(SERVO_PIN);
  servo.write(0);
  Serial.println("Готово.");
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();

    if (command == "open") {
      servo.write(90);
      Serial.println("Открыто");
      doorOpen = true;
    } else if (command == "close") {
      servo.write(0);
      Serial.println("Закрыто");
      doorOpen = false;
    } else {
      Serial.println("Неизвестная команда");
    }
  }
}
