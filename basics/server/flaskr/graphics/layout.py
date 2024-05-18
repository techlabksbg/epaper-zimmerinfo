from PIL import ImageFont, ImageDraw

class FontCollection:
    def __init__(self, size=0):
        self.small= ImageFont.truetype("DejaVuSans.ttf", size=9+size)
        self.normalBold = ImageFont.truetype("DejaVuSans-Bold.ttf", size=11+size)
        self.normal = ImageFont.truetype("DejaVuSans.ttf", size=11+size)
        self.largeBold = ImageFont.truetype("DejaVuSans-Bold.ttf", size=14+size)
        self.size = size



class TextLines:
    def __init__(self):
        self.lines = []
        self.boxes = []
        self.box = (0,0)

    def add(self, text:str, font:ImageFont):
        self.lines.append({"text":text, "font":font})
        self.boxes.append(get_text_dimensions(text,font))
        self.getBox()

    
    def getBox(self, sep=3) -> tuple[int,int]:
        self.box = (max([b[0] for b in self.boxes]),sum([b[1] for b in self.boxes])+len(self.boxes)*sep)
        return self.box

    def draw(self, x, y, bitmap, sep=3):
        drawbw = ImageDraw.Draw(bitmap)
        for i,line in enumerate(self.lines):
            drawbw.multiline_text((x,y), line['text'], font=line['font'], fill="black")
            print(f"draw at {x},{y} string ->{line['text']}<-")
            y+=self.boxes[i][1]+sep

class Column:
    def __init__(self):
        self.rows:list[TextLines] = []
        self.separators:list[int] = []
        self.gridY= []

    def add(self, lines:TextLines, separator=5):
        self.rows.append(lines)
        self.separators.append(separator)

    def getBox(self):
        w = max([line.box[0] for line in self.rows])
        h = sum([line.box[1] for line in self.rows])+sum(self.separators[0:-1])
        return (w,h)

    def getYCoordinates(self, y):
        yc = [y]
        for i,row in enumerate(self.rows):
            yc.append(yc[-1]+row.box[1]+self.separators[i])
        return yc

    def draw(self, x, y, bitmap):
        yc = self.getYCoordinates(y)
        for i,row in enumerate(self.rows):
            row.draw(x,yc[i],bitmap, self.separators[i])


class GridColumn:
    def __init__(self):
        self.rows:list[TextLines] = []
        self.gridY:list[float] = []

    def add(self, lines:TextLines, gridY:float):
        self.rows.append(lines)
        self.gridY.append(gridY)

    def draw(self,x, yc, bitmap):
        for i,row in enumerate(self.rows):
            yindex = int(self.gridY[i])
            if yindex>=len(yc):
                continue
            print(f"len(yc)={len(yc)}, self.gridY[i]={yindex}")
            y = yc[yindex]
            if yindex!=self.gridY[i]:
                ny = yc[yindex+1] if yindex+1<len(yc) else 2*yc[-1]-yc[-2]
                y = int(y+(ny-yc[yindex])*(self.gridY[i]-yindex))
            row.draw(x,y, bitmap)

    def getWidth(self):
        return max([line.box[0] for line in self.rows])

def columnsSetXc(columns: list[GridColumn], x:int=0, sep:int=3)->list[int]:
    xc=[x]
    for j, col in enumerate(columns):
        xc.append(xc[-1]+col.getWidth()+sep)
    return xc

def drawColumnSet(columns: list[GridColumn], xc, yc, bitmap, sep=3):
    for j, col in enumerate(columns):
        col.draw(xc[j],yc,bitmap)

def get_text_dimensions(text_string: str, font: ImageFont) -> list[int]:
    if (text_string==None or len(text_string)==0):
        return (0,0)
    # https://stackoverflow.com/a/46220683/9263761
    ascent, descent = font.getmetrics()
    text_width = font.getmask(text_string).getbbox()[2]
    text_height = font.getmask(text_string).getbbox()[3] + descent
    return (text_width, text_height)

