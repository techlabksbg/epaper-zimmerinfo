#include <Arduino.h>
#include <WiFi.h>
/*
The following file contains something like
#define SSID "Lord of the Pings"
#define PASSWD "MyPrecious"
#define SERVERURL "https://example.com"
*/
#include "secrets.h"
#include "DEV_Config.h"
#include "EPD.h"
#include "GUI_Paint.h"
#include <stdlib.h>
#include <string>

#include "soc/soc.h"
#include "soc/rtc_cntl_reg.h"

#include "httpsRequest.h"
#include "httpsota.h"
#include "firmware-version.h"
#include "drawBattery.h"

#define POWER_PIN 32
#define BATPIN 34



RTC_DATA_ATTR int nocon;
RTC_DATA_ATTR char bildhash[20];
// Also see https://randomnerdtutorials.com/esp32-adc-analog-read-arduino-ide/

void goToSleep(long long time);
void errorScreen(String fehler, UBYTE *BlackImage, int ScreenSize);

void flash(int times, int on, int off) {
  for (int i=0; i<times; i++) {
    digitalWrite(BUILTIN_LED, HIGH);
    delay(on);
    digitalWrite(BUILTIN_LED, LOW);
    delay(off);
  }
}

void fadeout() {
  for (int i=0; i<1000; i++) {
    digitalWrite(BUILTIN_LED, HIGH);
    delayMicroseconds(1000-i);
    digitalWrite(BUILTIN_LED, LOW);
    delayMicroseconds(i);
  }
}

void initWiFi() {
  Serial.println(SSID);
  WiFi.mode(WIFI_STA);
  WiFi.begin(SSID, PASSWD);
  Serial.print("Connecting to WiFi ..");
  int seconds = 20;
  while (WiFi.status() !=WL_CONNECTED && seconds>0) {
    Serial.print(".");
    delay(1000);
    flash(1, 10, 0);
    seconds--;
  }
}

double voltage=0.0;
int adValue = 0;
//from basics/esp32/batterie_messung
float batterie_messung() {
  adValue = 0;
  for (int i=0; i<100; i++) {
    adValue += analogRead(BATPIN);
    delay(10);
  }
  // 227056 sollte 4.055 V sein
  // 188410 sollte 3.405 V sein
  voltage = (float)(adValue-188410)/(227056-188410)*(4.055-3.405)+3.405;
  return voltage;
}

void antwort(String response, UBYTE *BlackImage, int ImageSize){
  int pos = 0;
  Serial.println(response);
  while (pos<response.length()) {
    int zeilenende = response.indexOf('\n', pos);
    if (zeilenende<0) {
      zeilenende = response.length();
    }
    int keyende = response.indexOf(' ', pos);
    if (keyende<0) {
      errorScreen(String("Missing space in line"), BlackImage, ImageSize);
    }
    String key = response.substring(pos, keyende);
    String value = response.substring(keyende+1, zeilenende);
    Serial.println(value);
    Serial.printf("key = %s, value=%s pos=%d, keyende=%d, zeilenende=%d\n", key.c_str(), value.c_str(), pos, keyende, zeilenende);
    pos = zeilenende+1;
    if (key == "sleep"){
      nocon=0;
      goToSleep(value.toInt());
    }
    if (key == "bild"){
      if (!value.startsWith("https://")) {
        value = String(SERVERURL)+value;
      }
      int len = request(value,(char*)BlackImage, ImageSize*2);
      if (len!=ImageSize*2) {
        errorScreen(String("https-Request has only size ")+String(len), BlackImage, ImageSize);
      } else {
        WiFi.disconnect(true);
        WiFi.mode(WIFI_OFF);
        //hier kann WiFI abgeschaltet werden
        Serial.println("Displaying graphics");
        DEV_Module_Init();
        EPD_7IN5B_V2_Init();
        drawBattery(voltage, 740,3, BlackImage, BlackImage+ImageSize);
        //EPD_7IN5B_V2_Clear();
        EPD_7IN5B_V2_Display(BlackImage, BlackImage+ImageSize);
        EPD_7IN5B_V2_Sleep();
      }
    }
    if (key=="hash"){
      if (value.length()<20) {
        strncpy(bildhash, value.c_str(), 19);
        Serial.print("Set bildhash to ");
        Serial.println(value);
      }
    }
    if (key == "update") {
      httpsOTA(value);
      errorScreen(String("OTA via https failed "), BlackImage, ImageSize);
    }
  }
}

void goToSleep(long long time){
  Serial.printf("Going deepsleep for %d seconds", time);
  fadeout();
  digitalWrite(POWER_PIN, LOW);
  delay(500);
  esp_sleep_enable_timer_wakeup(time*1000000ULL);
  esp_deep_sleep_start();
}

