import sqlite3

import click
from flask import current_app, g
import shutil
import os


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    shutil.rmtree("flaskr/static/macs", ignore_errors=True)
    shutil.rmtree("flaskr/static/rooms", ignore_errors=True)
    shutil.rmtree("flaskr/static/uploads", ignore_errors=True)
    shutil.rmtree("flaskr/static/binaries", ignore_errors=True)
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    try:
        os.makedirs(f"flaskr/static/macs/")
        os.makedirs(f"flaskr/static/rooms/")
        os.makedirs(f"flaskr/static/uploads/")
        os.makedirs(f"flaskr/static/binaries/")
    except OSError:
        pass
    app.cli.add_command(init_db_command)