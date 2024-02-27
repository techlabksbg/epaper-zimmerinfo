import cv2
import sys
import os
import numpy as np

file = "data.bin"
if len(sys.argv)>1:
    file = sys.argv[1]
if not os.path.exists(file):
    raise f"Datei {file} nicht gefunden!"

def readData(file):
    with open(file, "rb") as f:
        bindata = f.read()
    img = np.zeros((480,800,3), dtype=np.uint8)
    for y in range(480):
        for x in range(800):
            bit = 7-x%8
            byte = x//8+y*100
            bw = (bindata[byte] >> bit) & 1
            rw = (bindata[byte+48000] >> bit) & 1
            if (bw==1 and rw==1):
                img[y][x][0] = 255
                img[y][x][1] = 255
                img[y][x][2] = 255
            elif rw==0:
                img[y][x][2] = 255 
    return img



img = readData(file)
cv2.imshow("result", img)
cv2.waitKey(5000)