from lxml import html
import os

datei = "zimmerplan.html"

if not os.path.exists(datei):
    raise f"Datei {datei} nicht gefunden."

tree = html.parse(datei)
# Eintrag:
# /html/body/div[4]/div/main/div/div/main/div/div[4]/div[5]/div[1]/div[1]
# //*[@id="scheduler"]/div[5]
for a in tree.findall(".//*[@event_id]"):
    print(a)
    d = a.find(".//div[@class='stpt_event_title']")
    print(d.attrib['title'])
