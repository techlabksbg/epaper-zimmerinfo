AnfangszeitenKSBG = [
    "07:40" : 48,
    "08:34" : 74,
    "09.28" : 103,
    "10:30" : 132,
    "11:24" : 161,
    "12:14" : 190,
    "13:04" : 219,
    "13:55" : 248,
    "14:49" : 277,
    "15:43" : 306,
    "16:33" : 335,
    "17:23" : 364,
    # Ab hier Normale ISME-Zeiten Mittwoch
    "18:15" : 393,
    "19:05" : 422,
    "19:55" : 451
]

Wochentage = [
    "Dienstag" : 246,
    "Mittwoch" : 358,
    "Donnerstag" : 470,
    "Freitag" : 582,
    "Samstag" : 694
]




def draw_lesson(subject_short, Class, teacher_short, aditional_info, time, day): #day defines the starting day in int (2-7)
    info = subject_short + " " + Class
    draw_point = (Wochentage[day], AnfangszeitenKSBG[time])
    drawbw.multiline_text(draw_point, text=info, font=font, fill=0)
    info = teacher_short + " " + aditional_info
    draw_point = (52, AnfangszeitenKSBG[time]+14)
    drawbw.multiline_text(draw_point, text=info, font=font, fill=0)

def draw_lesson_today(subject, Class, teacher, aditional_info, time): #day defines the starting day in int (2-7)
    info = subject + " " + Class
    draw_point = (52, AnfangszeitenKSBG[time])
    drawbw.multiline_text(draw_point, text=info, font=font, fill=0)
    info = teacher + " " + aditional_info
    draw_point = (52, AnfangszeitenKSBG[time]+14)
    drawbw.multiline_text(draw_point, text=info, font=font, fill=0)
    
def draw_reservation_at_lessontime_Today(starttime, teacher, time):
    draw_point = (52, AnfangszeitenKSBG[time])
    drawbw.multiline_text(draw_point, text="Reservation", font=font, fill=0)
    draw_point = (52, AnfangszeitenKSBG[time]+14)
    drawbw.multiline_text(draw_point, text=teacher, font=font, fill=0)

def draw_reservation_at_lessontime(starttime, teacher, time, day):
<<<<<<< HEAD
    if time == "7:40":
        draw_point = (x, 51)
        drawbw.multiline_text(draw_point, text=info, font=font, fill=0)
    if time == "8:25":
        draw_point = (x, 88)
        drawbw.multiline_text(draw_point, text=info, font=font, fill=0)
    if time == "9:34":
        draw_point = (x, 125)
        drawbw.multiline_text(draw_point, text=info, font=font, fill=0)
    if time == "10:30":
        draw_point = (x, 162)
        drawbw.multiline_text(draw_point, text=info, font=font, fill=0)
    if time == "11:15":
        draw_point = (x, 199)
        drawbw.multiline_text(draw_point, text=info, font=font, fill=0)
    if time == "12:14":
        draw_point = (x, 236)
        drawbw.multiline_text(draw_point, text=info, font=font, fill=0)
    if time == "13:04":
        draw_point = (x, 273)
        drawbw.multiline_text(draw_point, text=info, font=font, fill=0)
    if time == "13:55":
        draw_point = (x, 310)
        drawbw.multiline_text(draw_point, text=info, font=font, fill=0)
    if time == "14:49":
        draw_point = (x, 347)
        drawbw.multiline_text(draw_point, text=info, font=font, fill=0)
    if time == "15:43":
        draw_point = (x, 384)
        drawbw.multiline_text(draw_point, text=info, font=font, fill=0)
    if time == "16:33":
        draw_point = (x, 421)
        drawbw.multiline_text(draw_point, text=info, font=font, fill=0)
    if time == "17:23":
        draw_point = (x, 458)
        drawbw.multiline_text(draw_point, text=info, font=font, fill=0)
=======
    draw_point = (Wochentage[day], AnfangszeitenKSBG[time])
    drawbw.multiline_text(draw_point, text="Reservation", font=font, fill=0)
    draw_point = (52, AnfangszeitenKSBG[time]+14)
    drawbw.multiline_text(draw_point, text=teacher, font=font, fill=0)

def draw_reservation_Today(starttime, endtime, teacher, time):
    info = "reservation" + starttime
    draw_point = (52, AnfangszeitenKSBG[time])
    drawbw.multiline_text(draw_point, text=info, font=font, fill=0)
    info = teacher + endtime
    draw_point = (52, AnfangszeitenKSBG[time]+14)
    drawbw.multiline_text(draw_point, text=info, font=font, fill=0)

def draw_reservation(starttime, endtime, teacher_short,  time, day):
    info = "reservation" + starttime
    draw_point = (52, AnfangszeitenKSBG[time])
    drawbw.multiline_text(draw_point, text=info, font=font, fill=0)
    info = teacher_short + endtime
    draw_point = (52, AnfangszeitenKSBG[time]+14)
    drawbw.multiline_text(draw_point, text=info, font=font, fill=0)