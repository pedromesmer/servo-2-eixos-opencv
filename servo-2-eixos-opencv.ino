#include <Servo.h>

int erroX = 0;
int erroY = 0;

Servo servoX, servoY;

float anguloX = 90;
float anguloY = 45;

float ganho = 0.02;

void setup() {
  Serial.begin(115200);

  servoX.attach(9);
  servoY.attach(10);

  servoX.write(anguloX);
  servoY.write(anguloY);
}

void loop() {

  if (Serial.available()) {
    String data = Serial.readStringUntil('\n');
    int commaIndex = data.indexOf(',');

    if (commaIndex > 0) {

      erroX = data.substring(0, commaIndex).toInt();
      erroY = data.substring(commaIndex + 1).toInt();

      int deadzone = 15;

      if (abs(erroX) < deadzone) {
        erroX = 0;
      }

      if (abs(erroY) < deadzone) {
        erroY = 0;
      }

      // movimento proporcional ao erro
      anguloX -= erroX * ganho;
      anguloY += erroY * ganho;

      // limites físicos
      anguloX = constrain(anguloX, 0, 180);
      anguloY = constrain(anguloY, 0, 90);

      servoX.write(anguloX);
      servoY.write(anguloY);
    }
  }
}
