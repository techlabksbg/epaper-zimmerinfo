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

def minutenrechner(time):
    my_time = time
    factors = (60, 1, 1/60)

    t1 = sum(i*j for i, j in zip(map(int, my_time.split(':')), factors))
    
    print(t1)
    return t1

minutenrechner("17:40:00")

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