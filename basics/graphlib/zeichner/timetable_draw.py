from PIL import Image, ImageFont, ImageDraw, ImageColor
from time import sleep
from operator import mul
try:
    from . import grid_draw as gr
    from . import grid_data as gd
except ImportError:
    import grid_draw as gr
    import grid_data as gd

from lxml import etree
from event import Event
from week import Week
from day import Day
from datetime import date
import sys,os
import initializer
import deutsch


if len(sys.argv)<2 or not os.path.exists(sys.argv[1]):
    raise "Please give an existing file on the command line"
#get the events from the file
tree = etree.parse(sys.argv[1])
events = []
for event in tree.findall(".//event"):
    events.append(Event(event))

week = Week(events, date.today())

heute_datum = date.today() #Datum im format "YYYY-MM-DD"
print(heute_datum)
heute_wochentag = date.today().weekday()

#make image and grid
bw = initializer.initialise_image_b()
rw = initializer.initialise_image_r()
gr.grid_drawer(bw[0], heute_wochentag, "H21", "Ivo Bloeschlinger")
gd.battery_indicator(0.3, bw[0], rw[0])
#bw[1].save("bw.png", "PNG")
#bw[1].show()

#insert data into immage
for di, day in enumerate(week.days):  # di: Index, day
    day.ausgabe()
    for event in day.events:
        start_time = str(event.start_datetime.time()) #Format "00:00:00"
        #print(start_time)
        end_time = str(event.end_datetime.time())
        fachkuerzel = event.fachkuerzel 
        klasse = event.klassekurz
        #print(fachkuerzel)
        #print(klasse)
        lehrername = event.lehrername
        lehrerkuerzel = event.lehrerkuerzel
        #print(lehrername)
        #print(lehrerkuerzel)
        wochentag = event.start_datetime.date().weekday() #0=Montag, 6=Sonntag
        #print(wochentag)
        event_datum = event.start_datetime.date() #Datum im format "YYYY-MM-DD"
        #print(event_datum)
        text = event.text
        #print(text)
        #print(type(text))

        reservator = event.reservator
        #print(reservator)

        gd.draw_data(current_weekday = heute_wochentag, current_date = heute_datum, event_date = event_datum, starttime = start_time, endtime = end_time, subject = fachkuerzel, Class = klasse, teacher = lehrername, aditional_info = "", time = start_time, subject_short = fachkuerzel, teacher_short = lehrerkuerzel, weekday = wochentag, reservator = None, drawbw=bw[0], font=ImageFont.truetype("DejaVuSans-Bold.ttf", size=11), bw = bw[1], text = text, drawrw = rw[0], rw = rw[1])
        # bw[1].show()



bw[1].save("bw.png", "PNG")
#bw[1].show()