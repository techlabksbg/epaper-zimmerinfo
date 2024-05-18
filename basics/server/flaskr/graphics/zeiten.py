from datetime import time, datetime, timedelta

anfangszeitenKSBG = [time(t[0],t[1]) for t in [
    [7,40], [8,34], [9,28], [10,30], [11,24], 
    [12,14], [13,4], 
    [13,55], [14,49], [15,43], [16,33], [17,23],
    [18,8], [18,15], [19,00], [19,5], [19,50],[19,55],[20,40],[20,45],[21,30]]]

separatorenKSBG = [0 for z in anfangszeitenKSBG]
separatorenKSBG[2]=separatorenKSBG[4]=separatorenKSBG[6]=1

anfangszeitenISME = [time(t[0],t[1]) for t in [
        [7,45], [8,40], [9,35], [10,40], [11,35], [12,25], [13,15], [14,5], [14,55]]]

rasterZeiten:list[time] = [time(t[0],t[1]) for t in [
    [7,40], [8,34], [9,28], [10,30], [11,24], 
    [12,14], [13,4], 
    [13,55], [14,49], [15,43], [16,33], [17,23],
    [18,15], [19,5], [19,55]]]


def rasterTextKSBG() -> list[list[str]]:
    r = []
    for s in rasterZeiten:
        e = addDelta(s,timedelta(minutes=45))        
        r.append([s.strftime("%H:%M"), e.strftime("- %H:%M")])
    return r

def rasterTextISME() -> list[list[str]]:
    r = []
    for s in anfangszeitenISME:
        e = addDelta(s,timedelta(minutes=45))        
        r.append([s.strftime("%H:%M"), e.strftime(" - %H:%M")])
    return r

def timeToDateTime(zeit:time) -> datetime:
     return datetime(2024,1,1,zeit.hour, zeit.minute)

def timeDifference(zeit1 : time, zeit2 : time) -> timedelta:
     return timeToDateTime(zeit2)-timeToDateTime(zeit1)

def addDelta(zeit:time, delta:timedelta) -> time:
     return (timeToDateTime(zeit)+delta).time()

def getRasterPosition(zeit:time) -> float:
    print(f"getRasterPosition({zeit})")
    if (zeit<rasterZeiten[0]):
         print("   zu früh -> 0")
         return 0.0
    if (zeit>rasterZeiten[-1]):
         delta = timeDifference(rasterZeiten[-1], zeit)
         if delta.seconds>45*60:
            print(f"   zu spät -> {len(rasterZeiten)}")
            return len(rasterZeiten)
         print(f"   zu spät, interpoliert:-> {len(rasterZeiten)-1 + delta.seconds/(45*60)}")
         return len(rasterZeiten)-1 + delta.seconds/(45*60)
    startIndex = min([i for i in range(len(rasterZeiten)) if rasterZeiten[i]>=zeit])
    delta = timeDifference(rasterZeiten[startIndex], zeit)
    print(f"   startIndex={startIndex}, -> delta={delta}  (time at index:{rasterZeiten[startIndex]})")
    return startIndex + delta.seconds/(45*60)
    


