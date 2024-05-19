from datetime import datetime
from PIL import ImageDraw

from .ev.day import Day
from .ev.week import Week
from .ev.event import Event
from .ev import deutsch
from . import layout
from . import zeiten

def draw(week: Week, heute, zimmertitel, zimmername, battery, bitmaps):

    fontSet = layout.FontCollection()

    def getEventType(event):
        return "ksbg"  # isme, reserved

    def makeTextKSBG(event: Event, compression) -> layout.TextLines:
        lines = layout.TextLines()
        lines.add(f"{event.fachkuerzel} {event.klassekurz}", fontSet.normalBold)
        if (compression<20):
            lines.add(deutsch.lehrerName(event.lehrername, compression), fontSet.normal)
        else:
            lines.add(f"{event.lehrerkuerzel}", fontSet.normal)
        return lines
        
        return 
    def makeTextISME(event: Event) -> layout.TextLines:
        return 
    def makeTextReserved(event: Event) -> layout.TextLines:
        return 

    def makeText(event:Event, compression:int) -> layout.TextLines:
        if getEventType(event)=="ksbg":
            return makeTextKSBG(event,compression)
        if getEventType(event)=="isme":
            return makeTextISME(event,compression)
        return makeTextReserved(event,compression)        

    def makeColumns(compressionLevelHeute:int, compressionLevelAndere:int)->list[layout.GridColumn]:
        columns :list[layout.GridColumn]= [layout.GridColumn() for i in range(6)]
        for day in week.days:
            compression = compressionLevelHeute if day.date==heute else compressionLevelAndere
            wday = day.date.weekday()
            if wday==6:
                continue
            head = layout.TextLines()
            if (len(day.events)==0):
                head.add(deutsch.wochentagDatumKurz(day.date), fontSet.normal)
            else:
                head.add(deutsch.wochentagDatum(day.date), fontSet.normalBold)
            columns[wday].add(head,0)
            for event in day.events:
                gridY = zeiten.getRasterPosition(event.start_datetime.time())+1
                text = makeText(event, compression)
                columns[wday].add(text, gridY)
        return columns

    def ksbgZeiten(bitmap) -> layout.Column:
        col = layout.Column()
        # Zimmername
        head = layout.TextLines()
        head.add(zimmername, fontSet.largeBold)
        col.add(head)
        # Zeiten
        for  i,lines in enumerate(zeiten.rasterTextKSBG()):
            tl = layout.TextLines()
            tl.add(lines[0], fontSet.normalBold)
            tl.add(lines[1], fontSet.small)
            tl.getBox(2)
            col.add(tl,3+zeiten.separatorenKSBG[i])
        col.draw(2,479-col.getBox()[1], bitmap) 
        return col

    def title():
        title = layout.TextLines()
        title.add(zimmertitel, fontSet.largeBold)
        return title
    
    def datum(bitmap):
        text = layout.TextLines()
        text.add(datetime.now().strftime("Generiert am %Y-%m-%d %H:%M:%S"), fontSet.small)
        text.draw(700-text.box[0],4, bitmap)

    def grid(bitmap, xc, yc):
        drawbw = ImageDraw.Draw(bitmap)
        for i,y in enumerate(yc):
            offset=0
            if (i>0):
                offset = zeiten.separatorenKSBG[i-1]
            for yy in range(y-offset,y+1):
                drawbw.line(((0,yy),(xc[-1],yy)),width=1,fill="black")
        for x in xc:
            drawbw.line(((x,yc[0]),(x,479)),width=1,fill="black")

    def redRect(a,b,x,y):
        drawbw = ImageDraw.Draw(bitmaps[1])
        drawbw.rectangle((a,b,x,y), fill="black")

    def redFill(a,b,xx,yy, fib1, fib2):
        drawbw = ImageDraw.Draw(bitmaps[1])
        for y in range(b+1,yy):
            for x in range(a+(y*fib1)%fib2, xx, fib2):
                drawbw.point((x,y),fill="black")

    resolution = bitmaps[0].size
    firstCol = ksbgZeiten(bitmaps[0])
    planStart = firstCol.getBox()[0]+3
    yc = firstCol.getYCoordinates(resolution[1]-3-firstCol.getBox()[1])
    columns = makeColumns(0,20)
    xc = layout.columnsSetXc(columns, planStart)
    layout.drawColumnSet(columns, xc, yc, bitmaps[0])
    grid(bitmap=bitmaps[0], xc=xc, yc=yc)
    title().draw(3,3,bitmaps[0])
    datum(bitmaps[0])
    redRect(xc[4],yc[4],xc[5],yc[5])
    redFill(xc[2],yc[4],xc[3],yc[5], 8,13)



