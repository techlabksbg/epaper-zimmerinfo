from PIL import Image, ImageFont, ImageDraw, ImageColor
from time import sleep
from operator import mul
import grid_draw as gd

def initialise_immage_b():
    bw = Image.new("1", (800,480), color=1)
    drawbw = ImageDraw.Draw(bw)
    return drawbw, bw

def initialise_immage_r():
    rw = Image.new("1", (800,480), color=1)
    drawrw = ImageDraw.Draw(rw)
    return drawrw, rw