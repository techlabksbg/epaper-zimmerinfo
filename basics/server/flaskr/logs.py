from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db
from flask import request

bp = Blueprint('logs', __name__)

@bp.route('/')
def index():
    db = get_db()
    macs = db.execute('SELECT id, roomid FROM mac').fetchall()

    new_macs = []
    for mac in macs:
        roomname = db.execute('SELECT roomname FROM room WHERE id = ?', (mac['roomid'], )).fetchone()['roomname']
        battery = db.execute('SELECT volt, statusTime FROM volt WHERE macid = ? ORDER BY(statusTime) DESC', (mac['id'],)).fetchone()['volt']
        new_macs.append({'roomname':roomname, 'macid':mac['id'], 'battery':battery})

    return render_template('logs/index.html', macs=new_macs)

@bp.route('/<int:id>/logs')
def log(id):
    db = get_db()
    volts = db.execute('SELECT volt, statusTime FROM volt WHERE macid = ? ORDER BY(statusTime) ASC', (id, )).fetchall()

    return render_template('logs/log.html', volts=volts)

