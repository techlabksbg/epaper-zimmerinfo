from lxml import etree
from event import Event

tree = etree.parse("H21.xml")

events = []
for event in tree.findall(".//event"):
    events.append(Event(event))
    
events.sort(key= lambda e : e.start_datetime)
print([str(e) for e in events])
