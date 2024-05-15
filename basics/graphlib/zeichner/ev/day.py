from datetime import date
from .event import Event
from . import deutsch

class Day:
    def __init__(self, date:date):
        self.events: list[Event] = []
        self.date:date = date

    def add(self, event:Event):
        if self.date != event.start_datetime.date():
            raise RuntimeError("Datum nicht gleich!")
        self.events.append(event)
        self.events.sort(key = lambda e : e.start_datetime)
        return self

    def ausgabe(self) -> None:
        print(deutsch.datum(self.date))
        print("="*30)
        for event in self.events:
            print(event)
        print("-"*20)
