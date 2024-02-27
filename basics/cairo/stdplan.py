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


ctx.select_font_face("Minimal5x7")
ctx.set_font_size(16)
ctx.move_to(10, 80)
ctx.show_text(f"Hello mit Schrift Minimal5x7 mit Grösse 16 être à blà blé maïs...")
surface.write_to_png("stdplan.png")  # Output to PNG