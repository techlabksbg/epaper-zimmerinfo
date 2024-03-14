from operator import mul
from PIL import Image, ImageFont, ImageDraw, ImageColor
from event import Event
import initializer as init


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
    "07:45:00" : 48,
    "08:40:00" : 74,
    "09:35:00" : 103,
    "10:40:00" : 132,
    "11:35:00" : 161,
    "12:25:00" : 190,
    "13:15:00" : 219,
    "14:05:00" : 248,
    "14:55:00" : 277
}


Wochentage = [
    0,
    246,
    358,
    470,
    582,
    694
]

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

    return t1


def position_box_normal(starttime, endtime, anfangszeiten):
    starttime_minute = minutenrechner(starttime)
    endtime_minute = minutenrechner(endtime)
    for time in (lesson_pixel):
        index = lesson_pixel.index(time)
        if lesson_pixel[index][0]<starttime_minute:
            pass
        else:
            timedifference = lesson_pixel[index-1][0]-starttime_minute
            pixeloffset = int(timedifference*0.644444)
            start_pixel = lesson_pixel[index-1][1] + pixeloffset
            break
    for time in (lesson_pixel):
        index = lesson_pixel.index(time)
        if lesson_pixel[index][0] < endtime_minute:
            pass
        else:
            timedifference = lesson_pixel[index-1][0]-endtime_minute
            pixeloffset = int(timedifference*0.644444)
            end_pixel = lesson_pixel[index-1][1] + pixeloffset
            break
    if end_pixel - start_pixel < 24:
        end_pixel = start_pixel + 24
    coordinates = [start_pixel, end_pixel]
    print("Startpixel,", start_pixel, end_pixel)
    return coordinates

def position_box_isme(starttime, endtime, anfangszeiten):
    starttime_minute = minutenrechner(starttime)
    endtime_minute = minutenrechner(endtime)
    start_pixel = 0
    end_pixel = 0
    for time in (isme_lesson_pixel):
        index = isme_lesson_pixel.index(time)
        if isme_lesson_pixel[index][0]<starttime_minute:
            pass
        else:
            timedifference = isme_lesson_pixel[index-1][0]-starttime_minute
            pixeloffset = int(timedifference*0.644444)
            start_pixel = isme_lesson_pixel[index-1][1] + pixeloffset
            break
    for time in (isme_lesson_pixel):
        index = isme_lesson_pixel.index(time)
        if isme_lesson_pixel[index][0] < endtime_minute:
            pass
        else:
            timedifference = isme_lesson_pixel[index-1][0]-endtime_minute
            pixeloffset = int(timedifference*0.644444)
            end_pixel = isme_lesson_pixel[index-1][1] + pixeloffset
            break
    if end_pixel - start_pixel < 24:
        end_pixel = start_pixel + 24
    coordinates = [start_pixel, end_pixel]
    print("Startpixel,", start_pixel, end_pixel)
    return coordinates

def check_isme_or_not(weekday): #0=Montag, 6 == Sonntag
    if weekday == 5:
        anfangszeiten = AnfangszeitenISME
    else:
        anfangszeiten = AnfangszeitenKSBG
    return anfangszeiten

def battery_indicator(battery_percent, drawbw, drawrw):
    drawbw.rounded_rectangle([(766, 4), (794, 16)] , fill ="white", radius=0, outline ="black", width = 1) 
    drawbw.rectangle([(764,9),(765,11)])

    y = 792-(battery_percent*24)

    if battery_percent < 26:
        drawrw.rounded_rectangle([(y, 6), (792, 14)] , fill ="black", radius=0, outline ="black", width = 1) 

    else:
        drawbw.rounded_rectangle([(y, 6), (792, 14)] , fill ="black", radius=0, outline ="black", width = 1) 


def draw_lesson(drawbw, subject_short, Class, teacher_short, aditional_info, time, day, Anfangszeiten, font):
    info = subject_short + " " + Class
    draw_point = (Wochentage[day], Anfangszeiten[time])
    drawbw.multiline_text(draw_point, text=info, font=font, fill=0)

    info = teacher_short + " " + aditional_info
    draw_point = (Wochentage[day], Anfangszeiten[time]+14)
    drawbw.multiline_text(draw_point, text=info, font=font, fill=0)

