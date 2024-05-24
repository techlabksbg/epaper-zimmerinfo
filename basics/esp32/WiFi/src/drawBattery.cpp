#include "drawBattery.h"

int percentage(float voltage) {
    float limits[9][2] = {{4.00, 100.0},
    {3.95 ,90.00},
    {3.9,80.00},
    {3.85,50.00},
    {3.8,40.00},
    {3.72,30.00},
    {3.68,20.00},
    {3.6,10.00},
    {3.0, 0.00}};
    if (voltage>=4.0) return 100;
    for (int i=1; i<9; i++) {
        if (voltage > limits[i][0]) {
            float lambda = (voltage-limits[i][0])/(limits[i-1][0]-limits[i][0]);
            int percent = limits[i][1]+lambda*(limits[i-1][1]-limits[i][1]);
            return percent;
        }
    }
    return 0;
}

void drawBattery(float voltage, int x, int y, UBYTE *black, UBYTE *red) {
    int w=27;
    char buf[20];
    int p = percentage(voltage);
    if (p>30) {
        Paint_SelectImage(black);
    } else {
        Paint_SelectImage(red);
    }
    Paint_DrawRectangle(x,y,x+w,y+10,BLACK, DOT_PIXEL_1X1, DRAW_FILL_EMPTY);
    Paint_DrawRectangle(x-2,y+4,x-1,y+6,BLACK, DOT_PIXEL_1X1, DRAW_FILL_EMPTY);
    Paint_DrawRectangle(x+w-w*p/100,y,x+w,y+10,BLACK, DOT_PIXEL_1X1, DRAW_FILL_FULL);
    sprintf(buf, "%.2fV", voltage);
    Paint_DrawString_EN(x, y+12, buf, &Font8, WHITE, BLACK);

}