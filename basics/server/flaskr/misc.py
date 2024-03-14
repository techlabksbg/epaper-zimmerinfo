from datetime import datetime

now = datetime.now()

six = now.replace(hour=6, minute=0, second=0, microsecond=0)
ten = now.replace(hour=10, minute=0, second=0, microsecond=0)
twelve = now.replace(hour=12, minute=0, second=0, microsecond=0)
seventeen = now.replace(hour=17, minute=0, second=0, microsecond=0)

times = [six, ten, twelve, seventeen]

xml_server = "http://localhost:5001/room"