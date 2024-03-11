# On Linux: sudo apt install python3-serial
# On Windows: pip install pyserial

import serial
import serial.tools.list_ports
import re
import sys
import os
import time

def getPort():
    # From https://stackoverflow.com/questions/12090503/listing-available-com-ports-with-python
    ports = serial.tools.list_ports.comports()
    for port, desc, hwid in sorted(ports):
        print("{}: {} [{}]".format(port, desc, hwid))
    return [port for port, desc, hwid in ports if re.search(r"USB", desc) or re.search(r"USB", hwid)][0]
    

def getData():
    if len(sys.argv)!=2:
        raise "Bitte Dateinnamen mit binären Daten angeben."
    fn = sys.argv[1]
    if not os.path.exists(fn):
        raise f"Datei {fn} existiert nicht."
    if not os.path.getsize(fn)==96000:
        raise f"Die Datei hat nicht die korrekt Grösse von 96000 Bytes"
    with open(fn, mode='rb') as file: # b is important -> binary
        data = file.read()
    return data



data = getData()
port = "/dev/ttyACM0"  # getPort()
print(f"Sending data to port {port}")
with serial.Serial(port, 115200, timeout=0) as ser:
    chunk = 128
    for i in range(0,96000,chunk):
        ser.write(data[i:i+chunk])
        s = ser.read(1000)
        if len(s)>0:
            print(s,end='')
        print(f"\r{i} of {96000}")
        time.sleep(0.001)
    #ser.write(data)
    for i in range(3):
        s = ser.read(1000)
        if len(s)>0:
            print(s,end='')
        time.sleep(0.01)

print(f"Done")
