from PIL import ImageFont, ImageDraw

class FontCollection:
    def __init__(self, size=0):
        self.small= ImageFont.truetype("DejaVuSans-Bold.ttf", size=9-size)
        self.normal = ImageFont.truetype("DejaVuSans-Bold.ttf", size=11+size)
        self.large = ImageFont.truetype("DejaVuSans.ttf", size=14+size)
        self.size = size



class TextLines:
    def __init__(self):
        self.lines = []
        self.boxes = []
        self.box = (0,0)

    def addLine(self, text:str, font:ImageFont):
        self.lines.append({"text":text, "font":font})
        self.boxes.append(get_text_dimensions(text,font))
        self.getBox()

    
    def getBox(self, sep=3) -> tuple[int,int]:
        self.box = (max([b[0] for b in self.boxes]),sum([b[1] for b in self.boxes])+(len(self.boxes)-1)*sep)
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

    def addRow(self, lines:TextLines, separator=5):
        self.rows.append(lines)
        self.separators.append(separator)

    def getBox(self):
        w = min([line.box[0] for line in self.rows])
        h = sum([line.box[1] for line in self.rows])+sum(self.separators[0:-1])
        return (w,h)

    def draw(self, x, y, bitmap):
        for i,row in enumerate(self.rows):
            row.draw(x,y,bitmap, self.separators[i])
            y += row.box[1]+self.separators[i]


def get_text_dimensions(text_string: str, font: ImageFont) -> list[int]:
    if (text_string==None or len(text_string)==0):
        return (0,0)
    # https://stackoverflow.com/a/46220683/9263761
    ascent, descent = font.getmetrics()
    text_width = font.getmask(text_string).getbbox()[2]
    text_height = font.getmask(text_string).getbbox()[3] + descent
    return (text_width, text_height)

