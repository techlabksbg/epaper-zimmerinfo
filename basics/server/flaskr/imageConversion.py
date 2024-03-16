from PIL import Image, ImageOps
import numpy as np

def newBWimage():
    """
    Erzeugt ein weisses Schwarz-Weiss Image
    """
    return Image.new("1",(800,480),color=1)


def resizeAndCenter(image):
    """
    Passt ein Bild auf die Grösse des Displays an und
    zentriert es, füllt allfällige Ränder mit Weiss
    """
    return ImageOps.pad(image, (800,480),color="white")
        

def bw_rw2bin(bw, rw):
    """
    returns a Byte Array with with a bw und rw bitmap.
    Suitable to send to the display
    """
    #bw = bw.composite(bw, )
    if (bw.size!=(800,480)):
        bw = resizeAndCenter(bw)
    if (rw.size!=(800,480)):
        rw = resizeAndCenter(rw)
    if (bw.format!="1"):
        bw = bw.convert("1")
    if (rw.format!="1"):
        rw = rw.convert("1")
    return bytes(bw.tobytes())+bytes(rw.tobytes())

def dither_to_bin_and_rgb(image):
    if (image.size!=(800,480)):
        image = resizeAndCenter(image)
    if (image.format!="RGB"):
        image = image.convert("RGB")

    positions = [[1,0],[-1,1],[0,1],[1,1]]
    weights = [7/16, 3/16, 5/16, 1/16]
    colors = np.array([[0,0,0], [1,0,0], [1,1,1]])
   
    data = np.array(image)/255
    res = np.copy(data)
    bw = newBWimage()
    bwpixels = bw.load()
    rw = newBWimage()
    rwpixels = rw.load()
    for y in range(480):
        for x in range(800):
            d = [np.linalg.norm(res[y,x]-cc) for cc in colors]
            i = d.index(min(d))
            if (i==0):
                bwpixels[x,y]=0
            if (i==1):
                rwpixels[x,y]=0
            res[y,x] = colors[i]
            e = data[y,x]-res[y,x]
            for i in range(len(positions)):
                a = x+positions[i][0]
                b = y+positions[i][1]
                if (a>=0 and a<800 and b<480):
                    res[b,a]+=e*weights[i]
    res*=255
    return bw_rw2bin(bw, rw), Image.fromarray(res.astype(np.uint8))
                    
    
#def bin_to_rgb(bin):


if __name__ == "__main__":
    img = Image.open("nemo.jpg")
    bin,rgb = dither_to_bin_and_rgb(img)
    with open("data.bin", "wb") as f:
        f.write(bin)
    rgb.save("data.png")