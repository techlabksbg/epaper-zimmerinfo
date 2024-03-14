from lxml import etree
from event import Event
from week import Week
from datetime import date
tree = etree.parse("H21.xml")

events = []
for event in tree.findall(".//event"):
    events.append(Event(event))
    

week = Week(events, date.today())

week.ausgabe()