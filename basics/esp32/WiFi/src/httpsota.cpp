// from https://github.com/espressif/arduino-esp32/blob/master/libraries/Update/examples/HTTPS_OTA_Update/HTTPS_OTA_Update.ino
#include <arch/cc.h>
#include <IPAddress.h>

#include "HttpsOTAUpdate.h"
#include "WiFi.h"

#include "ISRG_Root_X1.h"

static HttpsOTAStatus_t otastatus;

void HttpEvent(HttpEvent_t *event)
{
    switch(event->event_id) {
        case HTTP_EVENT_ERROR:
            Serial.println("Http Event Error");
            break;
        case HTTP_EVENT_ON_CONNECTED:
            Serial.println("Http Event On Connected");
            break;
        case HTTP_EVENT_HEADER_SENT:
            Serial.println("Http Event Header Sent");
            break;
        case HTTP_EVENT_ON_HEADER:
            Serial.printf("Http Event On Header, key=%s, value=%s\n", event->header_key, event->header_value);
            break;
        case HTTP_EVENT_ON_DATA:
            break;
        case HTTP_EVENT_ON_FINISH:
            Serial.println("Http Event On Finish");
            break;
        case HTTP_EVENT_DISCONNECTED:
            Serial.println("Http Event Disconnected");
            break;
        /*case HTTP_EVENT_REDIRECT:
            Serial.println("Http Event Redirect");
            break; */
    }
}


bool httpsOTA(String url){

    HttpsOTA.onHttpEvent(HttpEvent);
    Serial.println("Starting OTA");
    HttpsOTA.begin(url.c_str(), isrg_root_x1); 

    Serial.println("Please Wait it takes some time ...");
    while(1) {
        otastatus = HttpsOTA.status();
        if(otastatus == HTTPS_OTA_SUCCESS) { 
            Serial.println("Firmware written successfully. To reboot device, call API ESP.restart() or PUSH restart button on device");
            delay(1000);
            ESP.restart();
        } else if(otastatus == HTTPS_OTA_FAIL) { 
            Serial.println("Firmware Upgrade Fail");
            return false;
        }
        for (int i=0; i<1000; i++) {
            int k = abs(500-i);
            digitalWrite(BUILTIN_LED, HIGH);
            delayMicroseconds(500-k);
            digitalWrite(BUILTIN_LED, LOW);
            delayMicroseconds(k);
        }
    }
    return false;
}
