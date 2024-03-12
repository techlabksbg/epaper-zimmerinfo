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
