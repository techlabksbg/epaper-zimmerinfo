from datetime import date, datetime, timedelta
from .event import Event
from . import deutsch

class Day:
    def __init__(self, date:date):
        self.events = []
        self.date:date = date

    def add(self, event:Event):
        if self.date != event.start_datetime.date():
            raise RuntimeError("Datum nicht gleich!")
        self.events.append(event)
        self.events.sort(key = lambda e : e.start_datetime)
        return self

    def firstAndLastStart(self) -> tuple:
        start = min([e.start_datetime for e in self.events])
        laststart = max([e.start_datetime for e in self.events])
        return start, laststart

    def ausgabe(self) -> None:
        print(deutsch.datum(self.date))
        print("="*30)
        for event in self.events:
            print(event)
        print("-"*20)
