import re

ics = open("h21.ics", "r")
#for line in range(linenumber):     //When ics is properly imported.
while True:
    line = ics_data = ics.readline()
    summary = re.search("SUMMARY:(.*)", line)
    if summary != None:
        x = summary.string[8:].strip()
        print(x)
        if x == "Reserviert":
            print("Achtung x ist reserviert")