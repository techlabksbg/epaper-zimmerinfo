from lxml import html
import os

datei = "zimmerplan.html"

if not os.path.exists(datei):
    raise f"Datei {datei} nicht gefunden."

tree = html.parse(datei)

for a in tree.findall(".//nav/a"):

    d = a.find("./div")
    if d!=None:
        print(a.attrib['href'])
        print(d.text)
