wochentage = ['Montag', 'Dienstag', 'Mittwoch', "Donnerstag", 'Freitag', 'Samstag', 'Sonntag']
def wochentag(datum):
    return wochentage[datum.weekday()]

monate = ['', 'Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember']
def monat(datum):
    return monate[datum.month]

def datum(dat) -> str:
    return f"{wochentag(dat)} {dat.day}. {monat(dat)} {dat.year}"


def lehrerName(name:str, level:int = 0) -> str:
    name = name.strip()
    print(f"->{name}<-")
    if (level==0):
        return name
    if (level==1):
        el = name.split(" ")
        print(el)
        return " ".join(el[0:-1])+f" {el[-1][0]}."
    if (level>1):
        return name[0:-level]+"..."
