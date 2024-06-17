#pragma once
#include <ErriezDS3231.h>

struct RTC {
    ErriezDS3231 *ds3231;
    bool ok = false;
    bool init();
    bool resetTime();
    bool setAlarm(int seconds);
    struct tm dt;
};