#include <Arduino.h>
#include <WiFi.h>
#include "DEV_Config.h"
#include "EPD.h"
#include "GUI_Paint.h"
#include <stdlib.h>

#include "secrets.h"
#include "httpsRequest.h"

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


void setup(){
  DEV_Module_Init();
  EPD_7IN5B_V2_Init();

  Serial.begin(115200);
  UBYTE *BlackImage, *RYImage;
  UWORD Imagesize = ((EPD_7IN5B_V2_WIDTH % 8 == 0) ? (EPD_7IN5B_V2_WIDTH / 8 ) : (EPD_7IN5B_V2_WIDTH / 8 + 1)) * EPD_7IN5B_V2_HEIGHT;
  if ((BlackImage = (UBYTE *)malloc(Imagesize*2)) == NULL) {
    printf("Failed to apply for black and red memory...\r\n");
    while(1);
  }
  RYImage = BlackImage + Imagesize;

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
  httpsRequest("ofi.tech-lab.ch", "/ef05a/data.bin", (char *)BlackImage, Imagesize*2);
  Serial.println("Displaying graphics");
  EPD_7IN5B_V2_Display(BlackImage, RYImage);
  DEV_Delay_ms(2000);
}

void loop(){}