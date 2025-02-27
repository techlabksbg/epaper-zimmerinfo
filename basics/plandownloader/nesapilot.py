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
import sys

if not os.path.exists("mysecrets.py"):
    with open("mysecrets.py", "w") as f:
        f.write("raise RuntimeError('bitte diese Zeile in mysecrets.py löschen und Username und Passwort eintragen')\n#Auth for epaper server and url\nlogin_web='user'\npassword_web='pass'\nserver_url='http://127.0.0.1:5000/xml'\n")
    raise RuntimeError("Die Datei mysecrets.py wurde angelegt. Bitte bearbeiten Sie die Datei mysecrets.py.")

import mysecrets


class NesaPilot:
    def __init__(self):
        self.baseurl = "https://ksbg.nesa-sg.ch/"
        self.debug = False
        self.clearCookies()

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
        #if (hasattr(mysecrets,'curl')):
        #    print("Curl ist definiert")
        #    args[0] = mysecrets.curl
        if len(replacements)>0:
            args = [self.applyAllReplacements(a, replacements) for a in args]
        
        #print(args)
        # from https://stackoverflow.com/questions/4760215/running-shell-command-and-capturing-the-output
        result = subprocess.run(args, stdout=subprocess.PIPE)
        htmlcode = result.stdout.decode('utf-8')
        if self.debug:
            with open("execCurl.out", "w") as f:
                f.write(htmlcode)
        if isHTML:  # If its html
            tree = html.fromstring(htmlcode)  # Build an lxml-tree for easy access to element via XPath
        else: # if its proper xml
            tree = etree.fromstring(bytes(htmlcode, encoding='utf-8'))
        time.sleep(1) # 1 Sekunde schlafen, damit die Anfragen nicht zu schnell raus rausgehen...
        return tree



    def getRoom(self, room):
        # TODO Adust Dates...
        curr_date = date.today()
        min_date = curr_date + timedelta(days=-curr_date.weekday())
        max_date = min_date + timedelta(days=14)
        print(f"preparing link for min_date={min_date} to max_date={max_date}")
        r = [['"+view+"', "week"],
            ['"+curr_date+"', str(curr_date)],
            ['"+min_date+"', str(min_date)],
            ['"+max_date+"', str(max_date)]]

        print(r) 
        url = f"https://ksbg.nesa-sg.ch/dview/showzimmerplan.php?id=6zfgfbejsdtwgv3hcuwegujdbg&zimmer={room}"
        res = self.execCurl("generic.curl", [["MYURL", url]])
        url2 = f"https://ksbg.nesa-sg.ch/scheduler_processor.php?view=week&curr_date={curr_date}&min_date={min_date}&max_date={max_date}&nouser=1&id=&pageid=&ansicht=raummonitor&timeshift=-60"
        print(url2)
        xmldata = self.execCurl("generic.curl",[["MYURL", url2]], False)
        # Save xml-Document
        datei = f"roomdata/{room}.xml"
        print(f"Saving xml-Data to file {datei}")
        with open(datei, "wb") as f:
            f.write( html.tostring(xmldata))
        site = mysecrets.server_url
        auth=(mysecrets.login_web, mysecrets.password_web)
        requests.post(f"{site}?roomname={room}", files={'file': open(datei, 'r')}, auth=auth)


        


if __name__== "__main__":
    site = mysecrets.server_url
    auth=(mysecrets.login_web, mysecrets.password_web)
    response = requests.get(f"{site}", auth=auth)
    if (response.status_code!=200):
        print(f"Got http status code {response.status_code} from {site}")
        exit()
    roomnames = response.content.decode('utf8')
    roomnames = roomnames.split("\n")[:-1]
    print(f"Got he following roomnames: {roomnames}")
    if len(roomnames)==0:
        print("No rooms to fetch. Abort")
        exit()

    pilot = NesaPilot()
    for room in roomnames:
        pilot.getRoom(room)