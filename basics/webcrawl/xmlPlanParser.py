from lxml import etree
from event import Event

tree = etree.parse("roomdata/D15.xml")

events = []
for event in tree.findall(".//event"):
    events.append(Event(event))
    
#    for entry in event.findall(".//*"):
#        if (entry.text):
#            print(f"{entry.tag} -> {entry.text}")
#    print("-----------------------------")