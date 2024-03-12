import sqlite3
from PIL import Image, ImageDraw
import cv2
import numpy as np
import math
import os

########## EINIGES KOPIERT von ../dithering/dither.py ######################

def readAndConvertRGB(file):
    return cv2.imread(file)/255  # Conversion to float in 0..1

def filter(img):
    c = np.copy(img)
    h,w,_ = c.shape
    for y in range(h):
        for x in range(w):
            c[y,x] = [0, 0, 0] if np.sum(c[y,x]) < 1.5 else [1, 1, 1] 
    return c

def toBinaryRB(tox,toy,img):
    imh, imw, _ = img.shape
    w = 800
    h = 480
    perRow = math.ceil(w/8)
    n = perRow*h
    black = np.zeros((n,),dtype=np.uint8)
    red = np.zeros((n,),dtype=np.uint8)

    for y in range(h):
        for b in range(0,perRow):
            bk = 0
            rd = 0
            for x in range(b*8,min(b*8+8,w)):  # This probably leads to wrong results if w % 8 != 0
                tx = x-tox
                ty = y-toy
                # On image?
                if (tx>=0 and ty>=0 and tx<imw and ty<imh):
                    rd*=2
                    bk*=2
                    if (img[y,x,2]==1 and img[y,x,1]==0):  # BGR ! Color red
                        bk+=1
                    elif (img[y,x,0]==1 and img[y,x,1]==1): # White
                        bk+=1
                        rd+=1
                    else:   # Black
                        rd+=1
                else:
                    bk=bk*2+1
                    rd=rd*2
            black[b+y*perRow]=bk
            red[b+y*perRow]=rd
    return black, red

def convert_to_bin(path):
    for datei in os.listdir(path):
        datei = path+"/"+datei
        print(datei)
        img = readAndConvertRGB(datei)
        print(img.shape)
        c = filter(img)
        b, r = toBinaryRB(0, 0, c)
        datei = os.path.splitext(datei)[0]
        with open(datei + ".bin", "wb") as f:
            f.write(b)
            f.write(r)

