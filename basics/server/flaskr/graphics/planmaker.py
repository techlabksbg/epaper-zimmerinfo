import sys
from lxml import etree

from .ev.event import Event
from .ev.week import Week
from . import imageConversion
from . import drawing

from PIL import ImageDraw

def planmaker(xmldatei, heute, zimmertitel, zimmername, battery, outputdirAndPrefix):
    def loadData(xmldatei, heute):
        tree = etree.parse(xmldatei)
        events = []
        for event in tree.findall(".//event"):
            events.append(Event(event))
        return Week(events, heute)
       
    resolution = (800,480)
    week = loadData(xmldatei=xmldatei, heute=heute)
    bitmaps = [imageConversion.newBWimage(size=resolution) for i in range(2)]

    drawing.draw(week, heute, zimmertitel, zimmername, battery, bitmaps)
    
    with open(outputdirAndPrefix+".bin", "wb") as f:
        b = imageConversion.bw_rw2bin(bitmaps[0], bitmaps[1], resolution)
        res=0
        for c in b:
            f.write(bytes(chr(c)))
            res+=1
        print(f"planmaker:: I have {len(b)} bytes to write... into {outputdirAndPrefix}.bin  ->res={res}", file=sys.stderr)
        f.close()

    imageConversion.bw_rw2rgb(bitmaps[0], bitmaps[1], resolution).save(outputdirAndPrefix+".png")
