from lxml import html
import os

datei = "zimmerplan.html"

if not os.path.exists(datei):
    raise f"Datei {datei} nicht gefunden."

tree = html.parse(datei)
# Eintrag:
# /html/body/div[4]/div/main/div/div/main/div/div[4]/div[5]/div[1]/div[1]
# //*[@id="scheduler"]/div[5]

cal = tree.find(".//*[@class='dhx_cal_data']")
for day in cal.findall(".//*[@data-column-index]"):
    datum = day.attrib['aria-label']
    print(datum)
    for event in day.findall(".//*[@event_id]"):
        d = event.find(".//div[@class='stpt_event_title']")
        print(datum)
        print(d.attrib['title'])

