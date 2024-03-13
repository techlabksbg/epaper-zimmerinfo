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



def initialize_image():
    bw = Image.new("1", (800,480), color=1)
    drawbw = ImageDraw.Draw(bw)
    gd.grid_drawer(drawbw)
    return bw

#get the events from the file
tree = etree.parse("H21.xml")
events = []
for event in tree.findall(".//event"):
    events.append(Event(event))

week = Week(events, date.today())

#make image and grid
bw = initializer.initialise_immage()
gr.grid_drawer(bw[0], 5)
bw[1].save("bw.png", "PNG")
bw[1].show()

#insert data into immage
for di, day in enumerate(week.days):  # di: Index, day
    for event in day.events:
        time = str(event.start_datetime.time()) #Format "00:00:00"
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

        heute_datum = date.today() #Datum im format "YYYY-MM-DD"
        print(heute_datum)
        heute_wochentag = date.today().weekday()

