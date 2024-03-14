from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from datetime import datetime

from flaskr.__init__ import basic_auth
from flaskr.db import get_db
from flaskr.misc import times
from flaskr.plotting import plot_voltage
from flaskr.convert_to_bin import convert_to_bin
from flaskr.logs import get_hash
from flaskr.voltage2percentage import volatage2percentage
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
        if (not os.path.isfile("flaskr"+url_for('static', filename=f'rooms/{roomid}/data.bin'))):
            roomid = 0
            return roomid, hash_db
        hash_db = get_hash(roomid)

        if (hash_db == hash):
            roomid = -1
    else:
        roomid = 0
    return roomid, hash_db

def calc_firmware_update(firmware):
    if (firmware == None):
        return -1
    path = "flaskr"+url_for('static', filename='firmware/')
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

def xml_to_bin(roomid):
    db = get_db()
    path = f"flaskr/static/rooms/{roomid}/data.bin"
    macid = db.execute('SELECT id FROM mac WHERE roomid = ?', (roomid,)).fetchone()
    if (macid == None):
        raise ValueError(f"Roomid {roomid} has no mac assigned to it")
    macid = macid[0]

    teacher = db.execute('SELECT teacher FROM room WHERE id = ?', (roomid,)).fetchone()[0]

    volt = db.execute('SELECT volt, statusTime FROM volt WHERE macid = ? ORDER BY(statusTime) DESC', (macid,)).fetchone()
    percentage = volatage2percentage(volt[0])
    
    with open(path, 'wb') as f:
        f.write(b'0')


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
            os.makedirs(f"flaskr/static/uploads/{macid[0]}")
        except OSError:
            pass
        
    macid = macid[0]
    db.execute('INSERT INTO volt (volt, macid) VALUES (?, ?)', (volt, macid))
    db.commit()
    plot_graph(macid, mac)

    roomid, hash_db = calc_image_update(macid, hash)

    update_firmware = calc_firmware_update(firmware)

    # generate graph if needed
    if (roomid == 0):
        plot_graph(macid, mac)

    sleep_time = calculate_sleep_time()
    sleep_time = 120 # for testing purposes

    return render_template('anzeige/index.html', firmware=update_firmware, roomid=roomid, macid=macid, sleep_time=sleep_time, hash=hash_db)

@bp.route('/xml', methods=['POST', 'GET'])
@basic_auth.required
def xml():
    if (request.method == 'POST'):
        # get the data from the request
        roomname = request.args.get('roomname')
        xmldata = request.files['file']

        db = get_db()
        roomid = db.execute('SELECT id FROM room WHERE roomname = ?', (roomname, )).fetchone()
        xmldata.save(f"flaskr/static/rooms/{roomid[0]}/data.xml")
        xml_to_bin(roomid[0])
        return "OK"
    else:
        db = get_db()
        roomnames = db.execute('SELECT roomname FROM room INNER JOIN mac ON mac.roomid = room.id').fetchall()
        roomnames = [str(name[0])+"\n"for name in roomnames]
        roomnames = "".join(roomnames)
        return roomnames
