#include <Arduino.h>
#include <WiFi.h>
#include "DEV_Config.h"
#include "EPD.h"
#include "GUI_Paint.h"
#include <stdlib.h>
#include <WiFiClientSecure.h>

#include "secrets.h"
#include "ISRG_Root_X1.h"

int nocon=0;
// Also see https://randomnerdtutorials.com/esp32-adc-analog-read-arduino-ide/
#define BATPIN 34

void initWiFi() {
  WiFi.mode(WIFI_STA);
  WiFi.begin(SSID, PASSWD);
  Serial.print("Connecting to WiFi ..");
  int seconds = 20;
  while (WiFi.status() !=WL_CONNECTED && seconds>0) {
    Serial.print(".");
    delay(1000);
    seconds--;
  }
  Serial.println(WiFi.localIP());
}

// From https://randomnerdtutorials.com/esp32-https-requests/
void getImage(UBYTE *bw, UBYTE *rw) {
    WiFiClientSecure client;
    const char*  server = "ofi.tech-lab.ch";  // Server hostname
    client.setCACert(test_root_ca);
    Serial.println("\nStarting connection to server...");
  if (!client.connect(server, 443)) {
    Serial.println("Connection failed!");
  } else {
    Serial.println("Connected to server!");
    // Make a HTTP request:
    client.println("GET https://ofi.tech-lab.ch/ef05a/data.bin HTTP/1.0");
    client.println("Host: ofi.tech-lab.ch");
    client.println("Connection: close");
    client.println();

    while (client.connected()) {
      String line = client.readStringUntil('\n');
      Serial.println(line);
      if (line == "\r") {
        Serial.println("headers received");
        break;
      }
    }
    // if there are incoming bytes available
    // from the server, read them and print them:
    UBYTE *ptr = bw;
    Serial.printf("available: %d\n", client.available());
    for (UBYTE *ptr = bw; ptr<bw+48000; ptr++) {
      while (client.available()==0) delay(1);
      *ptr = client.read();
    }
    Serial.println("Read 48000 Bytes into bw");
    for (UBYTE *ptr = rw; ptr<rw+48000; ptr++) {
      while (client.available()==0) delay(1);
      *ptr = client.read();
    }
    Serial.println("Read 48000 Bytes into rw");
    for (UBYTE *ptr = rw; ptr<rw+48000; ptr++)
    client.stop();
  }
}


void setup(){
  DEV_Module_Init();
  EPD_7IN5B_V2_Init();

  Serial.begin(115200);
  UBYTE *BlackImage, *RYImage;
  UWORD Imagesize = ((EPD_7IN5B_V2_WIDTH % 8 == 0) ? (EPD_7IN5B_V2_WIDTH / 8 ) : (EPD_7IN5B_V2_WIDTH / 8 + 1)) * EPD_7IN5B_V2_HEIGHT;
  if ((BlackImage = (UBYTE *)malloc(Imagesize)) == NULL) {
    printf("Failed to apply for black memory...\r\n");
    while(1);
  }
  if ((RYImage = (UBYTE *)malloc(Imagesize)) == NULL) {
    printf("Failed to apply for red memory...\r\n");
    while(1);
  }
  printf("NewImage:BlackImage and RYImage\r\n");
  Paint_NewImage(BlackImage, EPD_7IN5B_V2_WIDTH, EPD_7IN5B_V2_HEIGHT , 0, WHITE);
  Paint_NewImage(RYImage, EPD_7IN5B_V2_WIDTH, EPD_7IN5B_V2_HEIGHT , 0, WHITE);

  initWiFi();
  if (WiFi.status() !=WL_CONNECTED) {
    Serial.println("Not connected!");
    nocon = nocon+1;
    Paint_SelectImage(BlackImage);
    Paint_DrawString_EN(10, 20, SSID, &Font16, WHITE, BLACK);
    Paint_DrawString_EN(10, 40, WiFi.macAddress().c_str(), &Font16, WHITE, BLACK);
  }
  getImage(BlackImage, RYImage);
  Serial.println("Displaying graphics");
  EPD_7IN5B_V2_Display(BlackImage, RYImage);
  DEV_Delay_ms(2000);
}

void loop(){}