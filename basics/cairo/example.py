# from https://pycairo.readthedocs.io/en/latest/tutorial/introduction.html#example

#!/usr/bin/env python

import math
from math import pi
import cairo

WIDTH, HEIGHT = 256, 256


# from https://github.com/pygobject/pycairo/blob/main/examples/cairo_snippets/snippets/text.py
def draw(cr, width, height):
    cr.scale(width, height)
    cr.set_line_width(0.04)

    cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL,
                        cairo.FONT_WEIGHT_BOLD)
    cr.set_font_size(0.35)

    cr.move_to(0.04, 0.53)
    cr.show_text("Hello")

    cr.move_to(0.27, 0.65)
    cr.text_path("void")
    cr.set_source_rgb(0.5, 0.5, 1)
    cr.fill_preserve()
    cr.set_source_rgb(0, 0, 0)
    cr.set_line_width(0.01)
    cr.stroke()

    # draw helping lines
    cr.set_source_rgba(1, 0.2, 0.2, 0.6)
    cr.arc(0.04, 0.53, 0.02, 0, 2 * pi)
    cr.arc(0.27, 0.65, 0.02, 0, 2 * pi)
    cr.fill()

surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
ctx = cairo.Context(surface)

ctx.scale(WIDTH, HEIGHT)  # Normalizing the canvas

pat = cairo.LinearGradient(0.0, 0.0, 0.0, 1.0)
pat.add_color_stop_rgba(1, 0.7, 0, 0, 0.5)  # First stop, 50% opacity
pat.add_color_stop_rgba(0, 0.9, 0.7, 0.2, 1)  # Last stop, 100% opacity

ctx.rectangle(0, 0, 1, 1)  # Rectangle(x0, y0, x1, y1)
ctx.set_source(pat)
ctx.fill()

ctx.translate(0.1, 0.1)  # Changing the current transformation matrix

ctx.move_to(0, 0)
# Arc(cx, cy, radius, start_angle, stop_angle)
ctx.arc(0.2, 0.1, 0.1, -math.pi / 2, 0)
ctx.line_to(0.5, 0.1)  # Line to (x,y)
# Curve(x1, y1, x2, y2, x3, y3)
ctx.curve_to(0.5, 0.2, 0.5, 0.4, 0.2, 0.8)
ctx.close_path()

ctx.set_source_rgb(0.3, 0.2, 0.5)  # Solid color
ctx.set_line_width(0.02)
ctx.stroke()

draw(ctx, 1, 1)

surface.write_to_png("example.png")  # Output to PNG