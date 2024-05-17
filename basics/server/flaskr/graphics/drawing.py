from .ev.day import Day
from .ev.week import Week
from .ev.event import Event
from . import layout
from . import zeiten

def draw(week: Week, heute, zimmertitel, zimmername, battery, bitmaps):

    fontSet = layout.FontCollection()

    def getEventType(event):
        return "ksbg"  # isme, reserved

    def computeSizeKSBG(event: Event) -> tuple[int,int]:
        lines = layout.TextLines()
        lines.addLine(f"{event.fachkuerzel} {event.klassekurz}", fontSet.normal)
        lines.addLine(f"{event.lehrerkuerzel}")
        return lines.getBox()
        
        return 
    def computeSizeISME(event: Event):
        return 
    def computeSizeReserved(event: Event):
        return 

    def computeSize(event:Event):
        if getEventType(event)=="ksbg":
            return computeSizeKSBG(event)
        if getEventType(event)=="isme":
            return computeSizeISME(event)
        return computeSizeReserved(event)        

    def computeSizes():
        for day in week.days:
            for event in day.events:
                computeSize(event)
                

    for  lines in zeiten.rasterTextKSBG():
        print(lines)

    resolution = bitmaps[0].size
