
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
# Wochentage und Stunden Separierer
drawbw.line([(0, 37), (800, 37)] , fill ="black", width = 2) 
# Pause Linie
drawbw.line([(0, 148), (800, 148)] , fill ="black", width = 2) 
# Mittags Linie
drawbw.line([(0, 222), (800, 222)] , fill ="black", width = 2) 
# Mittags Linie 2.0
drawbw.line([(0, 296), (800, 296)] , fill ="black", width = 2) 


for y in range(37, 480, 37):
    shape = [(0, y), (800, y)] 
    drawbw.line(shape, fill ="black", width = 1) 

#Draw vertical lines
# Zeit Separierer
drawbw.line([(40, 0), (40, 480)] , fill ="black", width = 2) 
for x in range(242, 800, 112):
    shape = [(x, 0), (x, 480)] 
    drawbw.line(shape, fill ="black", width = 1) 

sleep(2)

#Draw Lesson Times
font = ImageFont.truetype("DejaVuSans-Bold.ttf", size=11)
y = 51
lesso_times = ["7:40", "8:34", "9:28", "10:30", "11:15", "12:14", "13:04", "13:55", "14:49", "15:43", "16:33", "17:23"]
for time in lesso_times:
    draw_point = (2.4, y)
    drawbw.multiline_text(draw_point, text=time, font=font, fill=0)
    y += 37
# bw.show() 
sleep(2)

#Draw Days
font = ImageFont.truetype("DejaVuSans-Bold.ttf", size=11)
draw_point = (52, 11)
drawbw.multiline_text(draw_point, text="Heute", font=font, fill=0)

x = 257
days = ["Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag"]
for day in days:
    draw_point = (x, 11)
    drawbw.multiline_text(draw_point, text=day, font=font, fill=0)
    x += 112

# Stunde Konzept
drawbw.rounded_rectangle([(43, 40), (240, 72)] , fill ="white", radius=50, outline ="black", width = 1) 

drawbw.rounded_rectangle([(43, 76), (240, 146)] , fill ="white", radius=10, outline ="black", width = 1) 

font = ImageFont.truetype("DejaVuSans-Bold.ttf", size=11)

draw_point = (52, 42)
drawbw.multiline_text(draw_point, text="Test um zu sehen, ob es geht", font=font, fill=0)

draw_point = (52, 58)
drawbw.multiline_text(draw_point, text="Anderer Versuch", font=font, fill=0)

drawbw.rounded_rectangle([(244, 40), (352, 72)] , fill ="white", radius=7, outline ="black", width = 1) 

draw_point = (246, 42)
drawbw.multiline_text(draw_point, text="Reserviert 23.59", font=font, fill=0)


bw.save("bw.png", "PNG")
bw.show() 