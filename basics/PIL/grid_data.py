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


def draw_lesson(day, time, subject_short, Class, teacher_short, aditional_info): #day defines the starting day in int (2-7)
    info = subject_short + " " + Class
    draw_point = (52, AnfangszeitenKSBG[time])
    drawbw.multiline_text(draw_point, text=info, font=font, fill=0)
    info = teacher_short + " " + aditional_info
    draw_point = (52, AnfangszeitenKSBG[time]+14)
    drawbw.multiline_text(draw_point, text=info, font=font, fill=0)

def draw_lesson(day, time, subject, Class, teacher, aditional_info): #day defines the starting day in int (2-7)
    info = subject + " " + Class
    draw_point = (52, AnfangszeitenKSBG[time])
    drawbw.multiline_text(draw_point, text=info, font=font, fill=0)
    info = teacher + " " + aditional_info
    draw_point = (52, AnfangszeitenKSBG[time]+14)
    drawbw.multiline_text(draw_point, text=info, font=font, fill=0)
    
def draw_reservation_at_lessontime_Today(starttime, teacher):
    draw_point = (52, AnfangszeitenKSBG[time])
    drawbw.multiline_text(draw_point, text="Reservation", font=font, fill=0)
    draw_point = (52, AnfangszeitenKSBG[time]+14)
    drawbw.multiline_text(draw_point, text=teacher, font=font, fill=0)

def draw_reservation_at_lessontime(starttime, teacher):
    draw_point = (52, AnfangszeitenKSBG[time])
    drawbw.multiline_text(draw_point, text="Reservation", font=font, fill=0)
    draw_point = (52, AnfangszeitenKSBG[time]+14)
    drawbw.multiline_text(draw_point, text=teacher, font=font, fill=0)

def draw_reservation_Today(starttime, teacher):
    draw_point = (52, AnfangszeitenKSBG[time])
    drawbw.multiline_text(draw_point, text="Reservation", font=font, fill=0)
    draw_point = (52, AnfangszeitenKSBG[time]+14)
    drawbw.multiline_text(draw_point, text=teacher, font=font, fill=0)

def draw_reservation(starttime, teacher_short):
    draw_point = (52, AnfangszeitenKSBG[time])
    drawbw.multiline_text(draw_point, text="Reservation", font=font, fill=0)
    draw_point = (52, AnfangszeitenKSBG[time]+14)
    drawbw.multiline_text(draw_point, text=teacher, font=font, fill=0)
