import subprocess
# See https://lxml.de/installation.html if it is not installed
from lxml import html, etree
import shlex
import mysecrets
import os
import urllib.parse
import re


baseurl = "https://ksbg.nesa-sg.ch/"

def clearCookies():
    if os.path.exists("nesa-cookies.txt"):
        os.remove("nesa-cookies.txt")


# replacements is of the form [["ALT", "neu"], ["uralt", "brandneu"]]
def applyAllReplacements(s, repl):
    for r in repl:
        s = s.replace(r[0], r[1])
    return s

# replacements is of the form [["ALT", "neu"], ["uralt", "brandneu"]]
def execCurl(datei, replacements=[], isHTML = True):
    with open(datei, "r") as f:
        args = [a for a in shlex.split(f.read()) if a!="\n"]  # Split file into arguments like the shell would (well, except for escaped new lines, it seems)
    
    cookieHandling = shlex.split("-L -b nesa-cookies.txt -c nesa-cookies.txt")
    args = args[0:1] + cookieHandling + args[1:]
    if len(replacements)>0:
        args = [applyAllReplacements(a, replacements) for a in args]
    
    # from https://stackoverflow.com/questions/4760215/running-shell-command-and-capturing-the-output
    result = subprocess.run(args, stdout=subprocess.PIPE)
    htmlcode = result.stdout.decode('utf-8')
    with open("execCurl.out", "w") as f:
        f.write(htmlcode)
    if isHTML:  # If its html
        tree = html.fromstring(htmlcode)  # Build an lxml-tree for easy access to element via XPath
    else: # if its proper xml
        tree = etree.fromstring(bytes(htmlcode, encoding='utf-8'))
    return tree


def getStartSeite():
    clearCookies()
    return execCurl("startseite.curl")

def performLogin():
    t = getStartSeite()    
    # input Element mit Attribut name, das gleich loginhash ist. Davon gerne das Attribut value
    loginhash = t.find(".//input[@name='loginhash']").value
    r = [["LOGIN", urllib.parse.quote_plus(mysecrets.login)],
         ["PASSWORT", urllib.parse.quote_plus(mysecrets.passwort)],
         ['L0G1NHASH', urllib.parse.quote_plus(loginhash)]]
    return execCurl("login.curl", r)

def getNavMenu(tree):
    nav = {}
    for a in tree.findall(".//nav/a"):
        d = a.find("./div")
        if d!=None:
            nav[d.text] = baseurl+a.attrib['href']
        else:
            if a.text!=None and len(a.text)>0:
                nav[a.text] = baseurl+a.attrib['href']
    return nav

def getRooms(tree):
    sel = tree.find(".//select[@id='listindex_s']")
    rooms = {}
    for o in sel.findall(".//option"):
        rooms[o.text] = o.attrib['value']
    return rooms


tempfile = "temp.html"

if not os.path.exists(tempfile):
    menu = getNavMenu(performLogin())
    if not "Agenda" in menu:
        raise "Da ist etwas schief gelaufen, Keinen Link auf Agenda gefunden..."

    agenda = execCurl("generic.curl", [["MYURL",menu['Agenda']]])
    menu = getNavMenu(agenda)                  
    raumplan = execCurl("generic.curl", [["MYURL",menu['Raumpläne']]])

    menu = getNavMenu(raumplan)
    rooms = getRooms(raumplan)
    h21 = rooms['H21']
    
    h21plan = execCurl("generic.curl", [["MYURL",menu['Raumpläne']+f"&listindex_s={h21}&subFilter="]])

    with open(tempfile, "wb") as f:
        f.write(html.tostring(h21plan))

else:
    h21plan = html.parse(tempfile)


source = html.tostring(h21plan).decode("utf-8")
# js-Code in the form let url = "scheduler_processor.php?view="+view+"&curr_date="+curr_date+"&min_date="+min_date+"&max_date="+max_date+"&ansicht=raumansicht&id=abece56196bce8a8&transid=e7aa0e&pageid=22204";

paramurl = re.search("let url = \"(scheduler_processor.php\?view=.*)\";", source).group(1)
print(paramurl)

r = [['"+view+"', "week"],
     ['"+curr_date+"', "2024-02-08"],
     ['"+curr_date+"', "2024-02-08"],
     ['"+min_date+"', "2024-02-05"],
     ['"+max_date+"', "2024-02-22"]]

paramurl = baseurl + applyAllReplacements(paramurl, r)
print(paramurl)

xmlplan = execCurl("generic.curl", [["MYURL",paramurl]], False)
with open("h21.xml", "wb") as f:
    f.write(html.tostring(xmlplan))
