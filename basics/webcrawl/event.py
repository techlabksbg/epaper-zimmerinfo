from datetime import datetime
class Event:
    def __init__(self, tree):
        start_date = tree.find(".//start_date").text
        self.start_datetime = datetime.strptime(start_date, '%Y-%m-%d %H:%M')
        print(self.start_datetime)