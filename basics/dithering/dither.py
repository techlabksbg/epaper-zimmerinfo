import cv2
import sys
import os
import numpy as np
import math

file = "board.png"
if len(sys.argv)>1:
    file = sys.argv[1]
if not os.path.exists(file):
    raise f"Datei {file} nicht gefunden!"

def readAndConvert(file):
    return cv2.cvtColor(cv2.imread(file), cv2.COLOR_BGR2GRAY)/255  # Conversion to float in 0..1

def readAndConvertRGB(file):
    return cv2.imread(file)/255  # Conversion to float in 0..1

def toBWSimple(img):
    c = np.copy(img)
    h,w = c.shape
    for y in range(h):
        for x in range(w):
            if img[y,x]<0.5:
                c[y,x] = 0
            else:
                c[y,x] = 1.0
    return c


def floydSteinberg(img):
    positions = [[1,0],[-1,1],[0,1],[1,1]]
    weights = [7/16, 3/16, 5/16, 1/16]
    c = np.copy(img)
    h,w = c.shape
    for y in range(h):
        for x in range(w):
            e = c[y,x]
            if c[y,x]<0.5:
                c[y,x] = 0
            else:
                c[y,x] = 1.0
                e = e-1.0
            # Diffuse error
            for i in range(len(positions)):
                a = x+positions[i][0]
                b = y+positions[i][1]
                if (a>=0 and a<w and b<h):
                    c[b,a]+=e*weights[i]
    return c


def ditherWithRed(img):
    positions = [[1,0],[-1,1],[0,1],[1,1]]
    weights = [7/16, 3/16, 5/16, 1/16]
    colors = np.array([[0,0,0], [0,0,1], [1,1,1]])
    c = np.copy(img)
    h,w,_ = c.shape
    for y in range(h):
        for x in range(w):
            d = [np.linalg.norm(c[y,x]-cc) for cc in colors]
            i = d.index(min(d))
            c[y,x] = colors[i]
            e = img[y,x]-c[y,x]
            for i in range(len(positions)):
                a = x+positions[i][0]
                b = y+positions[i][1]
                if (a>=0 and a<w and b<h):
                    c[b,a]+=e*weights[i]
    return c

# Assume Bits in Bytes to be in big-endian
def toBinary(tox,toy,img):
    imh, imw = img.shape
    w = 800
    h = 480
    perRow = math.ceil(w/8)
    n = perRow*h
    data = np.zeros((n,),dtype=np.uint8)

    for y in range(h):
        for b in range(0,perRow):
            v = 0
            for x in range(b*8,min(b*8+8,w)):  # This probably leads to wrong results if w % 8 != 0
                tx = x-tox
                ty = y-toy
                # On image?
                if (tx>=0 and ty>=0 and tx<imw and ty<imh):
                    v = v*2 + int(img[y,x])
                else:
                    v = v*2 + 1  # Default white
            data[b+y*perRow]=v
    return data

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

def binaryToC(data, varname="myimage"):
    res = f"const unsigned char {varname}[{data.shape[0]}] = " + "{\n  "
    for i in range(data.shape[0]):
        res += f"{data[i]},"
        if i%16==15:
            res += "\n  "
    res += "};\n"
    return res
                                                     

img = readAndConvertRGB(file)
print(img.shape)
cv2.imshow('Image', img)
cv2.waitKey(100)
c = ditherWithRed(img)
cv2.imshow('Image', c)
cv2.waitKey(1000)
b,r = toBinaryRB(0,0,c)
with open("data.bin", "wb") as f:
    f.write(b)
    f.write(r)
#data  = toBinary(0,0,c)
#with open("data.c", "w") as f:
#    f.write(binaryToC(b,"myblack"))
#    f.write(binaryToC(r,"myred"))


