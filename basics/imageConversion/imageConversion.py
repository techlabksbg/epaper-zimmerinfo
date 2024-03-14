from PIL import Image, ImageOps
import io

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

"""
def ditherRGB(image):
    colors = [(0,0,0), (255,0,0), (255,255,255)]
    if (image.size!=(800,480)):
        image = resizeAndCenter(image)
    if (image.format!="RGB"):
        image = image.convert("RGB")

    
    def dist(c1, c2):
        

    for y in range(800):
        for x in range(480):


    rgb = Image.new("RGB", rw.size, color=(255,255,255))
    data = np.array(rgb)   # "data" is a height x width x 3 numpy array
    bwdata = np.array(bw)
    rwdata = np.array(rw)
    data[bwdata==False] = (0,0,0)
    data[rwdata==False] = (255,0,0)
    return Image.fromarray(data)

        
"""


if __name__ == "__main__":
    bw = Image.open("bw.png")
    rw = Image.open("rw.png")
    with open("data.bin", "wb") as f:
        bytes = bw_rw2bin(bw,rw)
        f.write(bytes)
