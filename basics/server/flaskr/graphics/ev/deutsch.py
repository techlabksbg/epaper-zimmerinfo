from datetime import date

wochentage = ['Montag', 'Dienstag', 'Mittwoch', "Donnerstag", 'Freitag', 'Samstag', 'Sonntag']
def wochentag(datum:date) -> str:
    return wochentage[datum.weekday()]

def wochentagDatumKurz(datum:date) -> str:
    return f"{wochentag(datum)[0:2]} {datum.day}.{datum.month}."

def wochentagDatum(datum:date) -> str:
    return f"{wochentag(datum)} {datum.day}.{datum.month}."

monate = ['', 'Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember']
def monat(datum:date) -> str:
    return monate[datum.month]

def datum(dat:date) -> str:
    return f"{wochentag(dat)} {dat.day}. {monat(dat)} {dat.year}"


def lehrerName(name:str, level:int = 0) -> str:
    name = name.strip()
    if (level==0):
        return name
    if (level==1):
        el = name.split(" ")
        print(el)
        return " ".join(el[0:-1])+f" {el[-1][0]}."
    if (level>1):
        return name[0:-level]+"..."