void errorScreen(String fehler, UBYTE *BlackImage, int ImageSize) {
  nocon = nocon+1;
  String MAC = "MAC: " + String(WiFi.macAddress());
  String battery = "Batteriespannung: " + String(voltage) + "V adValue=" + String(adValue);
  // Set images to white here!
  printf("NewImage:BlackImage and RYImage\r\n");
  Paint_NewImage(BlackImage, EPD_7IN5B_V2_WIDTH, EPD_7IN5B_V2_HEIGHT , 0, WHITE);
  Paint_NewImage(BlackImage+ImageSize, EPD_7IN5B_V2_WIDTH, EPD_7IN5B_V2_HEIGHT , 0, WHITE);
  Paint_SelectImage(BlackImage+ImageSize);
  Paint_Clear(WHITE);
  Paint_SelectImage(BlackImage);
  Paint_Clear(WHITE);
  
  Paint_DrawString_EN(100,100, fehler.c_str(), &Font16, WHITE, BLACK);
  Paint_DrawString_EN(100,150, "SSID " SSID, &Font16, WHITE, BLACK);
  Paint_DrawString_EN(100,180, MAC.c_str(), &Font16, WHITE, BLACK);
  Paint_DrawString_EN(100,210, battery.c_str(), &Font16, WHITE, BLACK);

  drawBattery(voltage, 740,10, BlackImage, BlackImage+ImageSize);

  WiFi.disconnect(true);
  WiFi.mode(WIFI_OFF);
  printf("EPD_Display\r\n");
  DEV_Module_Init();
  EPD_7IN5B_V2_Init();
  //EPD_7IN5B_V2_Clear();
  EPD_7IN5B_V2_Display(BlackImage, BlackImage+ImageSize);
  EPD_7IN5B_V2_Sleep();
  delay(1000);
  goToSleep(60*(1<<nocon));
}

void setup(){
  // Disable Brownout Detection 
  WRITE_PERI_REG(RTC_CNTL_BROWN_OUT_REG, 0);
  pinMode(POWER_PIN, OUTPUT);
  digitalWrite(POWER_PIN, HIGH);  // Switch power on

  Serial.begin(115200);
  Serial.println("MAC-Address:");
  Serial.println(WiFi.macAddress());
  batterie_messung();
  //voltage = 3.7;
  Serial.printf("Batterie-Spannung: %.2fV -> %d%% (from adValue=%d)\n",voltage,percentage(voltage), adValue);
  pinMode(BUILTIN_LED, OUTPUT);
  flash(2, 20, 300);
  if (esp_sleep_get_wakeup_cause()!=ESP_SLEEP_WAKEUP_TIMER){
    bildhash[0]=0;
    nocon=0;
  }

  printf("e-Paper Init and Clear...\r\n");
  //EPD_7IN5B_V2_Clear();
  DEV_Delay_ms(500);
  UBYTE *BlackImage, *RYImage;
  UWORD Imagesize = ((EPD_7IN5B_V2_WIDTH % 8 == 0) ? (EPD_7IN5B_V2_WIDTH / 8 ) : (EPD_7IN5B_V2_WIDTH / 8 + 1)) * EPD_7IN5B_V2_HEIGHT;
  if ((BlackImage = (UBYTE *)malloc(Imagesize*2)) == NULL) {
    printf("Failed to apply for black memory...\r\n");
    while(1);
    //LED blinken lassen
  }
  RYImage=BlackImage+Imagesize;
  Paint_NewImage(BlackImage, EPD_7IN5B_V2_WIDTH, EPD_7IN5B_V2_HEIGHT , 0, WHITE);
  Paint_SelectImage(BlackImage);
  Paint_Clear(WHITE);
  Paint_NewImage(RYImage, EPD_7IN5B_V2_WIDTH, EPD_7IN5B_V2_HEIGHT , 0, WHITE);
  Paint_SelectImage(RYImage);
  Paint_Clear(WHITE);


  

  Serial.println("WiFi-Init...");
  initWiFi();
  if (WiFi.status() !=WL_CONNECTED) {
    Serial.println("Keine WiFi-Verbindung...");
    errorScreen("Keine WiFi-Verbindung", BlackImage, Imagesize);

  }
  else{
    String mac = WiFi.macAddress();
    Serial.println("MAC-Address");
    Serial.println(mac);
    flash(5, 10, 100);
    int len = request(String(SERVERURL)+"anzeige?mac="+mac+"&volt="+String(voltage)+"&hash="+bildhash+"&firmware="+FIRMWARE+"&nocon="+String(nocon), (char *)BlackImage, Imagesize*2);
    BlackImage[len]=0;
    String response = String((char*)BlackImage);
    flash(5,10,100);
    antwort(response, BlackImage, Imagesize);
  }
}

void loop(){}