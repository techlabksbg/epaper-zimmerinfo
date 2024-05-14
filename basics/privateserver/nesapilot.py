# See https://lxml.de/installation.html if it is not installed
from lxml import html, etree
import subprocess
import shlex
import os
import urllib.parse
import re
from datetime import date, timedelta
import time
import requests
import filecmp

if not os.path.exists("mysecrets.py"):
    with open("mysecrets.py", "w") as f:
        f.write("raise RuntimeError('bitte diese Zeile in mysecrets.py löschen und Username und Passwort eintragen')\n#Nesa login\nlogin='hans.wurst'\npasswort='123456'\n\n#curl='custompathtocurl'\n\n#Auth for epaper server and url\nlogin_web='user'\npassword_web='pass'\nserver_url='http://127.0.0.1:5000/'\n")
    raise RuntimeError("Die Datei mysecrets.py wurde angelegt. Bitte bearbeiten Sie die Datei mysecrets.py.")

import mysecrets

class NesaPilot:
    def __init__(self):
        self.lastpage = None
        self.baseurl = "https://ksbg.nesa-sg.ch/"
        self.nav = {}
        self.debug = False
        self.rooms = {}
        self.clearCookies()
        self.performLogin()
        if len(self.nav.keys())==0:
            raise "Keine Navigation gefunden, da ist wohl das Login fehlgeschlagen..."

    def __del__(self):  # Clean up
        self.clearCookies()

    def clearCookies(self):
        if os.path.exists("nesa-cookies.txt"):
            os.remove("nesa-cookies.txt")


    # replacements is of the form [["ALT", "neu"], ["uralt", "brandneu"]]
    def applyAllReplacements(self, s, repl):
        for r in repl:
            s = s.replace(r[0], r[1])
        return s

    # replacements is of the form [["ALT", "neu"], ["uralt", "brandneu"]]
    def execCurl(self, datei, replacements=[], isHTML = True):
        with open(datei, "r") as f:
            args = [a for a in shlex.split(f.read()) if a!="\n"]  # Split file into arguments like the shell would (well, except for escaped new lines, it seems)
        
        cookieHandling = shlex.split("-L -b nesa-cookies.txt -c nesa-cookies.txt")
        args = args[0:1] + cookieHandling + args[1:]
        if (hasattr(mysecrets,'curl')):
            print("Curl ist definiert")
            args[0] = mysecrets.curl
        if len(replacements)>0:
            args = [self.applyAllReplacements(a, replacements) for a in args]
        
        # from https://stackoverflow.com/questions/4760215/running-shell-command-and-capturing-the-output
        result = subprocess.run(args, stdout=subprocess.PIPE)
        htmlcode = result.stdout.decode('utf-8')
        if self.debug:
            with open("execCurl.out", "w") as f:
                f.write(htmlcode)
        if isHTML:  # If its html
            tree = html.fromstring(htmlcode)  # Build an lxml-tree for easy access to element via XPath
            self.lastpage = tree
            self.getNavMenu()
        else: # if its proper xml
            tree = etree.fromstring(bytes(htmlcode, encoding='utf-8'))
        time.sleep(1) # 1 Sekunde schlafen, damit die Anfragen nicht zu schnell raus rausgehen...
        return tree


    def getStartSeite(self):
        self.clearCookies()
        print("--> Startseite laden... <--")
        return self.execCurl("startseite.curl")

    def performLogin(self):
        t = self.getStartSeite() 
        print("--> Perform login... <--")
        # input Element mit Attribut name, das gleich loginhash ist. Davon gerne das Attribut value
        loginhash = t.find(".//input[@name='loginhash']").value
        r = [["LOGIN", urllib.parse.quote_plus(mysecrets.login)],
            ["PASSWORT", urllib.parse.quote_plus(mysecrets.passwort)],
            ['L0G1NHASH', urllib.parse.quote_plus(loginhash)]]
        return self.execCurl("login.curl", r)

    def getNavMenu(self):
        self.nav = {}
        if self.lastpage == None:
            return self.nav
        for a in self.lastpage.findall(".//nav/a"):
            d = a.find("./div")
            if d!=None:
                self.nav[d.text] = self.baseurl+a.attrib['href']
            else:
                if a.text!=None and len(a.text)>0:
                    self.nav[a.text] = self.baseurl+a.attrib['href']
        return self.nav

    def getRoomDict(self):
        sel = self.lastpage.find(".//select[@id='listindex_s']")
        self.rooms = {}
        for o in sel.findall(".//option"):
            self.rooms[o.text] = o.attrib['value']
        return self.rooms


    def getRoomAjaxLink(self, numdays=7):
        source = html.tostring(self.lastpage).decode("utf-8")
        # js-Code in the form let url = "scheduler_processor.php?view="+view+"&curr_date="+curr_date+"&min_date="+min_date+"&max_date="+max_date+"&ansicht=raumansicht&id=abece56196bce8a8&transid=e7aa0e&pageid=22204";
        paramurl = re.search("let url = \"(scheduler_processor.php\?view=.*)\";", source).group(1)
        curr_date = date.today()
        min_date = curr_date - timedelta(days=curr_date.weekday())
        max_date = min_date + timedelta(days=numdays-1)

        r = [['"+view+"', "week"],
            ['"+curr_date+"', str(curr_date)],
            ['"+min_date+"', str(min_date)],
            ['"+max_date+"', str(max_date)]]
        paramurl = self.baseurl + self.applyAllReplacements(paramurl, r)
        return paramurl
                

    def getRooms(self, roomlist, numDays=7):
        update_rooms = []
        if not os.path.exists("roomdata"):
            os.mkdir("roomdata")
        print("--> Dem Link «Agenda» folgen... <--")
        self.execCurl("generic.curl", [["MYURL",self.nav['Agenda']]])
        print("--> Dem Link «Raumpläne» folgen... <--")
        self.execCurl("generic.curl", [["MYURL",self.nav['Raumpläne']]])
        self.getRoomDict()  # Get List of all available room (and corresponding indices)
        print(f"--> Liste der Räume: {self.rooms} <--")
        for room in roomlist:
            if not room in self.rooms:  # Does this room even exist?
                print(f"Raum {room} ist nicht in der Liste der Räume. Vorhandene Räume:\n{self.rooms.keys()}")
                continue
            # Load room page
            print(f"--> Seite für den Raum {room} laden... <--")
            self.execCurl("generic.curl", [["MYURL",self.nav['Raumpläne']+f"&listindex_s={self.rooms[room]}&subFilter="]])
            # Extract Ajax Link for this room
            ajaxURL = self.getRoomAjaxLink(numDays)
            # Make Ajax Request
            print(f"--> XML-Daten für Raum {room} laden... <--")
            xml = self.execCurl("generic.curl", [["MYURL",ajaxURL]], False)
            # Save xml-Document
            new_datei = f"roomdata/{room}_new.xml"
            datei = f"roomdata/{room}.xml"
            with open(new_datei, "wb") as f:
                f.write(html.tostring(xml))
            # overwrite room.xml if they differ
            if not os.path.isfile(datei) or not filecmp.cmp(new_datei, datei):
                with open(datei, "wb") as f:
                    f.write(html.tostring(xml))
                update_rooms.append(room)
                print(f"--> Saved plan to {datei} 3 Sekunden warten... <--")
            else:
                print(f"--> {datei} hat sich nicht geändert. 3 Sekunden warten... <--")
            os.remove(new_datei)
            time.sleep(3)
        return update_rooms


if __name__== "__main__":
    site = mysecrets.server_url
    auth=(mysecrets.login_web, mysecrets.password_web)

    pilot = NesaPilot()
    roomnames = requests.get(f"{site}", auth=auth).content.decode('utf8')
    roomnames = roomnames.split("\n")[:-1]
    roomnames = pilot.getRooms(roomnames, 45)

    # post request with all xml files
    for room in roomnames:
        datei = f"roomdata/{room}.xml"
        requests.post(f"{site}?roomname={room}", files={'file': open(datei, 'r')}, auth=auth)