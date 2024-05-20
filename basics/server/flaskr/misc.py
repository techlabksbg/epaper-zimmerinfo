from datetime import datetime, timedelta

def updatesToday():
    now = datetime.now()

    six = now.replace(hour=7, minute=0, second=0, microsecond=0)
    ten = now.replace(hour=10, minute=0, second=0, microsecond=0)
    twelve = now.replace(hour=12, minute=0, second=0, microsecond=0)
    seventeen = now.replace(hour=15, minute=0, second=0, microsecond=0)
    sixTomorrow = six+timedelta(days=1)

    return [six, ten, twelve, seventeen, sixTomorrow]
