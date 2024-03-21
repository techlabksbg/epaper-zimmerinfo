from flask import (
    Blueprint, flash, redirect, render_template, request, url_for, current_app
)

from datetime import datetime # Import datetime module
import hashlib
from PIL import Image

from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename

from flaskr.__init__ import basic_auth
from flaskr.db import get_db
from flaskr.plotting import plot_voltage
from flaskr.voltage2percentage import voltage2percentage
from flaskr.imageConversion import dither_to_bin_and_rgb
from flaskr.datalogic import id_for_room, id_for_mac

import os

bp = Blueprint('logs', __name__)

def get_hash(roomid):
    path = "flaskr"+url_for('static', filename=f'rooms/{roomid}/data.bin')
    hash = ""
    with open(path, 'rb') as f:
        data = f.read()
        hash = hashlib.md5(data).hexdigest()
    return hash[:16]

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
            battery = None
        else:
            battery = voltage2percentage(battery['volt'])*100

        new_macs.append({'roomname':roomname, 'macid':mac['id'], 'battery':battery, 'macname':macname})

    return render_template('logs/index.html', macs=new_macs)

@bp.route('/<int:id>/logs')
def log(id):
    db = get_db()
    volts = db.execute('SELECT volt, statusTime FROM volt WHERE macid = ? ORDER BY(statusTime) ASC', (id, )).fetchall()
    volts = [dict(row) for row in volts]
    for volt in volts:
        volt['volt'] = voltage2percentage(volt['volt'])*100

    mac = db.execute('SELECT mac, roomid FROM mac WHERE id = ?', (id, )).fetchone()
    if (mac == None):
        return redirect(url_for('logs.index'))
    roomid = mac['roomid']
    mac = mac['mac']

    room = db.execute('SELECT roomname FROM room WHERE id = ?', (roomid, )).fetchone()
    if (room == None):
        room = None
    else:
        room = room['roomname']

    return render_template('logs/log.html', volts=volts, mac=mac, room=room, id=str(id))

@bp.route('/create', methods=('GET', 'POST'))
@basic_auth.required
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

            roomid = id_for_room(roomname)

            mac_for_room = db.execute('SELECT mac FROM mac WHERE roomid = ?', (roomid, )).fetchone()
            if (mac_for_room != None):
                error = 'Room already has MAC-Address ' + str(mac_for_room['mac']) + ' assigned to it.'
                flash(error)
                return render_template('logs/create.html')

            macid = id_for_mac(mac) 
            db.execute('UPDATE mac SET roomid = ? WHERE mac = ?', (roomid, mac))
            db.commit()
            if (macid == None):  # Never happening now, what did it do before?
                # ???
                plot_voltage(f"flaskr/static/macs/{macid}", macid, mac)

            return redirect(url_for('logs.index'))

    return render_template('logs/create.html')

@bp.route('/<int:id>/upload', methods=('GET', 'POST'))
@basic_auth.required
def upload_image(id):
    if request.method == 'POST':
        # Check if the POST request has the file part
        if 'image' not in request.files:
            return 'No file part'

        image = request.files['image']

        # If the user does not select a file, the browser may also
        # submit an empty part without filename
        if image.filename == '':
            return 'No selected image'

        # Generate a unique filename based on the current time, page ID, and secure filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{id}/{timestamp}"
        pngfilename = filename+".png"
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename) 
        binpath = os.path.join(current_app.config['BINARIES_FOLDER'], filename+".bin") 
        pngfilepath = filepath+".png"
        # Save the image to a folder
        image.save(pngfilepath)
        rgb = Image.open(pngfilepath)
        binary,rgb = dither_to_bin_and_rgb(rgb)
        with open(binpath, "wb") as f:
            f.write(binary)
        rgb.save(pngfilepath, "PNG")

        return render_template('logs/upload_success.html', filename=pngfilename)

    return render_template('logs/upload_form.html', id=id)
