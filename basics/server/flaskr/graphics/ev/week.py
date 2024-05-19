from datetime import date, datetime, timedelta
from .day import Day
from .event import Event

class Week:
    def __init__(self, events:list, start_date:date):
        self.days: list = [Day(start_date + timedelta(days=i)) for i in range(7)]
        self.start_date: date = start_date
        self.make_days(events)

    def make_days(self, events: list) -> None:
        for event in events:
            e_date = event.start_datetime.date()
            index = (e_date - self.start_date).days
            if index>=0 and index<7:
                self.days[index].add(event)
            

    def ausgabe(self) -> None:
        print(f"Woche vom {self.start_date}")
        print("#"*30)
        for day in self.days:
            day.ausgabe()
