# Benötige Software für das Projekt
Allgemein:
  * Visual Studio Code (via Windows AppStore)
  * Python3 (via Windows AppStore)
  * git (https://gitforwindows.org/)
    * bash (bereits in git als git-bash enthalten)
    * ssh (nach einem Vierteljahrhundert jetzt auch native in Windows enthalten)

## Python libraries
Siehe [Dependencies](python-dependencies.txt).

Es wird empfohlen ein virtuelles Python environment aufzusetzen. Das Script

[install-deps.bash](install-deps.bash)

erledigt das Aufsetzen des venv (in .venv) und installiert gleich auch alle nötigen packages.

Das Environment muss auf der Kommandozeile mit
```bash
source .venv/bin/activate
```
gestartet werden.



[Zurück](README.md) zum README
