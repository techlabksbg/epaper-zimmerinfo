#include <Arduino.h>
#include "WiFi.h"
#include "secrets.h"
#define LED 8

void printWifiStatus() {
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());

  IPAddress ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);

  long rssi = WiFi.RSSI();
  Serial.print("signal strength (RSSI):");
  Serial.print(rssi);
  Serial.println(" dBm");
}

void setup() {
    Serial.begin(115200);    
     while (!Serial) { }
    pinMode(LED, OUTPUT);
    Serial.print("Attempting to connect to WiFi on SSID ");
    Serial.println(MY_SSID);
    WiFi.useStaticBuffers(true);
    WiFi.mode(WIFI_STA);
    WiFi.begin(MY_SSID, MY_PASSWORD);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }

    Serial.println("");
    Serial.println("Connected to WiFi");
    printWifiStatus();
}

void loop() {
    Serial.println("Hello world");
    digitalWrite(LED, LOW);
    delay(100);
    digitalWrite(LED, HIGH);
    delay(1000);
}