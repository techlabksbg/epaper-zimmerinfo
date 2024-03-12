from PIL import Image, ImageFont, ImageDraw, ImageColor
import numpy as np

def combine_bw_rw(bw, rw):
    rgb = Image.new("RGB", rw.size, color=(255,255,255))
    data = np.array(rgb)   # "data" is a height x width x 3 numpy array
    bwdata = np.array(bw)
    rwdata = np.array(rw)
    data[bwdata==False] = (0,0,0)
    data[rwdata==False] = (255,0,0)
    return Image.fromarray(data)

if __name__=="__main__":

    font = ImageFont.truetype("DejaVuSans.ttf", size=30)
    bw = Image.new("1", (800,480), color=1)
    rw = Image.new("1", (800,480), color=1)
    drawbw = ImageDraw.Draw(bw)
    drawbw.multiline_text((20,100), text="Das ist Schwarz!", font=font, fill=0)

    drawrw = ImageDraw.Draw(rw)
    drawrw.multiline_text((20,200), text="Das ist Rot!", font=font, fill=0)

    rgb = combine_bw_rw(bw, rw)
    rgb.show()