def draw_lesson_today(drawbw, subject, Class, teacher, aditional_info, time, Anfangszeiten, font): 
    info = subject + " " + Class
    draw_point = (52, Anfangszeiten[time])
    drawbw.multiline_text(draw_point, text=info, font=font, fill=0)
    info = teacher + " " + aditional_info
    draw_point = (52, Anfangszeiten[time]+14)
    drawbw.multiline_text(draw_point, text=info, font=font, fill=0)
    
def draw_reservation_at_lessontime_today(drawbw, starttime, teacher, time, Anfangszeiten, font):
    draw_point = (52, Anfangszeiten[time])
    drawbw.multiline_text(draw_point, text="Reservation", font=font, fill=0)
    draw_point = (52, Anfangszeiten[time]+14)
    drawbw.multiline_text(draw_point, text=teacher, font=font, fill=0)

def draw_reservation_at_lessontime(drawbw, starttime, teacher, time, day, Anfangszeiten, font):
    draw_point = (Wochentage[day], Anfangszeiten[time])
    drawbw.multiline_text(draw_point, text="Reservation", font=font, fill=0)
    drawbw.multiline_text((400, 200), text="Reservation", font=font, fill=0)
    draw_point = (Wochentage[day], Anfangszeiten[time]+14)
    drawbw.multiline_text(draw_point, text=teacher, font=font, fill=0)

def draw_reservation_today(drawbw, starttime, endtime, teacher, time, Anfangszeiten, current_weekday, font):
    if current_weekday != 5:
        position = position_box_normal(starttime=starttime, endtime=endtime, anfangszeiten=Anfangszeiten)
    else:
        position = position_box_isme(starttime=starttime, endtime=endtime, anfangszeiten=Anfangszeiten)
    drawbw.rounded_rectangle([(43, position[0]), (240, position[1])] , fill ="white", radius=7, outline ="black", width = 1) 
    info = "reservation" + starttime[:-3]
    draw_point = (52, position[0])
    drawbw.multiline_text(draw_point, text=info, font=font, fill=0)
    info = teacher + endtime[:-3]
    draw_point = (52, Anfangszeiten[time]+14)
    drawbw.multiline_text(draw_point, text=info, font=font, fill=0)

def draw_reservation(drawbw, starttime, endtime, teacher_short,  time, day, Anfangszeiten, font):
    position = position_box_isme(starttime=starttime, endtime=endtime, anfangszeiten = Anfangszeiten)
    drawbw.rounded_rectangle([(Wochentage[day], position[0]), (Wochentage[day]+108, position[1])] , fill ="white", radius=7, outline ="black", width = 1) 
    info = "reservation" + starttime[:-3]
    print(Anfangszeiten)
    draw_point = (Wochentage[day], Anfangszeiten[time])
    drawbw.multiline_text(draw_point, text=info, font=font, fill=0)
    info = teacher_short + endtime[:-3]
    draw_point = (Wochentage[day], Anfangszeiten[time]+14)
    drawbw.multiline_text(draw_point, text=teacher_short, font=font, fill=0)


def draw_data(current_weekday, current_date, event_date, starttime, endtime, subject, Class, teacher, aditional_info, time, subject_short, teacher_short, weekday, reservator, drawbw, font, bw, text, drawrw, rw):
    anfangszeiten = check_isme_or_not(weekday)
    if Class == None:
        Class = " "
    if subject == None:
        subject = " "
    if subject_short == None:
        subject_short = " "
    if "2024-03-18" == str(event_date):
        if text != "Reserviert":
            draw_lesson_today(drawbw, subject, Class, teacher, aditional_info, time, anfangszeiten, font)
        else:
            if starttime in anfangszeiten:
                draw_reservation_at_lessontime_today(drawbw, starttime, teacher, time, anfangszeiten, font)
            else:
                draw_reservation_today(drawbw, starttime, endtime, teacher, time, anfangszeiten, current_weekday, font)


    else:
        if text != "Reserviert":
            draw_lesson(drawbw, subject_short, Class, teacher_short, aditional_info, time, weekday, anfangszeiten, font)
        else:
            if starttime in anfangszeiten:
                draw_reservation_at_lessontime(drawbw, starttime, teacher, time, weekday, anfangszeiten, font)
            else:
                draw_reservation(drawbw, starttime, endtime, teacher, time, current_weekday, anfangszeiten, font)

    bw.save("bw.png", "PNG")
    rw.save("rw.png", "PNG")

    rgb = init.combine_bw_rw(bw, rw)
    rgb.show()

    

