from datetime import datetime
#from typing import Self

class Event:
    def __init__(self, tree, noneReplacer="n/a"):
        def noneRep(s:str)->str:
            if s==None:
                return noneReplacer
            return s
        start_date = tree.find(".//start_date").text
        self.start_datetime: datetime = datetime.strptime(start_date, '%Y-%m-%d %H:%M')
        end_date = tree.find(".//end_date").text
        self.end_datetime: datetime = datetime.strptime(end_date, '%Y-%m-%d %H:%M')
        self.text: str = tree.find('.//text').text
        self.kommentar: str = tree.find('.//kommentar').text
        self.anzeigestp: str = tree.find('.//anzeigestp').text
        self.mandantname: str = tree.find('.//mandantname').text
        self.color: str = tree.find('.//color').text
        self.klasse: str = tree.find('.//klasse').text
        if self.klasse:
            self.klassekurz: str = self.klasse.replace("*","")
        else:
            self.klassekurz = noneRep(None)
        self.fachkuerzel: str = noneRep(tree.find('.//fachkuerzel').text)
        self.kurskuerzel: str = noneRep(tree.find('.//kurskuerzel').text)
        self.lehrerkuerzelname: str | None = tree.find('.//lehrerkuerzelname').text
        if self.lehrerkuerzelname:
            self.lehrername = self.lehrerkuerzelname[0:self.lehrerkuerzelname.find("(")]
        else:
            self.lehrername = noneRep(None)
        self.lehrerkuerzel: str = noneRep(tree.find('.//lehrerkuerzel').text)
        self.reservator: str = noneRep(tree.find('.//reservator').text)
        self.reservation: str = noneRep(tree.find('.//reservation').text)
        self.istrv: str = noneRep(tree.find('.//istrv').text)

        if (self.start_datetime>self.end_datetime):
            raise RuntimeError("Ende vor Start...")

    def __str__(self) -> str:
        return f"{self.text}: {self.start_datetime} bis {self.end_datetime}"

    def __lt__(self, other) -> bool:
        return self.end_datetime < other.end_datetime
    
    def __gt__(self, other) -> bool:
        return other<self

    def overlap(self, other) -> bool:
        return not (self<other or self>other)