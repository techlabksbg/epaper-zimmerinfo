from PIL import Image, ImageFont, ImageDraw, ImageColor
from time import sleep
from operator import mul
import grid_draw as gd

def initialise_image_b():
    bw = Image.new("1", (800,480), color=1)
    drawbw = ImageDraw.Draw(bw)
    return drawbw, bw

def initialise_image_r():
    rw = Image.new("1", (800,480), color=1)
    drawrw = ImageDraw.Draw(rw)
    return drawrw, rw

def combine_bw_rw(bw, rw):
    rgb = Image.new("RGB", rw.size, color=(255,255,255))
    data = np.array(rgb)   # "data" is a height x width x 3 numpy array
    bwdata = np.array(bw)
    rwdata = np.array(rw)
    data[bwdata==False] = (0,0,0)
    data[rwdata==False] = (255,0,0)
    return Image.fromarray(data)