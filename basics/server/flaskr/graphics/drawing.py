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
                
    def ksbgZeiten(bitmap):
        col = layout.Column()
        for  i,lines in enumerate(zeiten.rasterTextKSBG()):
            tl = layout.TextLines()
            for line in lines:
                tl.addLine(line, fontSet.normal)
            tl.getBox(2)
            col.addRow(tl,3+zeiten.separatorenKSBG[i])
        col.draw(2,479-col.getBox()[1], bitmap) 


    ksbgZeiten(bitmaps[0])

