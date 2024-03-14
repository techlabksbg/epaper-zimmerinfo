from flask import Flask, render_template, request, Response
from flask_basicauth import BasicAuth
from flaskr.crawler import get_xml
from lxml import html
import flaskr.mysecrets as mysecrets
import os

app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = mysecrets.login_web
app.config['BASIC_AUTH_PASSWORD'] = mysecrets.password_web

basic_auth = BasicAuth(app)

@app.route('/room')
@basic_auth.required
def room_xml():
    roomname = request.args.get('roomname')
    if (roomname == None):
        return Response("", mimetype='text/xml')
    
    xml = get_xml(roomname)
    
    if (xml == None):
        return Response("", mimetype='text/xml')
    print(html.tostring(xml))
    return Response(html.tostring(xml), mimetype='text/xml')
