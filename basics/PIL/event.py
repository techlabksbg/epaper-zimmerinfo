from datetime import datetime
from typing import Self

class Event:
    def __init__(self, tree):
        start_date = tree.find(".//start_date").text
        self.start_datetime: datetime = datetime.strptime(start_date, '%Y-%m-%d %H:%M')
        end_date = tree.find(".//end_date").text
        self.end_datetime: datetime = datetime.strptime(end_date, '%Y-%m-%d %H:%M')
        self.text: str = tree.find('.//text').text
        self.color: str = tree.find('.//color').text
        self.klasse: str | None = tree.find('.//klasse').text
        if self.klasse:
            self.klassekurz: str = self.klasse.replace("*","")
        else:
            self.klassekurz = None
        self.fachkuerzel: str = tree.find('.//fachkuerzel').text
        self.lehrerkuerzelname: str | None = tree.find('.//lehrerkuerzelname').text
        if self.lehrerkuerzelname:
            self.lehrername = self.lehrerkuerzelname[0:self.lehrerkuerzelname.find("(")]
        else:
            self.lehrername = None
        self.lehrerkuerzel: str = tree.find('.//lehrerkuerzel').text
        self.reservator: str = tree.find('.//reservator').text

        if (self.start_datetime>self.end_datetime):
            raise RuntimeError("Ende vor Start...")

    def __str__(self) -> str:
        return f"{self.text}: {self.start_datetime} bis {self.end_datetime}"

    def __lt__(self, other:Self) -> bool:
        return self.end_datetime < other.end_datetime
    
    def __gt__(self, other:Self) -> bool:
        return other<self

    def overlap(self, other:Self) -> bool:
        return not (self<other or self>other)