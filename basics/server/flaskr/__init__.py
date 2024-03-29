import os

from flask import Flask
from flask_basicauth import BasicAuth
# Stupid default values for the user
if not os.path.exists("flaskr/mysecrets.py"):
    with open("flaskr/mysecrets.py","w") as f:
        f.write("login='user'\npassword='pass'\n")

import flaskr.mysecrets as mysecrets 
basic_auth = BasicAuth()

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
        UPLOAD_FOLDER='flaskr/static/uploads', # Change the folder path accordingly
        BINARIES_FOLDER='flaskr/static/binaries',
        FIRMWARE_FOLDER='flaskr/static/firmware',
        ROOMS_FOLDER='flaskr/static/rooms',
        MACS_FOLDER='flaskr/static/macs',
        BASIC_AUTH_USERNAME=mysecrets.login,
        BASIC_AUTH_PASSWORD=mysecrets.password
    )

    basic_auth = BasicAuth(app)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import logs
    app.register_blueprint(logs.bp)

    from . import anzeige
    app.register_blueprint(anzeige.bp)

    return app
