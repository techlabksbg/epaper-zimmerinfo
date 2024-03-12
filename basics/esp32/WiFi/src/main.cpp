#include <Arduino.h>
#include <WiFi.h>
#include "secrets.h"
#include "DEV_Config.h"
#include "EPD.h"
#include "GUI_Paint.h"
#include <stdlib.h>
#include <string>
int nocon=0;
// Also see https://randomnerdtutorials.com/esp32-adc-analog-read-arduino-ide/

#define BATPIN 34

void initWiFi() {
  WiFi.mode(WIFI_STA);
  WiFi.begin(SSID, PASSWD);
  Serial.print("Connecting to WiFi ..");
  Serial.println(WiFi.localIP());
}

//from basics/esp32/batterie_messung
String batterie_messung() {
  int bat = 0;
  for (int i=0; i<100; i++) {
    bat += analogRead(BATPIN);
    delay(10);
  }
  // 227056 sollte 4.055 V sein
  // 188410 sollte 3.405 V sein
  float vbat = (float)(bat-188410)/(227056-188410)*(4.055-3.405)+3.405;
  return String(vbat);
}

void setup(){
  printf("EPD_7IN5B_V2_test Demo\r\n");
  DEV_Module_Init();

  printf("e-Paper Init and Clear...\r\n");
  EPD_7IN5B_V2_Init();
  EPD_7IN5B_V2_Clear();
  DEV_Delay_ms(500);
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
  delay(10000);
  if (WiFi.status() !=WL_CONNECTED) {
    nocon = nocon+1;
    Paint_SelectImage(BlackImage);
    Paint_DrawString_EN(100,150, "keine Verbindung zu "SSID, &Font16, WHITE, BLACK);
    Paint_DrawString_EN(100,180, WiFi.macAddress().c_str(), &Font16, WHITE, BLACK);
    Paint_DrawString_EN(100,210, batterie_messung().c_str(), &Font16, WHITE, BLACK);
    printf("EPD_Display\r\n");
    EPD_7IN5B_V2_Display(BlackImage, RYImage);
  }
  else {
    nocon = 0;
    Paint_SelectImage(BlackImage);
    


    Paint_SelectImage(RYImage);
    


  }
}

void loop(){}