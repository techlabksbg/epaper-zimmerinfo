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

def grid_drawer(drawbw):
    # Draw fat horizontal lines
    # Weekdays and Hours Separator
    drawbw.line([(0, 45), (800, 45)] , fill ="black", width = 2) 
    # Break Line
    drawbw.line([(0, 132), (800, 132)] , fill ="black", width = 2) 
    # Lunch Line
    drawbw.line([(0, 190), (800, 190)] , fill ="black", width = 2) 
    # Lunch Line 2.0
    drawbw.line([(0, 248), (800, 248)] , fill ="black", width = 2) 
    # Above Weekdays Line
    drawbw.line([(0, 22), (800, 22)] , fill ="black", width = 2) 


    for y in range(45, 480, 29):
        shape = [(0, y), (800, y)] 
        drawbw.line(shape, fill ="black", width = 1) 

    #Draw vertical lines
    # Time Separator
    drawbw.line([(40, 22), (40, 480)] , fill ="black", width = 2) 
    for x in range(242, 800, 112):
        shape = [(x, 22), (x, 480)] 
        drawbw.line(shape, fill ="black", width = 1) 

    sleep(2)

    #Draw Lesson Times
    font = ImageFont.truetype("DejaVuSans-Bold.ttf", size=11)
    y = 52
    lesso_times = ["7:40", "8:34", "9:28", "10:30", "11:15", "12:14", "13:04", "13:55", "14:49", "15:43", "16:33", "17:23", "18:15", "19:05", "19:55"]
    weekend_times = ["07:45", "08:40", "09:35", "10:40", "11:35", "12:25", "13:15", "14:05", "14:55"]
    day = "M"
    if day == "Samstag":
        for time in weekend_times:
            draw_point = (2.4, y)
            drawbw.multiline_text(draw_point, text=time, font=font, fill=0)
            y += 29
    else:
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


    font = ImageFont.truetype("DejaVuSans-Bold.ttf", size=11)

    draw_point = (45,4)
    drawbw.multiline_text(draw_point, text="Ivo Bloechliger", font=font, fill=0)

    gd.hauptsacheeinrechteck("09:28:00", "10:13:00", drawbw) 