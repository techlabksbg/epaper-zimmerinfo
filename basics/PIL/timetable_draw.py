from PIL import Image, ImageFont, ImageDraw, ImageColor
from time import sleep
from operator import mul
import grid_draw as gr
import grid_data as gd
from lxml import etree
from event import Event
from week import Week
from day import Day
from datetime import date
import initializer
import deutsch


#get the events from the file
tree = etree.parse("H21.xml")
events = []
for event in tree.findall(".//event"):
    events.append(Event(event))

week = Week(events, date.today())

#make image and grid
bw = initializer.initialise_immage()
gr.grid_drawer(bw[0], 5, "h21", "Ivo Bloeschlinger")
gd.head_draw(bw[0], "H21", "Ivo Bloeschinger")
gd.battery_indicator(0.3, bw[0])
bw[1].save("bw.png", "PNG")
bw[1].show()

#insert data into immage
for di, day in enumerate(week.days):  # di: Index, day
    for event in day.events:
        start_time = str(event.start_datetime.time()) #Format "00:00:00"
        print(start_time)
        end_time = str(event.end_datetime.time())
        fachkuerzel = event.fachkuerzel 
        klasse = event.klassekurz
        print(fachkuerzel)
        print(klasse)
        lehrername = event.lehrername
        lehrerkuerzel = event.lehrerkuerzel
        print(lehrername)
        print(lehrerkuerzel)
        wochentag = event.start_datetime.date().weekday() #0=Montag, 6=Sonntag
        print(wochentag)
        event_datum = event.start_datetime.date() #Datum im format "YYYY-MM-DD"
        print(event_datum)

        heute_datum = date.today() #Datum im format "YYYY-MM-DD"
        print(heute_datum)
        heute_wochentag = date.today().weekday()
        reservator = event.reservator
        print(reservator)

        gd.draw_data(current_weekday = heute_wochentag, current_date = heute_datum, event_date = event_datum, starttime = start_time, endtime = end_time, subject = fachkuerzel, Class = klasse, teacher = lehrername, aditional_info = "", time = start_time, subject_short = fachkuerzel, teacher_short = lehrerkuerzel, weekday = wochentag, reservator = None, drawbw=bw[0], font=ImageFont.truetype("DejaVuSans-Bold.ttf", size=11))


