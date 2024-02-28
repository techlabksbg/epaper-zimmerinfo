import cairo

WIDTH, HEIGHT = 800, 480


surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
ctx = cairo.Context(surface)
#ctx.scale(WIDTH, HEIGHT)  # Normalizing the canvas

ctx.set_line_width(1)
for i in range(0,480,48):
    ctx.move_to(-0.5,i-0.5)
    ctx.line_to(799.5,i-0.5)
    ctx.stroke()

notperfect = ["PixelPerfect"]
fonts = [ "Pixel Emulator", "High Pixel\-7", "Thirteen Pixel Fonts", "Mini Pixel\-7", "Minimal5x7", ]

for fn,font in enumerate(fonts):
    ctx.select_font_face(font)
    for s in range(10,22,1):
        ctx.set_font_size(s)
        ctx.move_to(10+180*fn, s*20-160)
        ctx.show_text(f"#{font} s={s}")
surface.write_to_png("stdplan.png")  # Output to PNG