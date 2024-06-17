#include <rtc.h>
#include <Arduino.h>

bool RTC::init() {
    ds3231 = new ErriezDS3231();
    ok = ds3231->begin();
    if (!ok) {
        Serial.println("Could not initialize RTC connection");
    }
    dt.tm_year = 2024;
    dt.tm_mday = 1;
    dt.tm_mon = 1;
    dt.tm_hour = 0;
    dt.tm_min = 0;
    dt.tm_sec = 0;
    return ok;
}

bool RTC::resetTime() {
    if (ok) {
        if (!ds3231->write(&dt)) {
            Serial.println("Could not set RTC clock");
            return false;
        }
        return true;
    }
    return false;
}

bool RTC::setAlarm(int seconds) {
    int h = seconds/3600;
    int m = (seconds/60)%60;
    seconds = seconds % 60;
    bool res = ds3231->setAlarm1(Alarm1MatchHours, 0, h, m , seconds % 60);
    if (!res) {
        Serial.printf("Setting alarm failed! %d seconds -> h=%d, m=%d, s=%s\n", h,m,seconds);
    }
    res = res && ds3231->alarmInterruptEnable(Alarm1, true);
    if (!res) {
        Serial.println("Setting Interrupt line may have failed");
    }
    return res;
}