
# Ubuntu Linux: sudo apt install python3-pil
# pip install pil

# from https://stackoverflow.com/questions/68648801/generate-image-from-given-text
from PIL import Image, ImageFont, ImageDraw, ImageColor

#img = Image.new("RGB", (800,480), color=(255,255,255))
bw = Image.new("1", (800,480), color=1)

#font = ImageFont.truetype("../pixelperfect/Minimal5x7.ttf", size=32)
drawbw = ImageDraw.Draw(bw)
y = 10
for s in range(8,27):
    font = ImageFont.truetype("../pixelperfectfonts/Minimal5x7.ttf", size=s)
    draw_point = (10, y)
    text = f"s={s} Minimal5x7 0123456789"
    w,h = drawbw.textsize(text, font=font)
    drawbw.multiline_text(draw_point, text=text, font=font, fill=0)
    drawbw.rectangle(((draw_point[0]-1, draw_point[1]-1),(draw_point[0]+w+1,draw_point[1]+h+1)))
    #drawbw.line(((10,s*10-79),(790,s*10-79)), fill=0,width=1)
    font = ImageFont.truetype("DejaVuSans.ttf", size=s)
    text = f"s={s} The brown fox jumps over the lazy dog"
    draw_point = (20+w, y)
    w,h = drawbw.textsize(text, font=font)
    drawbw.multiline_text(draw_point, text=text, font=font, fill=0)
    drawbw.rectangle(((draw_point[0]-1, draw_point[1]-1),(draw_point[0]+w+1,draw_point[1]+h+1)))
    font = ImageFont.truetype("DejaVuSans-Bold.ttf", size=s)
    text = f"s={s} Déja vu Äöï"
    draw_point = (10+w+draw_point[0], y)
    w,h = drawbw.textsize(text, font=font)
    drawbw.multiline_text(draw_point, text=text, font=font, fill=0)
    drawbw.rectangle(((draw_point[0]-1, draw_point[1]-1),(draw_point[0]+w+1,draw_point[1]+h+1)))
    y+=h+4

bw.save("bw.png", "PNG")
