import icalendar
from datetime import datetime

filepath = "h21.ics"

with open(filepath, "rb") as file:
    calendar = file.read().decode('utf-8')


# timetable = icalendar.Calendar.from_ical(calendar)
# print (timetable)

event = icalendar.Calendar.from_ical(calendar)
for event in event.walk():
    name = event.get('SUMMARY')
    start_data = event.get('DTSTART')
    end_date = event.get('DTEND')
    print ("Name:", name, "| Start Date:", start_data, "| End Date:", end_date)
# start_date = event.get('DTSTART').date()
# end_date = event.get('DTEND').dt.date()

