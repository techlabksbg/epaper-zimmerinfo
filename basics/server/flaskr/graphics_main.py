from graphics.planmaker import planmaker
import datetime

planmaker(xmldatei="static/rooms/1/data.xml", heute=datetime.date.today()-datetime.timedelta(days=0), zimmername="H21", zimmertitel="Markus Keller, Ivo Blöchliger", battery=0.7, outputdirAndPrefix="static/rooms/1/data")
