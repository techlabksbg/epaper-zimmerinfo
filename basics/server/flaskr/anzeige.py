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
        db.execute('INSERT INTO mac (mac) VALUES (?)',
        (mac, ))
        db.commit()

        macid = db.execute(
        'SELECT id FROM mac WHERE mac = ?',(mac,)
        ).fetchone()
        
    macid = macid[0]
    db.execute('INSERT INTO volt (volt, macid) VALUES (?, ?)', (volt, macid))
    db.commit()

    return redirect(url_for('logs.index'))