import icalendar
from datetime import datetime

filepath = "h21.ics"

with open(filepath, "rb") as file:
    calendar = file.read()


timetable = icalendar.Calendar.from_ical(calendar)
print (timetable)