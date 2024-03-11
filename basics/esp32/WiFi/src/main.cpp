#include <Arduino.h>
#include <WiFi.h>

#include secrets.h

void setup(){
    WiFi.disconnect();
    WiFi.mode(WIFI_STA);
    WiFi.begin(SSID, PASSWD);
    Serial.print("Connecting to WiFi ..");
}