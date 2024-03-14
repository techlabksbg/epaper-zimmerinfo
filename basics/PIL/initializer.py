from PIL import Image, ImageFont, ImageDraw, ImageColor
from time import sleep
from operator import mul
import grid_draw as gd

def initialise_immage():
    bw = Image.new("1", (800,480), color=1)
    drawbw = ImageDraw.Draw(bw)
    return drawbw, bw