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
y = 10
for di, day in enumerate(week.days):  # di: Index, day
    for event in day.events:
        t = event.start_datetime.time()
        print(t)
        print(type(t))
        print(str(t))
        text = f"{event.fachkuerzel} {event.klassekurz}"
        print(type(event.fachkuerzel))
        print(type(event.klassekurz))
        print(text)
        print(type(event.lehrername))
        print(event.lehrername)
        print(type(event.lehrerkuerzel))
        print(event.lehrerkuerzel)