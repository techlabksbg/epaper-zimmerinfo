from PIL import Image, ImageFont, ImageDraw, ImageColor
from time import sleep
from operator import mul
from datetime import date
import os
from lxml import etree

from . import grid_draw as gr
from . import grid_data as gd
from . import initializer

from .ev.event import Event
from .ev.week import Week

# xmldatei: Pfad zur xml-Datei
# heute: Heutiges Datum, damit auch zu anderen Zeitpunkten Pläne gerendert werden könnten.
# zimmername, z.B. "H21"
# zimmertitel, z.B. "Dr. Hans-Wurst"
# battery: Zahl zwischen 0 und 1.
def xml2image(xmldatei, heute, zimmername, zimmertitel, battery, outputverzeichnis="."):

    if not os.path.exists(xmldatei):
        raise "Please give an existing file on the command line"
    #get the events from the file
    tree = etree.parse(xmldatei)
    events = []
    for event in tree.findall(".//event"):
        events.append(Event(event))

    week = Week(events, heute)

    print(f"heute={heute}")
    heute_wochentag = heute.weekday()

    #make image and grid
    print("initialise_image")
    bw = initializer.initialise_image_b()
    rw = initializer.initialise_image_r()
    print("gridDrawer")
    gr.grid_drawer(bw[0], heute_wochentag, zimmername, zimmertitel)
    print("battery_indicator")
    gd.battery_indicator(battery, bw[0], rw[0])

    #insert data into immage
    for di, day in enumerate(week.days):  # di: Index, day
        day.ausgabe()
        for event in day.events:
            start_time = str(event.start_datetime.time()) #Format "00:00:00"
            end_time = str(event.end_datetime.time())
            fachkuerzel = event.fachkuerzel 
            klasse = event.klassekurz
            lehrername = event.lehrername
            lehrerkuerzel = event.lehrerkuerzel
            wochentag = event.start_datetime.date().weekday() #0=Montag, 6=Sonntag
            event_datum = event.start_datetime.date() #Datum im format "YYYY-MM-DD"
            text = event.text

            reservator = event.reservator

            gd.draw_data(current_weekday = heute_wochentag, current_date = heute, event_date = event_datum, starttime = start_time, endtime = end_time, subject = fachkuerzel, Class = klasse, teacher = lehrername, aditional_info = "", time = start_time, subject_short = fachkuerzel, teacher_short = lehrerkuerzel, weekday = wochentag, reservator = None, drawbw=bw[0], font=ImageFont.truetype("DejaVuSans-Bold.ttf", size=11), bw = bw[1], text = text, drawrw = rw[0], rw = rw[1])



    bw[1].save(outputverzeichnis+"/bw.png", "PNG")
    