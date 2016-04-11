from flask import Flask, g, redirect, session, json
from flask.ext.openid import OpenID
from blitzdb import FileBackend
from objects import Waifu, User
from vote import votes
from steam import get_steam_userinfo
from config import _cfg, _cfgi
import re

import random

app = Flask(__name__)
app.register_blueprint(votes)
app.dbbackend = FileBackend("./database")
app.config['UPLOAD_FOLDER'] = _cfg("content-folder")
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg', 'gif', 'JPEG', 'JPG', 'PNG', 'GIF'])

app.config['WAIFU_BGS'] = list(["0.png","1.png"])
app.config['STEAM_API_KEY'] = _cfg("steam-api-key")
app.oid = OpenID(app)
app.secret_key = _cfg("secret-key")
oid = app.oid

_steam_id_re = re.compile('steamcommunity.com/openid/id/(.*?)$')

@app.route('/login')
@oid.loginhandler
def login():
    if 'user_id' in session:
        return redirect(oid.get_next_url())
    return oid.try_login('http://steamcommunity.com/openid')

@oid.after_login
def create_or_login(resp):
    match = _steam_id_re.search(resp.identity_url)
    g.user = User.get_or_create(match.group(1))
    steamdata = get_steam_userinfo(g.user.steam_id)
    g.user.nickname = steamdata['personaname']
    dbbackend.save(g.user)
    dbbackend.commit()
    session['user_id'] = g.user.pk
    flash('You are logged in as %s' % g.user.nickname)
    return redirect(oid.get_next_url())

def get_random_waifu_bg():
    return random.choice(app.config['WAIFU_BGS'])

app.jinja_env.globals.update(get_random_waifu_bg=get_random_waifu_bg)

if __name__ == "__main__":
    app.run(host=_cfg("host"), port=_cfgi("port"), debug=True)

@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = dbbackend.get(User, {"pk":session['user_id']})

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(oid.get_next_url())
