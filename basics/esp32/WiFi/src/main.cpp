#include <Arduino.h>
#include <WiFi.h>
#include "secrets.h"
#include "DEV_Config.h"
#include "EPD.h"
#include "GUI_Paint.h"
#include <stdlib.h>
#include <string>
#include "httpsRequest.h"

RTC_DATA_ATTR int nocon=0;
// Also see https://randomnerdtutorials.com/esp32-adc-analog-read-arduino-ide/

void goToSleep(long long time);

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

void antwort(String response, UBYTE *BlackImage, int ImageSize){
  int pos = 0;
  Serial.println(response);
  Serial.print("substr -> ");
  Serial.println(response.substring(13,35));
  while (pos<response.length()) {
    int zeilenende = response.indexOf('\n', pos);
    int keyende = response.indexOf(' ', pos);
    String key = response.substring(pos, keyende);
    String value = response.substring(keyende+1, zeilenende);
    Serial.println(value);
    Serial.printf("key = %s, value=%s pos=%d, keyende=%d, zeilenende=%d\n", key.c_str(), value.c_str(), pos, keyende, zeilenende);
    pos = zeilenende+1;
    if (key == "sleep"){
      goToSleep(value.toInt());
    }
    if (key == "bild"){
      if (!value.startsWith("https://")) {
        value = String("https://epaper.tech-lab.ch/")+value;
      }
      int len = httpsRequest(value,(char*)BlackImage, ImageSize*2);
      //hier kann WiFI abgeschaltet werden
      Serial.println("Displaying graphics");
      EPD_7IN5B_V2_Display(BlackImage, BlackImage+ImageSize);
      DEV_Delay_ms(2000);
    }
  }
}

void goToSleep(long long time){
  Serial.printf("Going deepsleep for %d seconds", time);
  esp_sleep_enable_timer_wakeup(time*1000000ULL);
  esp_deep_sleep_start();
}

void setup(){
  Serial.begin(115200);
  printf("EPD_7IN5B_V2_test Demo\r\n");
  DEV_Module_Init();

  printf("e-Paper Init and Clear...\r\n");
  EPD_7IN5B_V2_Init();
  // EPD_7IN5B_V2_Clear();
  DEV_Delay_ms(500);
  UBYTE *BlackImage, *RYImage;
  UWORD Imagesize = ((EPD_7IN5B_V2_WIDTH % 8 == 0) ? (EPD_7IN5B_V2_WIDTH / 8 ) : (EPD_7IN5B_V2_WIDTH / 8 + 1)) * EPD_7IN5B_V2_HEIGHT;
  if ((BlackImage = (UBYTE *)malloc(Imagesize*2)) == NULL) {
    printf("Failed to apply for black memory...\r\n");
    while(1);
  }
  RYImage=BlackImage+Imagesize;
  
  printf("NewImage:BlackImage and RYImage\r\n");
  Paint_NewImage(BlackImage, EPD_7IN5B_V2_WIDTH, EPD_7IN5B_V2_HEIGHT , 0, WHITE);
  Paint_NewImage(RYImage, EPD_7IN5B_V2_WIDTH, EPD_7IN5B_V2_HEIGHT , 0, WHITE);

  initWiFi();
  if (WiFi.status() !=WL_CONNECTED) {


    nocon = nocon+1;
    String MAC = "MAC: " + String(WiFi.macAddress());
    String battery = "Batteriespannung: " + batterie_messung() + "V";
    Paint_SelectImage(BlackImage);
    Paint_SelectImage(RYImage);
    Paint_SelectImage(BlackImage);
    Paint_DrawString_EN(100,150, "keine Verbindung zu " SSID, &Font16, WHITE, BLACK);
    Paint_DrawString_EN(100,180, MAC.c_str(), &Font16, WHITE, BLACK);
    Paint_DrawString_EN(100,210, battery.c_str(), &Font16, WHITE, BLACK);
    printf("EPD_Display\r\n");
    EPD_7IN5B_V2_Display(BlackImage,RYImage);
    goToSleep(1<<nocon);
    }

  else {
    String mac = WiFi.macAddress();
    nocon = 0;
    int len = httpsRequest(String("https://epaper.tech-lab.ch/anzeige?mac=")+mac+"&volt="+batterie_messung(), (char *)BlackImage, Imagesize*2);
    BlackImage[len]=0;
    String response = String((char*)BlackImage);
    antwort(response, BlackImage, Imagesize);
    /*Serial.println("Displaying graphics");
    EPD_7IN5B_V2_Display(BlackImage, RYImage);
    DEV_Delay_ms(2000); */
  }
}

void loop(){}