from datetime import date, timedelta
from zeichner.xml2image import xml2image

xml2image("H21.xml", date.today()+timedelta(days=5), "H21", "Markus Keller und Ivo Blöchliger", 0.3)



