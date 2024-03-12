# Ubuntu Linux: sudo apt install python3-pil
# pip install pil

# from https://stackoverflow.com/questions/68648801/generate-image-from-given-text
from PIL import Image, ImageFont, ImageDraw, ImageColor
from time import sleep
from operator import mul
import grid_data as gd

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
drawbw.line([(0, 45), (800, 45)] , fill ="black", width = 2) 
# Pause Linie
drawbw.line([(0, 132), (800, 132)] , fill ="black", width = 2) 
# Mittags Linie
drawbw.line([(0, 190), (800, 190)] , fill ="black", width = 2) 
# Mittags Linie 2.0
drawbw.line([(0, 248), (800, 248)] , fill ="black", width = 2) 
# Über Wochentage Linie
drawbw.line([(0, 22), (800, 22)] , fill ="black", width = 2) 

# AnfangszeitenKSBG = [
#     1 : "07:40",
#     2 : "08:34",
#     3 : "09.28",
#     4 : "10:30",
#     5 : "11:24",
#     6 : "12:14",
#     7 : "13:04",
#     8 : "13:55",
#     9 : "14:49",
#     10 : "15:43",
#     11 : "16:33",
#     12 : "17:23",
#     # Ab hier Normale ISME-Zeiten Mittwoch
#     13 : "18:15",
#     14 : "19:05",
#     15 : "19:55"
# ]

# AnfangszeitenISME = [
#     1 = "07:45",
#     2 = "08:40",
#     3 = "09:35",
#     4 = "10:40",
#     5 = "11:35",
#     6 = "12:25",
#     7 = "13:15",
#     8 = "14:05",
#     9 = "14:55"
# ]

for y in range(45, 480, 29):
    shape = [(0, y), (800, y)] 
    drawbw.line(shape, fill ="black", width = 1) 

#Draw vertical lines
# Zeit Separierer
drawbw.line([(40, 22), (40, 480)] , fill ="black", width = 2) 
for x in range(242, 800, 112):
    shape = [(x, 22), (x, 480)] 
    drawbw.line(shape, fill ="black", width = 1) 

sleep(2)

#Draw Lesson Times
font = ImageFont.truetype("DejaVuSans-Bold.ttf", size=11)
y = 52
lesso_times = ["7:40", "8:34", "9:28", "10:30", "11:15", "12:14", "13:04", "13:55", "14:49", "15:43", "16:33", "17:23"]
for time in lesso_times:
    draw_point = (2.4, y)
    drawbw.multiline_text(draw_point, text=time, font=font, fill=0)
    y += 29
# bw.show() 
sleep(2)

#Draw Days
font = ImageFont.truetype("DejaVuSans-Bold.ttf", size=11)
draw_point = (52, 27)
drawbw.multiline_text(draw_point, text="Heute", font=font, fill=0)

x = 257
days = ["Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag"]
for day in days:
    draw_point = (x, 27)
    drawbw.multiline_text(draw_point, text=day, font=font, fill=0)
    x += 112

# Stunde Konzept
# drawbw.rounded_rectangle([(43, 40), (240, 72)] , fill ="white", radius=50, outline ="black", width = 1) 

drawbw.rounded_rectangle([(43, 76), (240, 146)] , fill ="white", radius=10, outline ="black", width = 1) 

font = ImageFont.truetype("DejaVuSans-Bold.ttf", size=11)

draw_point = (52, 46)
drawbw.multiline_text(draw_point, text="Test um zu sehen, ob es geht", font=font, fill=0)

draw_point = (52, 60)
drawbw.multiline_text(draw_point, text="Anderer Versuch", font=font, fill=0)

drawbw.rounded_rectangle([(244, 48), (352, 72)] , fill ="white", radius=7, outline ="black", width = 1) 

draw_point = (246, 48)
drawbw.multiline_text(draw_point, text="Reserviert 23.59", font=font, fill="#FF0000" )

draw_point = (246, 58)
drawbw.multiline_text(draw_point, text="Reserviert 23.59", font=font, fill=0)

draw_point = (2,2)
drawbw.multiline_text(draw_point, text=".", font=font, fill=0)

draw_point = (45,4)
drawbw.multiline_text(draw_point, text="Ivo Bloechliger", font=font, fill=0)

gd.hauptsacheeinrechteck("09:28:00", "10:13:00", drawbw)

bw.save("bw.png", "PNG")
bw.show() 
