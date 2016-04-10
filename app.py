from flask import Flask
from blitzdb import FileBackend
from objects import Waifu
from vote import votes
import random
app = Flask(__name__)
app.register_blueprint(votes)
app.dbbackend = FileBackend("./database")
app.config['UPLOAD_FOLDER'] = "/home/eirexe/waifubook/static/content"
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg', 'gif'])

app.config['WAIFU_BGS'] = list(["0.png","1.png"])

def get_random_waifu_bg():
    return random.choice(app.config['WAIFU_BGS'])

app.jinja_env.globals.update(get_random_waifu_bg=get_random_waifu_bg)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
