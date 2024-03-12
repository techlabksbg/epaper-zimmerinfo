from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db
from flask import request

bp = Blueprint('anzeige', __name__)

@bp.route('/anzeige')
def index():
    mac = request.args.get('mac')
    volt = request.args.get('volt')

    db = get_db()

    macid = db.execute(
        'SELECT id FROM mac WHERE mac = ?',(mac,)
    ).fetchone()
    print(macid)

    if (macid == None):
        # TODO get room
        room = "H21"+str(mac)
        db.execute('INSERT INTO room (roomname) VALUES (?)', (room, ))
        roomid = db.execute('SELECT id FROM room WHERE roomname = ?', (room, )).fetchone()[0]

        print(roomid, mac)
        db.execute('INSERT INTO mac (mac, roomid) VALUES (?, ?)',
        (mac, roomid))
        db.commit()

        macid = db.execute(
        'SELECT id FROM mac WHERE mac = ?',(mac,)
        ).fetchone()

    macid = macid[0]
    
    db.execute('INSERT INTO volt (volt, macid) VALUES (?, ?)', (volt, macid))
    db.commit()

    #displays = db.execute('SELECT id, mac, volt FROM displays').fetchall()
    #for row in displays:
    #    print(row[:])
    #    print(row["volt"])
    #    print()
    return redirect(url_for('logs.index'))