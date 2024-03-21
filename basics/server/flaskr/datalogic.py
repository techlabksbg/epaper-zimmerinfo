import os

from flaskr.db import get_db
from flask import current_app

def id_for_mac(mac):
    """
    Returns an id for a mac address.
    If it does not exist, it is created, along with all necessary folders
    """
    db = get_db()
    macid = db.execute('SELECT id FROM mac WHERE mac = ?',(mac,)).fetchone()


    if (macid == None):
        db.execute('INSERT INTO mac (mac) VALUES (?)', (mac, ))
        db.commit()

        macid = db.execute('SELECT id FROM mac WHERE mac = ?',(mac,)).fetchone()[0]
        try:
            #os.makedirs(f"flaskr/static/macs/{macid[0]}")
            os.makedirs(os.path.join(current_app.config['UPLOAD_FOLDER'], str(macid)))
            os.makedirs(os.path.join(current_app.config['BINARIES_FOLDER'], str(macid)))
            os.makedirs(os.path.join(current_app.config['MACS_FOLDER'], str(macid)))
        except OSError:
            pass
    else:
        macid = macid[0]
        
    return macid

def id_for_room(roomname):
    """
    Returns an id for a room name.
    If it does not exist, it is created, along with all necessary folders
    """
    db = get_db()

    roomid = db.execute('SELECT id FROM room WHERE roomname = ?', (roomname, )).fetchone()
    if (roomid == None):
        db.execute('INSERT INTO room (roomname) VALUES (?)', (roomname, ))
        db.commit()

        roomid = db.execute('SELECT id FROM room WHERE roomname = ?', (roomname, )).fetchone()[0]
        os.makedirs(os.path.join(current_app.config['ROOMS_FOLDER'], str(roomid)))
    else:        
        roomid = roomid[0]
    return roomid


def calc_firmware_update(firmware):
    if (firmware == None):
        return -1
    path = current_app.config['FIRMWARE_FOLDER']
    files = os.listdir(path)

    latest_version = firmware

    for file in files:
        if not file.endswith('.bin'):
            continue

        version = file.split('.')[0]
        print(version)
        print(firmware)

        if (version > firmware):
            latest_version = max(latest_version, version)
        
    if (latest_version == firmware):
        return -1
    return latest_version
