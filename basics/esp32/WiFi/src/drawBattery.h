#pragma once

#include "DEV_Config.h"
#include "EPD.h"
#include "GUI_Paint.h"

int percentage(float voltage);
void drawBattery(float voltage, int x, int y, UBYTE *black, UBYTE *red);