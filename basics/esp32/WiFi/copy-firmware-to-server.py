import datetime
import os

now = datetime.datetime.now();
firmware = now.strftime("%Y%m%d-%H%M%S")
print(firmware)
include = f"#define FIRMWARE \"{firmware}\""
print(include)

with open("src/firmware-version.h", "w") as f:
    f.write(include)
cmd = "~/.platformio/penv/bin/pio run"
print(cmd)
os.system(cmd)
binfile = ".pio/build/esp32doit-devkit-v1/firmware.bin"
if os.path.exists(binfile):
    cmd = f"scp {binfile} ef:epaper/epaper-zimmerinfo/basics/server/flaskr/static/firmware/{firmware}.bin"
    print(cmd)
    os.system(cmd)
else:
    print("Sorry, binary file does not exist, ")
