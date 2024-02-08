import re

ics = open("h21.ics", "r")
reservations = []
#for line in range(linenumber):     //When ics is properly imported.
for i in range(10000):
    line = ics_data = ics.readline()
    summary = re.search("SUMMARY:(.*)", line)
    if summary != None:
        x = summary.string[8:].strip()
        reservations.append(x)
print(reservations)
for event in reservations: #Reservationen müssen auf reguläre und ausserordentliche geprüft werden
    normal = re.search("(.*-.*-.*)", event)
    if normal != None:
        normal = normal.group(1)
    print(normal)
    if normal == None:
            print("Achtung x ist reserviert")
        