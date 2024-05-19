from PIL import Image, ImageOps
import numpy as np
import sys

def newBWimage(size=(800,480)):
    """
    Erzeugt ein weisses Schwarz-Weiss Image
    """
    return Image.new("1",size,color=1)


def resizeAndCenter(image, size=(800,480)):
    """
    Passt ein Bild auf die Grösse des Displays an und
    zentriert es, füllt allfällige Ränder mit Weiss
    """
    return ImageOps.pad(image, size,color="white")
        

def bw_rw2bin(bw, rw, size=(800,480)):
    """
    returns a Byte Array with with a bw und rw bitmap.
    Suitable to send to the display
    """
    #bw = bw.composite(bw, )
    if (bw.size!=size):
        bw = resizeAndCenter(bw, size)
    if (rw.size!=size):
        rw = resizeAndCenter(rw, size)
    if (bw.format!="1"):
        bw = bw.convert("1")
    if (rw.format!="1"):
        rw = rw.convert("1")
    
    # Set all pixels that are both red and black to black (i.e. set red to white)
    b = np.array(bw)
    r = np.array(rw)
    r[:,:][b[:,:]==0] = 1
    rw = Image.fromarray(r)
    print(f"bw_rw2bin len(bw)={len(bw.to_bytes())} len(rw)={len(rw.to_bytes())}", file=sys.stderr)
    return bytes(bw.tobytes())+bytes(rw.tobytes())

def bw_rw2rgb(bw, rw, size=(800,480)):
    if (bw.size!=size):
        bw = resizeAndCenter(bw)
    if (rw.size!=size):
        rw = resizeAndCenter(rw)
    b = bw.convert("RGB")
    r = rw.convert("RGB")
    datab = np.array(b)
    datar = np.array(r)
    # Convert all pixels that are black and red to black (i.e. white on the red bitmap)
    datar[:,:,:3][datab[:,:,0]==0] = [255,255,255]
    datar[:,:,:3][datar[:,:,0]==0] = [255,0,0]  # Replace all black with red
    datar[:,:,:3][datab[:,:,0]==0] = [0,0,0]    # Copy black pixels as black

    return Image.fromarray(datar)


def dither_to_bin_and_rgb(image, size=(800,480)):
    if (image.size!=size):
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
    for y in range(size[1]):
        for x in range(size[0]):
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