#include <Servo.h>

/*
Instável, a camera deve ficar no servo e o servo sempre tentar centralizar o alvo.
atualmente, a camera está fixa e o servo reflete o movimento do alvo.
*/

int xRead = 0;
int yRead = 0;

Servo servoX, servoY;

void setup() {
  Serial.begin(115200);

  servoX.attach(9);
  servoY.attach(10);

  servoX.write(90);
  servoY.write(45);
}

void loop() {
  if (Serial.available()) {
    String data = Serial.readStringUntil('\n');

    int commaIndex = data.indexOf(',');

    if (commaIndex > 0) {
      xRead = data.substring(0, commaIndex).toInt();
      yRead = data.substring(commaIndex + 1).toInt();

      float x = (xRead * 180.0) / 1000.0; // 0 a 180
      float y = (yRead *  90.0) / 1000.0; // 0 a 90

      servoX.write(180 - x);
      servoY.write(y);

      // debug
      Serial.print("X: ");
      Serial.print(x);
      Serial.print(" | Y: ");
      Serial.println(y);
    }
  }
}
