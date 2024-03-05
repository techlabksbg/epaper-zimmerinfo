wochentage = ['Montag', 'Dienstag', 'Mittwoch', "Donnerstag", 'Freitag', 'Samstag', 'Sonntag']
def wochentag(datum):
    return wochentage[datum.weekday()]

monate = ['', 'Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember']
def monat(datum):
    return monate[datum.month]

def datum(dat):
    return f"{wochentag(dat)} {dat.day}. {monat(dat)} {dat.year}"


