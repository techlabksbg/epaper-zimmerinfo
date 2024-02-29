from datetime import datetime
class Event:
    def __init__(self, tree):
        start_date = tree.find(".//start_date").text
        self.start_datetime = datetime.strptime(start_date, '%Y-%m-%d %H:%M')
        end_date = tree.find(".//end_date").text
        self.end_datetime = datetime.strptime(end_date, '%Y-%m-%d %H:%M')
        self.text = tree.find('.//text').text
        self.color = tree.find('.//color').text
        self.klasse = tree.find('.//klasse').text
        if self.klasse:
            self.klassekurz = self.klasse.replace("*","")
        self.fachkuerzel = tree.find('.//fachkuerzel').text
        self.lehrerkuerzelname = tree.find('.//lehrerkuerzelname').text
        if self.lehrerkuerzelname:
            self.lehrername = self.lehrerkuerzelname[0:self.lehrerkuerzelname.find("(")]
        self.lehrerkuerzel = tree.find('.//lehrerkuerzel').text
        self.reservator = tree.find('.//reservator').text

        if (self.start_datetime>self.end_datetime):
            raise RuntimeError("Ende vor Start...")

    def __str__(self):
        return f"{self.text}: {self.start_datetime} bis {self.end_datetime}"

    def __lt__(self, other):
        return self.end_datetime < other.end_datetime
    
    def __gt__(self, other):
        return other<self

    def overlap(self, other):
        return not (self<other or self>other)