from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db
from flaskr.plotting import plot_voltage
from flask import request

import os

bp = Blueprint('logs', __name__)

@bp.route('/')
def index():
    db = get_db()
    macs = db.execute('SELECT id, roomid, mac FROM mac').fetchall()

    new_macs = []
    for mac in macs:
        macname = mac['mac']

        roomname = db.execute('SELECT roomname FROM room WHERE id = ?', (mac['roomid'], )).fetchone()
        if (roomname == None):
            roomname = "No room name available yet"
        else:
            roomname = roomname['roomname']

        battery = db.execute('SELECT volt, statusTime FROM volt WHERE macid = ? ORDER BY(statusTime) DESC', (mac['id'],)).fetchone()
        if (battery == None):
            battery = "No Battery Information available yet"
        else:
            battery = battery['volt']

        new_macs.append({'roomname':roomname, 'macid':mac['id'], 'battery':battery, 'macname':macname})

    return render_template('logs/index.html', macs=new_macs)

@bp.route('/<int:id>/logs')
def log(id):
    db = get_db()
    volts = db.execute('SELECT volt, statusTime FROM volt WHERE macid = ? ORDER BY(statusTime) ASC', (id, )).fetchall()

    mac = db.execute('SELECT mac, roomid FROM mac WHERE id = ?', (id, )).fetchone()
    roomid = mac['roomid']
    mac = mac['mac']

    room = db.execute('SELECT roomname FROM room WHERE id = ?', (roomid, )).fetchone()
    if (room == None):
        room = None
    else:
        room = room[0]

    return render_template('logs/log.html', volts=volts, mac=mac, room=room, id=str(id))

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        mac = request.form['mac']
        roomname = request.form['roomname']
        error = None

        if not mac:
            error = 'MAC-Address required.'
        if not roomname:
            error = 'room name required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()

            roomid = db.execute('SELECT id FROM room WHERE roomname = ?', (roomname, )).fetchone()
            if (roomid == None):
                db.execute('INSERT INTO room (roomname) VALUES (?)', (roomname, ))
                db.commit()

                roomid = db.execute('SELECT id FROM room WHERE roomname = ?', (roomname, )).fetchone()
                os.makedirs(f"flaskr/static/rooms/{roomid[0]}")

            roomid = roomid[0]

            mac_for_room = db.execute('SELECT mac FROM mac WHERE roomid = ?', (roomid, )).fetchone()
            if (mac_for_room != None):
                error = 'Room already has mac ' + str(mac_for_room[0]) + ' assigned to it.'
                flash(error)
                return render_template('logs/create.html')

            macid = db.execute('SELECT id FROM mac WHERE mac = ?', (mac, )).fetchone()
            if (macid == None):
                db.execute('INSERT INTO mac (roomid, mac) VALUES (?, ?)', (roomid, mac))
                db.commit()

                macid = db.execute('SELECT id FROM mac WHERE mac = ?', (mac, )).fetchone()[0]
                os.makedirs(f"flaskr/static/macs/{macid}")

                plot_voltage(f"flaskr/static/macs/{macid}", macid, mac)
            else:
                db.execute('UPDATE mac SET roomid = ? WHERE mac = ?', (roomid, mac))
                db.commit()

            return redirect(url_for('logs.index'))

    return render_template('logs/create.html')

