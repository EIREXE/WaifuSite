from flask import Flask, redirect, session, json, url_for
from flask_oauth import OAuth
from blitzdb import FileBackend
from objects import Waifu, User
from vote import votes
from config import _cfg, _cfgi
from flask.ext.login import login_user, LoginManager, current_user, logout_user
import requests
import re

import random

app = Flask(__name__)
app.register_blueprint(votes)
app.dbbackend = FileBackend("./database")
app.config['UPLOAD_FOLDER'] = _cfg("content-folder")
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg', 'gif', 'JPEG', 'JPG', 'PNG', 'GIF'])
app.config['SERVER_NAME'] = "waifuname.modulous.net"


login_manager = LoginManager()
login_manager.init_app(app)

app.config['WAIFU_BGS'] = list(["0.png","1.png"])

oauth = OAuth()

google = oauth.remote_app('google',
                          base_url='https://www.google.com/accounts/',
                          authorize_url='https://accounts.google.com/o/oauth2/auth',
                          request_token_url=None,
                          request_token_params={'scope': 'https://www.googleapis.com/auth/userinfo.email',
                                                'response_type': 'code'},
                          access_token_url='https://accounts.google.com/o/oauth2/token',
                          access_token_method='POST',
                          access_token_params={'grant_type': 'authorization_code'},
                          consumer_key=_cfg("google-api-key"),
                          consumer_secret=_cfg("google-api-secret"))
app.secret_key = _cfg("secret-key")

def get_random_waifu_bg():
    return random.choice(app.config['WAIFU_BGS'])

app.jinja_env.globals.update(get_random_waifu_bg=get_random_waifu_bg)


@login_manager.user_loader
def load_user(user_id):
    try:
        return app.dbbackend.get(User, {"pk":user_id})
    except User.DoesNotExist:
        return None

@app.route('/login')
def login():
    callback=url_for('authorized', _external=True)
    return google.authorize(callback=callback)



@app.route("/oauth2callback")
@google.authorized_handler
def authorized(resp):
    access_token = resp['access_token']
    for key in resp:
        print(key)
    session['access_token'] = access_token, ''
    r = requests.get('https://www.googleapis.com/oauth2/v1/userinfo?alt=json&access_token=' + resp['access_token'])
    print(r.text)
    rjson = r.json()

    try:
        user = app.dbbackend.get(User, {"google_id": rjson["id"]})
    except User.DoesNotExist:
        user = User({
            "name": rjson['name'],
            "email": rjson['email'],
            "google_picture": rjson['picture'],
            "google_id": rjson['id'],
            "google_token": resp['access_token'],
            "voted_waifus": []
        })
    user.google_token = resp['access_token']
    app.dbbackend.save(user)
    app.dbbackend.commit()
    login_user(user)
    print(current_user.name)
    return redirect("/")

@app.route("/test")
def test():
    print(len(current_user.voted_waifus))
    for waifu in current_user.voted_waifus:
        print(waifu.name)

@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")
@google.tokengetter
def get_access_token():
    return session.get('access_token')
if __name__ == "__main__":
    app.run(host=_cfg("host"), port=_cfgi("port"), debug=True)
