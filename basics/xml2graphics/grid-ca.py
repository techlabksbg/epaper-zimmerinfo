from PIL import Image

# Erstelle ein weißes Bild mit 100x100 Pixeln
image = Image.new("RGB", (100, 100), "white")

# Setze einen roten Pixel in der Mitte des Bildes
image.putpixel((50, 50), (255, 0, 0))

# Zeige das Bild an
image.show()

# Speichere das Bild
image.save("pixelart.png")

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

(0 y) , (800 y)