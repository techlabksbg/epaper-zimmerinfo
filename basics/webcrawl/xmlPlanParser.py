from lxml import html, etree

tree = etree.parse("roomdata/D15.xml")

for event in tree.findall(".//event"):
    for entry in event.findall(".//*"):
        if (entry.text):
            print(f"{entry.tag} -> {entry.text}")
    print("-----------------------------")