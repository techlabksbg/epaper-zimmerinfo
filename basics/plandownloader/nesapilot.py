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
        
        print(args)
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
        url = f"https://ksbg.nesa-sg.ch/dview/showzimmerplan.php?id=6zfgfbejsdtwgv3hcuwegujdbg&zimmer={room}"
        res = self.execCurl("generic.curl", [["MYURL", url]])
        url2 = "https://ksbg.nesa-sg.ch/scheduler_processor.php?view=week&curr_date=2025-02-21&min_date=2025-02-17&max_date=2025-02-24&nouser=1&id=&pageid=&ansicht=raummonitor&timeshift=-60"
        xmldata = self.execCurl("generic.curl",[["MYURL", url2]], False)
        # Save xml-Document
        datei = f"roomdata/{room}.xml"
        print(f"Saving xml-Data to file {datei}")
        with open(datei, "wb") as f:
            f.write( html.tostring(xmldata))

if __name__== "__main__":
    pilot = NesaPilot()
    for room in sys.argv[1:]:
        pilot.getRoom(room)