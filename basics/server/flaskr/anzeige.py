from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from datetime import datetime

from flaskr.auth import login_required
from flaskr.db import get_db
from flaskr.misc import times
from flaskr.plotting import plot_voltage
from flaskr.convert_to_bin import convert_to_bin
from flaskr.logs import get_hash
from flask import request

import os

bp = Blueprint('anzeige', __name__)

def calculate_sleep_time():
    current_time = datetime.now()
    sleep_time = 0
    for time in times:
        if (current_time < time):
            sleep_time = (time - current_time).seconds
            break

    return sleep_time

def plot_graph(macid, mac):
    path = f"flaskr/static/macs/{macid}"

    # remove all files in the directory
    for file in os.listdir(path):
        os.remove(f"{path}/{file}")

    plot_voltage(path, macid, mac)
    convert_to_bin(path)

def calc_image_update(macid, hash):
    db = get_db()

    roomid = db.execute('SELECT roomid FROM mac WHERE id = ?', (macid,)).fetchone()[0]
    hash_db = 0
    if (roomid != None):
        # TODO get latest xml file and create .bin

        with open(f"flaskr/static/rooms/{roomid}/data.bin", 'wb') as f:
            f.write(b'\0' * 96*1024)
        
        hash_db = get_hash(roomid)

        if (hash_db == hash):
            roomid = -1
    else:
        roomid = 0
    return roomid, hash_db

def calc_firmware_upadte(firmware):
    path = "flaskr"+url_for('static', filename='firmware/')
    files = os.listdir(path)
    firmware = int(firmware.replace('-', ''))

    latest_version = -1
    int_latest_version = -1

    for file in files:
        if not file.endswith('.bin'):
            continue

        version = file.split('.')[0]
        int_version = int(version.replace('-', ''))

        if (int_version > firmware):
            if (int_latest_version < int_version):
                latest_version = version
                int_latest_version = int_version
        
    return latest_version


@bp.route('/anzeige')
def index():
    mac = request.args.get('mac')
    volt = request.args.get('volt')
    firmware = request.args.get('firmware')
    print(firmware)
    hash = request.args.get('hash')

    db = get_db()

    macid = db.execute('SELECT id FROM mac WHERE mac = ?',(mac,)).fetchone()

    if (macid == None):
        db.execute('INSERT INTO mac (mac) VALUES (?)', (mac, ))
        db.commit()

        macid = db.execute('SELECT id FROM mac WHERE mac = ?',(mac,)).fetchone()
        try:
            os.makedirs(f"flaskr/static/macs/{macid[0]}")
        except OSError:
            pass
        
    macid = macid[0]
    db.execute('INSERT INTO volt (volt, macid) VALUES (?, ?)', (volt, macid))
    db.commit()
    plot_graph(macid, mac)

    roomid, hash_db = calc_image_update(macid, hash)

    update_firmware = calc_firmware_upadte(firmware)

    # generate graph if needed
    if (roomid == 0):
        plot_graph(macid, mac)

    sleep_time = calculate_sleep_time()
    sleep_time = 120 # for testing purposes

    return render_template('anzeige/index.html', firmware=update_firmware, roomid=roomid, macid=macid, sleep_time=sleep_time, hash=hash_db)