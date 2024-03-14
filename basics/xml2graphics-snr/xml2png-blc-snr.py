from lxml import etree
from event import Event
from week import Week
# from day import Day
from datetime import date, timedelta
import deutsch
from PIL import Image, ImageFont, ImageDraw #, ImageColor
import datetime

def erzeuge_stundenplan(zimmer = "G14", besitzer = "Mister X", batteriestand = 0.7):

    anfangszeiten_ksbg = [
        "07:40",
        "08:34",
        "09:28",
        "10:30",
        "11:24",

        "12:14",
        "13:04",

        "13:55",
        "14:49",
        "15:43",
        "16:33",
        "17:23",
        # Ab hier Normale ISME-Zeiten Mittwoch
        "18:15",
        "19:05",
        "19:55",
    ]

    anfangszeiten_isme = [
        "07:45",
        "08:40",
        "09:35",
        "10:40",
        "11:35",
        "12:25",
        "13:15",
        "14:05",
        "14:55"
    ]

    display_hoehe = 480
    display_breite = 800

    plan_topleft_x, plan_topleft_y = 0, 60
    anzahl_spalten, anzahl_zeilen = 7, max(len(anfangszeiten_ksbg), len(anfangszeiten_isme))

    stundenplan_breite, stundenplan_hoehe = display_breite - plan_topleft_x, display_hoehe - plan_topleft_y
    boxbreite, boxhoehe = stundenplan_breite // (anzahl_spalten + 2), stundenplan_hoehe // (anzahl_zeilen + 1)

    topleft_x, topleft_y = plan_topleft_x + boxbreite, plan_topleft_y + boxhoehe

    padding_x, padding_y = boxbreite // 10, boxhoehe // 20
    boxinhaltbreite = boxbreite - 2 * padding_x
    boxinhalthoehe = boxhoehe - 2 * padding_y

    #font = ImageFont.truetype("../pixelperfect/Minimal5x7.ttf", size=32)
    inhaltfont = ImageFont.truetype("../PIL/DejaVuSans.ttf", size=11)
    titelfonr = ImageFont.truetype("../PIL/DejaVuSans.ttf", size=25)
    
    def minuten_von_uhrzeitstring(s):
        t = datetime.datetime.strptime(s, "%H:%M")
        return t.hour * 60 + t.minute

    def zeile_von_datetimeobjekt(t):
        minuten = t.hour * 60 + t.minute
        anfangszeiten = anfangszeiten_ksbg
        y = 0
        while minuten_von_uhrzeitstring(anfangszeiten[y]) < minuten:
            y += 1
        return y

    def bildkoordinate_von_spalte_zeile(x, y):
        return (topleft_x + x * boxbreite, topleft_y + y * boxhoehe)

    # https://levelup.gitconnected.com/how-to-properly-calculate-text-size-in-pil-images-17a2cc6f51fd
    def get_text_dimensions(text_string: str, font: ImageFont) -> list[int]:
        # https://stackoverflow.com/a/46220683/9263761
        ascent, descent = font.getmetrics()
        text_width = font.getmask(text_string).getbbox()[2]
        text_height = font.getmask(text_string).getbbox()[3] + descent
        return (text_width, text_height)

    def schreibe(x, y, s, align="topleft"):
        w, h = get_text_dimensions(s, inhaltfont)
        bx, by = bildkoordinate_von_spalte_zeile(x, y)
        if align == "topleft":
            vx, vy = 0, 0
        elif align == "topright":
            vx, vy = boxinhaltbreite - w, 0
        elif align == "bottomright":
            vx, vy = boxinhaltbreite - w, boxinhalthoehe - h
        elif align == "bottomleft":
            vx, vy = 0, boxinhalthoehe - h
        elif align == "center":
            vx, vy = (boxinhaltbreite - w) // 2, (boxinhalthoehe - h) // 2
        drawbw.text((bx + padding_x + vx, by + padding_y + vy), s, font = inhaltfont, fill="black")

    tree = etree.parse(f"roomdata/{zimmer}.xml")
    events = []
    for event in tree.findall(".//event"):
        events.append(Event(event))

    week = Week(events, date.today()+timedelta(days=7))

    bw = Image.new("1", (800,480), color=1)
    drawbw = ImageDraw.Draw(bw)

    rw = Image.new("1", (800,480), color=1)
    drawrw = ImageDraw.Draw(rw)


    for x in range(anzahl_spalten + 1):
        drawbw.line([bildkoordinate_von_spalte_zeile(x, 0), bildkoordinate_von_spalte_zeile(x, anzahl_zeilen)] , fill ="black", width = 2)

    for y in range(anzahl_zeilen + 1):
        drawbw.line([bildkoordinate_von_spalte_zeile(0, y), bildkoordinate_von_spalte_zeile(anzahl_spalten, y)] , fill ="black", width = 2)

    # Montag = 0
    wochentagnummer = datetime.date.today().weekday() 

    for x in range(anzahl_spalten):
        text = deutsch.wochentage[(x+wochentagnummer) % 7]
        schreibe(x, -1, text, align="center")

    # drawbw.multiline_text(bildkoordinate_von_spalte_zeile(-1, -1), text="Mo-Fr", font=font11, fill=0)
    schreibe(-1, -1, "Mo-Fr", align="center")

    # drawbw.multiline_text(bildkoordinate_von_spalte_zeile(anzahl_spalten, -1), text="Sa", font=font11, fill=0)
    schreibe(anzahl_spalten, -1, "Sa", align="center")

    for y, zeit in enumerate(anfangszeiten_ksbg):
        schreibe(-1, y, zeit, align="center")
        # drawbw.multiline_text(bildkoordinate_von_spalte_zeile(-1, y), text=zeit, font=font11, fill=0)

    for y, zeit in enumerate(anfangszeiten_isme):
        schreibe(anzahl_spalten, y, zeit, align="center")
        # drawbw.multiline_text(bildkoordinate_von_spalte_zeile(anzahl_spalten, y), text=zeit, font=font11, fill=0)

    for x, day in enumerate(week.days):
        maxy = -1000
        for event in day.events:
            text = f"{event.fachkuerzel} {event.klassekurz}"
            #w,h = get_text_dimensions(text, font) #drawbw.textsize(text, font=font)
            # drawbw.multiline_text((0, 0), text=text, font=font15, fill=0)
            level = 0
            # while True:
            #     text = deutsch.lehrerName(event.lehrername, level)
            #     w, h = get_text_dimensions(text,font11)
            #     # print(f"level [{level}] text {text}")
            #     if w < boxbreite:
            #         break
            #     level += 1
            y = zeile_von_datetimeobjekt(event.start_datetime.time())
            schreibe(x, y, event.fachkuerzel)
            schreibe(x, y, event.lehrerkuerzel, align = "topright")
            schreibe(x, y, event.klassekurz, align = "bottomleft")
            if y > maxy:
                maxy = y
        if maxy != -1000:
            # schreibe(x, y, "ROT", align = "center")
            bx, by = bildkoordinate_von_spalte_zeile(x, maxy)
            # drawrw.rectangle([(bx, by), (bx + boxbreite, by + boxhoehe)], fill ="black", outline ="white") 
            for j in range(by, by + boxhoehe):
                for i in range(bx, bx + boxbreite):
                    if (i + 5*j) % 8 == 0:
                        # drawrw.point(i, j)
                        # drawbw.point((i, j), fill="black")
                        drawrw.point((i, j), fill="black")



    kopfzeilenfont = titelfonr
    kopfzeile = f'{zimmer}, {besitzer}'

    w, h = get_text_dimensions(kopfzeile, kopfzeilenfont)
    drawbw.text((topleft_x, (topleft_y - boxhoehe - h) // 2), kopfzeile, font = kopfzeilenfont, fill="black")

    batteriestring = f'Batterie: {batteriestand * 100:.1f} %'
    w, h = get_text_dimensions(batteriestring, kopfzeilenfont)
    drawbw.text((topleft_x + 3 * boxbreite, (topleft_y - boxhoehe - h) // 2), batteriestring, font = kopfzeilenfont, fill="black")
    return bw, rw

bw, rw = erzeuge_stundenplan("A11", "Mister X", 0.5)

bw.save("bw.png", "PNG") 
rw.save("rw.png", "PNG") 

