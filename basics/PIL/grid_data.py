from operator import mul
from PIL import Image, ImageFont, ImageDraw, ImageColor

AnfangszeitenKSBG = {
    "07:40:00" : 48,
    "08:34:00" : 74,
    "09:28:00" : 103,
    "10:30:00" : 132,
    "11:24:00" : 161,

    "12:14:00" : 190,
    "13:04:00" : 219,

    "13:55:00" : 248,
    "14:49:00" : 277,
    "15:43:00" : 306,
    "16:33:00" : 335,
    "17:23:00" : 364,
    # Ab hier Normale ISME-Zeiten Mittwoch
    "18:15:00" : 393,
    "19:05:00" : 422,
    "19:55:00" : 451
}

AnfangszeitenISME = {
    1 : "07:45",
    2 : "08:40",
    3 : "09:35",
    4 : "10:40",
    5 : "11:35",
    6 : "12:25",
    7 : "13:15",
    8 : "14:05",
    9 : "14:55"
}


Wochentage = {
    "Dienstag" : 246,
    "Mittwoch" : 358,
    "Donnerstag" : 470,
    "Freitag" : 582,
    "Samstag" : 694
}

lesson_pixel = [
    [460,48],
    [514,74],
    [568,103],
    [630,132],
    [684,161],

    [734,190],
    [784,219],

    [835,248],
    [889,277],
    [943,306],
    [993,335],
    [1043,364],

    [1095,393],
    [1145,422],
    [1195,451]
]

isme_lesson_pixel = [
    [460,48],
    [520,74],
    [575,103],
    [640,132],
    [695,161],
    [745,190],
    [795,219],
    [845,248],
    [895,277]
]

def minutenrechner(time):
    my_time = time
    factors = (60, 1, 1/60)

    t1 = sum(i*j for i, j in zip(map(int, my_time.split(':')), factors))
    
    print(t1)
    return t1

minutenrechner("14:55:00")

def koordinatenfinder(timein):
    if timein in AnfangszeitenKSBG:
        return AnfangszeitenKSBG[timein]

font = ImageFont.truetype("DejaVuSans-Bold.ttf", size=11)

def hauptsacheeinrechteck(timea, timeb, drawbw):
        #img = Image.new("RGB", (800,480), color=(255,255,255))

    #font = ImageFont.truetype("../pixelperfect/Minimal5x7.ttf", size=32)
    # drawbw = ImageDraw.Draw(bw)
    draw_point = (45,koordinatenfinder(timea))
    drawbw.multiline_text(draw_point, text="Ivo Bloechliger", font=font, fill=0)
    
    # drawbw.rounded_rectangle([(43, koordinatenfinder(timea)), (240, koordinatenfinder(timeb))] , fill ="white", radius=1, outline ="black", width = 1) 
    

def position_box(starttime, endtime):
    starttime_minute = minutenrechner(starttime)
    endtime_minute = minutenrechner(endtime)
    for time in (lesson_pixel):
        #print(time)
        index = lesson_pixel.index(time)
        #print(index)
        #print(lesson_pixel[index])
        if lesson_pixel[index][0]<starttime_minute:
            pass
        else:
            timedifference = lesson_pixel[index-1][0]-starttime_minute
            pixeloffset = int(timedifference*0.644444)
            start_pixel = lesson_pixel[index-1][1] + pixeloffset

        
    for time in enumerate(lesson_pixel):
        if lesson_pixel[index][0] < endtime_minute:
            pass
        else:
            timedifference = lesson_pixel[index-1][0]-endtime_minute
            pixeloffset = int(timedifference*0.644444)
            print(pixeloffset)
            end_pixel = lesson_pixel[index-1][1] + pixeloffset
    print("Startpixel,", start_pixel, end_pixel)
position_box("07:47:00", "08:45:00")

def draw_lesson(subject_short, Class, teacher_short, aditional_info, time, day):
    info = subject_short + " " + Class
    draw_point = (Wochentage[day], AnfangszeitenKSBG[time])
    drawbw.multiline_text(draw_point, text=info, font=font, fill=0)

    info = teacher_short + " " + aditional_info
    draw_point = (Weekdays[day], AnfangszeitenKSBG[time]+14)
    drawbw.multiline_text(draw_point, text=info, font=font, fill=0)

def draw_lesson_today(subject, Class, teacher, aditional_info, time): 
    info = subject + " " + Class
    draw_point = (52, AnfangszeitenKSBG[time])
    drawbw.multiline_text(draw_point, text=info, font=font, fill=0)
    info = teacher + " " + aditional_info
    draw_point = (52, AnfangszeitenKSBG[time]+14)
    drawbw.multiline_text(draw_point, text=info, font=font, fill=0)
    
def draw_reservation_at_lessontime_today(starttime, teacher, time):
    draw_point = (52, AnfangszeitenKSBG[time])
    drawbw.multiline_text(draw_point, text="Reservation", font=font, fill=0)
    draw_point = (52, AnfangszeitenKSBG[time]+14)
    drawbw.multiline_text(draw_point, text=teacher, font=font, fill=0)

def draw_reservation_at_lessontime(starttime, teacher, time, day):
    draw_point = (Weekdays[day], AnfangszeitenKSBG[time])
    drawbw.multiline_text(draw_point, text="Reservation", font=font, fill=0)
    draw_point = (Weekdays[day], AnfangszeitenKSBG[time]+14)
    drawbw.multiline_text(draw_point, text=teacher, font=font, fill=0)

def draw_reservation_today(starttime, endtime, teacher, time):
    drawbw.rounded_rectangle([(43, AnfangszeitenKSBG[time]), (240, AnfangszeitenKSBG[time])] , fill ="white", radius=7, outline ="black", width = 1) 

    info = "reservation" + starttime
    draw_point = (52, AnfangszeitenKSBG[time])
    drawbw.multiline_text(draw_point, text=info, font=font, fill=0)
    info = teacher + endtime
    draw_point = (52, AnfangszeitenKSBG[time]+14)
    drawbw.multiline_text(draw_point, text=info, font=font, fill=0)

def draw_reservation(starttime, endtime, teacher_short,  time, day):
    info = "reservation" + starttime
    draw_point = (Weekdays[day], AnfangszeitenKSBG[time])
    drawbw.multiline_text(draw_point, text=info, font=font, fill=0)
    info = teacher_short + endtime
    draw_point = (Weekdays[day], AnfangszeitenKSBG[time]+14)
    drawbw.multiline_text(draw_point, text=teacher, font=font, fill=0)
