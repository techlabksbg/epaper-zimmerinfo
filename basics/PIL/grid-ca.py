
# Ubuntu Linux: sudo apt install python3-pil
# pip install pil

# from https://stackoverflow.com/questions/68648801/generate-image-from-given-text
from PIL import Image, ImageFont, ImageDraw, ImageColor
from time import sleep

# https://levelup.gitconnected.com/how-to-properly-calculate-text-size-in-pil-images-17a2cc6f51fd
def get_text_dimensions(text_string, font):
    # https://stackoverflow.com/a/46220683/9263761
    ascent, descent = font.getmetrics()

    text_width = font.getmask(text_string).getbbox()[2]
    text_height = font.getmask(text_string).getbbox()[3] + descent

    return (text_width, text_height)

#img = Image.new("RGB", (800,480), color=(255,255,255))
bw = Image.new("1", (800,480), color=1)

# Draw horizontal lines
drawbw = ImageDraw.Draw(bw)
for y in range(37, 480, 37):
    shape = [(0, y), (800, y)] 
    drawbw.line(shape, fill ="black", width = 2) 

#Draw vertical lines
drawbw.line([(40, 0), (40, 480)] , fill ="black", width = 2) 
for x in range(242, 800, 112):
    shape = [(x, 0), (x, 480)] 
    drawbw.line(shape, fill ="black", width = 2) 

sleep(2)

#Draw Lesson Times
font = ImageFont.truetype("DejaVuSans-Bold.ttf", size=11)
y = 51
lesso_times = ["7:40", "8:34", "9:28", "10:30", "11:15", "12:14", "13:04", "13:55", "14:49", "15:43", "16:33", "17:23"]
for time in lesso_times:
    draw_point = (2.4, y)
    drawbw.multiline_text(draw_point, text=time, font=font, fill=0)
    y += 37
bw.show() 
sleep(2)

#Draw Lesson Times
font = ImageFont.truetype("DejaVuSans-Bold.ttf", size=11)
draw_point = (52, 11)
drawbw.multiline_text(draw_point, text="Montag", font=font, fill=0)

x = 257
days = ["Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag"]
for day in days:
    draw_point = (x, 11)
    drawbw.multiline_text(draw_point, text=day, font=font, fill=0)
    x += 112
bw.show() 
bw.save("bw.png", "PNG")

