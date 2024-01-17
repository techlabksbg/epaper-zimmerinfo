#include <Arduino.h>

// From the file epd7in5b_V2-demo.ino


#include "DEV_Config.h"
#include "EPD.h"



UBYTE *blackImage, *redImage;
UWORD Imagesize = ((EPD_7IN5B_V2_WIDTH % 8 == 0) ? (EPD_7IN5B_V2_WIDTH / 8 ) : (EPD_7IN5B_V2_WIDTH / 8 + 1)) * EPD_7IN5B_V2_HEIGHT;

/* Entry point ----------------------------------------------------------------*/
void setup()
{
  Serial.begin(115200);
  delay(100);
  Serial.println("EPD_7IN5B_V2 Serial transmission demo");
  DEV_Module_Init();
  EPD_7IN5B_V2_Init();
  Serial.println("e-Paper Init done.");
/*  EPD_7IN5B_V2_Clear();
  DEV_Delay_ms(500); */

  //Create a new image cache named IMAGE_BW and fill it with white
  if ((blackImage = (UBYTE *)malloc(Imagesize)) == NULL) {
    Serial.println("Failed to apply for black memory... Stop.");
    while(1);
  }
  if ((redImage = (UBYTE *)malloc(Imagesize)) == NULL) {
    Serial.println("Failed to apply for red memory... Stop.");
    while(1);
  }

}

/* The main loop -------------------------------------------------------------*/
UBYTE *curImage = nullptr;
int curByte = 0;
unsigned long nextTime = 0;
void loop() {
  if (curImage==nullptr) {
    curImage = blackImage;
  }
  if (nextTime<millis()) {
    nextTime = millis()+1000;
    Serial.println("Ready");
  }
  while (Serial.available()) {
    //Serial.printf("Write byte %d at %p\n", curByte, curImage);
    curImage[curByte] = Serial.read();
    //Serial.printf("Read %d\n", curImage[curByte]);
    curByte++;
    if (curByte>=Imagesize) {
      curByte = 0;
      if (curImage == blackImage) {
        curImage = redImage;
        Serial.println("Halfway");
      } else {        
        curImage = blackImage;        
        Serial.println("Transmission complete!");
        delay(10);
        EPD_7IN5B_V2_Display(blackImage, redImage);
      }
    }
  }
}
