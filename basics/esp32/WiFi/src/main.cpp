#include <Arduino.h>
#include <WiFi.h>
#include "secrets.h"
// Also see https://randomnerdtutorials.com/esp32-adc-analog-read-arduino-ide/
#define BATPIN 34

void initWiFi() {
  WiFi.mode(WIFI_STA);
  WiFi.begin(SSID, PASSWD);
  Serial.print("Connecting to WiFi ..");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print('.');
    delay(1000);
  }
  Serial.println(WiFi.localIP());
}


void setup(){
  Serial.begin(115200);
  initWiFi();
}

void loop(){}