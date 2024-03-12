import sqlite3
from PIL import Image, ImageDraw
import cv2
import numpy as np
import math

########## EINIGES KOPIERT von ../dithering/dither.py ######################

def readAndConvertRGB(file):
    return cv2.imread(file)/255  # Conversion to float in 0..1


# def ditherWithRed(img):
#     positions = [[1,0],[-1,1],[0,1],[1,1]]
#     weights = [7/16, 3/16, 5/16, 1/16]
#     colors = np.array([[0,0,0], [0,0,1], [1,1,1]])
#     c = np.copy(img)
#     h,w,_ = c.shape
#     for y in range(h):
#         for x in range(w):
#             d = [np.linalg.norm(c[y,x]-cc) for cc in colors]
#             i = d.index(min(d))
#             c[y,x] = colors[i]
#             e = img[y,x]-c[y,x]
#             for i in range(len(positions)):
#                 a = x+positions[i][0]
#                 b = y+positions[i][1]
#                 if (a>=0 and a<w and b<h):
#                     c[b,a]+=e*weights[i]
#     return c

def filter(img):
    # positions = [[1,0],[-1,1],[0,1],[1,1]]
    # weights = [7/16, 3/16, 5/16, 1/16]
    # colors = np.array([[0,0,0], [0,0,1], [1,1,1]])
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

for datei in ['diagram', 'matplotdiagram-800x480']:
    img = readAndConvertRGB(datei + '.png')
    print(img.shape)
    # cv2.imshow('Image', img)
    # cv2.waitKey(100)
    # c = ditherWithRed(img)
    c = filter(img)
    # cv2.imshow('Image', c)
    # cv2.waitKey(1000)
    b, r = toBinaryRB(0, 0, c)
    with open(datei + ".bin", "wb") as f:
        f.write(b)
        f.write(r)

