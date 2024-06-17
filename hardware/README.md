# Hardware
  * ESP32-Mikrokontroller mit WaveShare DriverHat: https://www.aliexpress.com/item/1005001881216085.html
  * Displays: https://www.aliexpress.com/item/1005005121813674.html
  * TPS63020 Boost Converter: https://www.aliexpress.com/item/1005006167904909.html
  * DS3231: (And https://microcontrollerslab.com/esp32-ds3231-real-time-clock-rtc-oled/)


## Masse
Display: 
  * Aussen: 111mm x 170mm
  * Rand link, oben, rechts: 4mm, unten 10mm
  * Ribbon unten: 73mm, 22mm 75mm, kann auf 1mm umgebogen werden. Ribbon-Länge 24mm, Kontakt 4mm



# Schemas
## WaveShare ESP32 Driver Board
  * Wiki: https://www.waveshare.com/wiki/E-Paper_ESP32_Driver_Board
  * Allgemein ESP32 Pinout: https://randomnerdtutorials.com/esp32-pinout-reference-gpios/
### Gebrauchte Pins:
  * Driver Board: 13, 14, 15, 25, 26, 27
  * Batterie-Sensor: 34, Power-Switch 32
  * RTC DS3231: I2C-Default Pins: 21 (SDA), 22 (SCL)
### Noch freie Pins:
  * Problemlos: 4, 16 (UART 2 RX), 17 (UART 2 TX), 18, 19 (nicht angeschrieben, zwischen 18 und GND), ~21~, ~22~, 23, ~32~, 33, (Input only: ~34~, 35)
  * With care: 2 (LED, must be floating or low at boot), 12 (boot fails if HIGH)
## TPS63020
![TPS63020 Boost Converter](boost-buck-converter.jpg)

## DS3231
  * Library: https://registry.platformio.org/libraries/erriez/ErriezDS3231
  * SDA: 21, SCL: 22
