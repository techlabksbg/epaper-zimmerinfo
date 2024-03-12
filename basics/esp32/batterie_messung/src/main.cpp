#include <Arduino.h>

// Also see https://randomnerdtutorials.com/esp32-adc-analog-read-arduino-ide/
#define BATPIN 34

void setup() {
  Serial.begin(115200);
  
}

void loop() {
  int bat = 0;
  for (int i=0; i<100; i++) {
    bat += analogRead(BATPIN);
    delay(10);
  }
  // 227056 sollte 4.055 V sein
  // 188410 sollte 3.405 V sein
  float vbat = (float)(bat-188410)/(227056-188410)*(4.055-3.405)+3.405;
  Serial.printf("%d -> %.2f V\n", bat, vbat);
  delay(1000);
  
}