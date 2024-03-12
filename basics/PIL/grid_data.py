




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