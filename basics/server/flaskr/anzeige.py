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
    if (roomid != None):
        hash_db = db.execute('SELECT hash FROM room WHERE id = ?', (roomid,)).fetchone()[0]

        if (hash_db == hash):
            roomid = -1
    else:
        roomid = 0
    return roomid, hash_db

def calc_firmware_upadte(firmware):
    return -1

@bp.route('/anzeige')
def index():
    mac = request.args.get('mac')
    volt = request.args.get('volt')
    firmware = request.args.get('firmware')
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

    print(macid[0])
        
    macid = macid[0]
    db.execute('INSERT INTO volt (volt, macid) VALUES (?, ?)', (volt, macid))
    db.commit()

    roomid, hash_db = calc_image_update(macid, hash)

    sleep_time = calculate_sleep_time()
    sleep_time = 120 # for testing purposes

    update_firmware = calc_firmware_upadte(firmware)

    # generate graph if needed
    if (roomid == 0):
        plot_graph(macid, mac)

    return render_template('anzeige/index.html', firmware=update_firmware, roomid=roomid, macid=macid, sleep_time=sleep_time, hash=hash_db)