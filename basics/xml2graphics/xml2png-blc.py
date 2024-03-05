from lxml import etree
from event import Event
from week import Week
from day import Day
from datetime import date
import deutsch

from PIL import Image, ImageFont, ImageDraw, ImageColor

# https://levelup.gitconnected.com/how-to-properly-calculate-text-size-in-pil-images-17a2cc6f51fd
def get_text_dimensions(text_string: str, font: ImageFont) -> list[int]:
    # https://stackoverflow.com/a/46220683/9263761
    ascent, descent = font.getmetrics()

    text_width = font.getmask(text_string).getbbox()[2]
    text_height = font.getmask(text_string).getbbox()[3] + descent

    return (text_width, text_height)


tree = etree.parse("H21.xml")

events = []
for event in tree.findall(".//event"):
    events.append(Event(event))
    

week = Week(events, date.today())
#img = Image.new("RGB", (800,480), color=(255,255,255))
bw = Image.new("1", (800,480), color=1)

#font = ImageFont.truetype("../pixelperfect/Minimal5x7.ttf", size=32)
drawbw = ImageDraw.Draw(bw)
y = 10
font11 = ImageFont.truetype("../PIL/DejaVuSans.ttf", size=11)
font15 = ImageFont.truetype("../PIL/DejaVuSans.ttf", size=15)
for di, day in enumerate(week.days):  # di: Index, day
    for event in day.events:
        width = 80
        t = event.start_datetime.time()
        minutes = t.hour*60+t.minute - 7*60-40
        topleft = (di*width,minutes/700*480)
        tl2 = (topleft[0], topleft[1]+15)
        text = f"{event.fachkuerzel} {event.klassekurz}"
        #w,h = get_text_dimensions(text, font) #drawbw.textsize(text, font=font)
        drawbw.multiline_text(topleft, text=text, font=font15, fill=0)
        level = 0
        while True:
            text = deutsch.lehrerName(event.lehrername, level)
            w,h = get_text_dimensions(text,font11)
            print(f"level [{level}] text {text}")
            if w<width:
                break
            level+=1
        drawbw.multiline_text(tl2, text=text, font=font11, fill=0)

bw.save("bw.png", "PNG") 

