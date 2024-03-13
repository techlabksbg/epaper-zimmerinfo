from PIL import Image, ImageFont, ImageDraw, ImageColor
from time import sleep
from operator import mul
import grid_data as gd
import grid_draw as gr
import grid_data as gd

def get_text_dimensions(text_string, font):
    # https://stackoverflow.com/a/46220683/9263761
    ascent, descent = font.getmetrics()

    text_width = font.getmask(text_string).getbbox()[2]
    text_height = font.getmask(text_string).getbbox()[3] + descent

    return (text_width, text_height)

def initializer():
    bw = Image.new("1", (800,480), color=1)
    drawbw = ImageDraw.Draw(bw)
    gr.grid_drawer(drawbw)
    return bw


bw = initializer()
bw.save("bw.png", "PNG")
bw.show()