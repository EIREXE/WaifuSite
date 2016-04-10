from flask import Flask
from blitzdb import FileBackend
from objects import Waifu
from vote import votes
from config import _cfg, _cfgi
import random
app = Flask(__name__)
app.register_blueprint(votes)
app.dbbackend = FileBackend("./database")
app.config['UPLOAD_FOLDER'] = _cfg("content-folder")
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg', 'gif', 'JPEG', 'JPG', 'PNG', 'GIF'])

app.config['WAIFU_BGS'] = list(["0.png","1.png"])

def get_random_waifu_bg():
    return random.choice(app.config['WAIFU_BGS'])

app.jinja_env.globals.update(get_random_waifu_bg=get_random_waifu_bg)

if __name__ == "__main__":
    app.run(host=_cfg("host"), port=_cfgi("port"), debug=True)
