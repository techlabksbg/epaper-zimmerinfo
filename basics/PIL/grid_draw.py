# Ubuntu Linux: sudo apt install python3-pil
# pip install pil

# from https://stackoverflow.com/questions/68648801/generate-image-from-given-text
from PIL import Image, ImageFont, ImageDraw, ImageColor
from time import sleep
from operator import mul
import grid_data as gd

def grid_drawer(drawbw, current_week_day, roomnumber, teacher):
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
    
    if current_week_day == 5:
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
    week_days = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag"]
    font = ImageFont.truetype("DejaVuSans-Bold.ttf", size=11)
    draw_point = (52, 27)
    drawbw.multiline_text(draw_point, text="Heute " + week_days[current_week_day], font=font, fill=0)
    x = 257
    for i in range(1,6):
        draw_point = (x, 27)
        drawbw.multiline_text(draw_point, text=week_days[current_week_day+i], font=font, fill=0)
        x += 112


    # Battery indicator
    font = ImageFont.truetype("DejaVuSans-Bold.ttf", size=11)

    draw_point = (45,4)
    drawbw.multiline_text(draw_point, text=teacher, font=font, fill=0)

    drawbw.rounded_rectangle([(766, 4), (794, 16)] , fill ="white", radius=0, outline ="black", width = 1) 

    prozent = 100
    x = 32-(prozent/100*24)
    y = 792-(prozent/100*24)

    drawbw.rounded_rectangle([(y, 6), (792, 14)] , fill ="black", radius=0, outline ="black", width = 1) 

    drawbw.rectangle([(764,9),(765,11)])

    
    # Room number
    draw_point = (7,27)
    drawbw.multiline_text(draw_point, text=roomnumber , font=font, fill=0)
