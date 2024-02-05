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
    print(args.__repr__())
    print(replacements.__repr__())
    if len(replacements)>0:
        args = [applyAllReplacements(a, replacements) for a in args]
    
    print(args.__repr__())
    # from https://stackoverflow.com/questions/4760215/running-shell-command-and-capturing-the-output
    result = subprocess.run(args, stdout=subprocess.PIPE)
    htmlcode = result.stdout.decode('utf-8')
    tree = html.fromstring(htmlcode)
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


s = performLogin()



