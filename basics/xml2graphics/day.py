import deutsch

class Day:
    def __init__(self, date):
        self.events = []
        self.date = date

    def add(self, event):
        if self.date != event.start_datetime.date():
            raise RuntimeError("Datum nicht gleich!")
        self.events.append(event)
        self.events.sort(key = lambda e : e.start_datetime)

    def ausgabe(self):
        print(deutsch.datum(self.date))
        print("="*30)
        for event in self.events:
            print(event)
        print("-"*20)