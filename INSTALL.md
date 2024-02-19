# Benötige Software für das Projekt
Allgemein:
  * Visual Studio Code (via Windows AppStore)
  * Python3 (via Windows AppStore)
  * git (https://gitforwindows.org/)
    * bash (bereits in git als git-bash enthalten)
    * ssh (nach einem Vierteljahrhundert jetzt auch native in Windows enthalten)

## Python libraries
  * icalendar
  * lxml

### Installation unter Windows:
```bash
pip install icalendar lxml cairosvg
```

### Installation unter Ubuntu: 
```bash
sudo apt install python3-icalendar python3-lxml python3-cairosvg
```
Man könnte auch pip3 verwenden, was aber unter Umständen zu Konflikten mit dem Paketmanager apt führen kann.
Eine weitere, saubere Alternative sind virtuelle Python-Environments


[Zurück](README.md) zum README
