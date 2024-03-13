from lxml import etree
from event import Event
from week import Week
from day import Day
from datetime import date
import deutsch

tree = etree.parse("H21.xml")
events = []
for event in tree.findall(".//event"):
    events.append(Event(event))

week = Week(events, date.today())

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