from flask import Flask, render_template, request, Response
from flask_basicauth import BasicAuth
from flaskr.crawler import get_xml
from lxml import html
import os

app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = 'a'
app.config['BASIC_AUTH_PASSWORD'] = 'b'

basic_auth = BasicAuth(app)

@app.route('/room')
@basic_auth.required
def room_xml():
    roomname = request.args.get('roomname')
    if (roomname == None):
        return Response("<xml></xml>", mimetype='text/xml')
    
    xml = get_xml(roomname)
    
    if (xml == None):
        return Response("<xml></xml>", mimetype='text/xml')
    
    return Response(html.tostring(xml), mimetype='text/xml')
