
def draw_lesson(day, time, subject, Class, teacher): #day defines the starting day in int (2-7)
    x = day*112+145
    if time == "7:40":
        info = subject + Class + teacher
        draw_point = (x, 51)
        drawbw.multiline_text(draw_point, text=info, font=font, fill=0)
    if time == "8:25":
        info = subject + Class + teacher
        draw_point = (x, 88)
        drawbw.multiline_text(draw_point, text=info, font=font, fill=0)
    if time == "9:34":
        info = subject + Class + teacher
        draw_point = (x, 125)
        drawbw.multiline_text(draw_point, text=info, font=font, fill=0)
    if time == "10:30":
        info = subject + Class + teacher
        draw_point = (x, 162)
        drawbw.multiline_text(draw_point, text=info, font=font, fill=0)
    if time == "11:15":
        info = subject + Class + teacher
        draw_point = (x, 199)
        drawbw.multiline_text(draw_point, text=info, font=font, fill=0)
    if time == "12:14":
        info = subject + Class + teacher
        draw_point = (x, 236)
        drawbw.multiline_text(draw_point, text=info, font=font, fill=0)
    if time == "13:04":
        info = subject + Class + teacher
        draw_point = (x, 273)
        drawbw.multiline_text(draw_point, text=info, font=font, fill=0)
    if time == "13:55":
        info = subject + Class + teacher
        draw_point = (x, 310)
        drawbw.multiline_text(draw_point, text=info, font=font, fill=0)
    if time == "14:49":
        info = subject + Class + teacher
        draw_point = (x, 347)
        drawbw.multiline_text(draw_point, text=info, font=font, fill=0)
    if time == "15:43":
        info = subject + Class + teacher
        draw_point = (x, 384)
        drawbw.multiline_text(draw_point, text=info, font=font, fill=0)
    if time == "16:33":
        info = subject + Class + teacher
        draw_point = (x, 421)
        drawbw.multiline_text(draw_point, text=info, font=font, fill=0)
    if time == "17:23":
        info = subject + Class + teacher
        draw_point = (x, 458)
        drawbw.multiline_text(draw_point, text=info, font=font, fill=0)

def draw_lesson_today(time, subject, Class, teacher): 
    if time == "7:40":
        info = subject + Class + teacher
        draw_point = (52, 51)
        drawbw.multiline_text(draw_point, text=info, font=font, fill=0)
    if time == "8:25":
        info = subject + Class + teacher
        draw_point = (52, 88)
        drawbw.multiline_text(draw_point, text=info, font=font, fill=0)
    if time == "9:34":
        info = subject + Class + teacher
        draw_point = (52, 125)
        drawbw.multiline_text(draw_point, text=info, font=font, fill=0)
    if time == "10:30":
        info = subject + Class + teacher
        draw_point = (52, 162)
        drawbw.multiline_text(draw_point, text=info, font=font, fill=0)
    if time == "11:15":
        info = subject + Class + teacher
        draw_point = (52, 199)
        drawbw.multiline_text(draw_point, text=info, font=font, fill=0)
    if time == "12:14":
        info = subject + Class + teacher
        draw_point = (52, 236)
        drawbw.multiline_text(draw_point, text=info, font=font, fill=0)
    if time == "13:04":
        info = subject + Class + teacher
        draw_point = (52, 273)
        drawbw.multiline_text(draw_point, text=info, font=font, fill=0)
    if time == "13:55":
        info = subject + Class + teacher
        draw_point = (52, 310)
        drawbw.multiline_text(draw_point, text=info, font=font, fill=0)
    if time == "14:49":
        info = subject + Class + teacher
        draw_point = (52, 347)
        drawbw.multiline_text(draw_point, text=info, font=font, fill=0)
    if time == "15:43":
        info = subject + Class + teacher
        draw_point = (52, 384)
        drawbw.multiline_text(draw_point, text=info, font=font, fill=0)
    if time == "16:33":
        info = subject + Class + teacher
        draw_point = (52, 421)
        drawbw.multiline_text(draw_point, text=info, font=font, fill=0)
    if time == "17:23":
        info = subject + Class + teacher
        draw_point = (52, 458)
        drawbw.multiline_text(draw_point, text=info, font=font, fill=0)