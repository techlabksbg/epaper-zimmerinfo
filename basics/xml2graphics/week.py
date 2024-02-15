from datetime import date, datetime, timedelta
from day import Day
class Week:
    def __init__(self, events, start_date):
        self.days = [Day(start_date + timedelta(days=i)) for i in range(7)]
        self.start_date = start_date
        self.make_days(events)

    def make_days(self, events):
        for event in events:
            e_date = event.start_datetime.date()
            index = (e_date - self.start_date).days
            if index>=0 and index<7:
                self.days[index].add(event)
            

    def ausgabe(self):
        print(f"Woche vom {self.start_date}")
        print("#"*30)
        for day in self.days:
            day.ausgabe()
