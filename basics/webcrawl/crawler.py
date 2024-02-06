import subprocess
# See https://lxml.de/installation.html if it is not installed
from lxml import html
import shlex
import mysecrets
import os
import urllib.parse

def clearCookies():
    if os.path.exists("nesa-cookies.txt"):
        os.remove("nesa-cookies.txt")


# replacements is of the form [["ALT", "neu"], ["uralt", "brandneu"]]
def applyAllReplacements(s, repl):
    for r in repl:
        s = s.replace(r[0], r[1])
    return s

# replacements is of the form [["ALT", "neu"], ["uralt", "brandneu"]]
def execCurl(datei, replacements=[]):
    with open(datei, "r") as f:
        args = [a for a in shlex.split(f.read()) if a!="\n"]  # Split file into arguments like the shell would (well, except for escaped new lines, it seems)
    
    cookieHandling = shlex.split("-L -b nesa-cookies.txt -c nesa-cookies.txt")
    args = args[0:1] + cookieHandling + args[1:]
    if len(replacements)>0:
        args = [applyAllReplacements(a, replacements) for a in args]
    
    # from https://stackoverflow.com/questions/4760215/running-shell-command-and-capturing-the-output
    result = subprocess.run(args, stdout=subprocess.PIPE)
    htmlcode = result.stdout.decode('utf-8')
    tree = html.fromstring(htmlcode)  # Build an lxml-tree for easy access to element via XPath
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


# Use cached page to avoid too many requests
if os.path.exists("home.html"):
    with open("home.html", "r") as f:
        s = html.parse("home.html")
else:
    s = performLogin()
    with open("home.html", "wb") as f:
        f.write(html.tostring(s))

for a in s.findall(".//nav/a"):
    d = a.find("./div")
    if d!=None:
        print(a.attrib['href'])
        print(d.text)
