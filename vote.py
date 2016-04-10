from flask import render_template, Response, Blueprint, current_app, request, redirect, abort
from objects import Waifu
from werkzeug import secure_filename
from blitzdb import queryset, FileBackend
import blitzdb
from PIL import Image
from resizeimage import resizeimage
import os
votes = Blueprint('Votes', __name__)

@votes.route("/")
def home():
    waifus = current_app.dbbackend.filter(Waifu, {"type":"Waifu"})
    waifus = waifus.sort(key="votes", order=blitzdb.queryset.QuerySet.DESCENDING)
    return render_template("index.html", waifus=waifus)

@votes.route("/vote/<pk>")
def vote(pk):
    print(pk)
    if request.method == 'GET':
        if pk + '_vote' in request.cookies:
            return redirect('/already_voted')
        redirect_to_index = redirect("/thankyou")
        response = current_app.make_response(redirect_to_index)
        response.set_cookie(pk + '_vote', value='true')
        waifu = current_app.dbbackend.filter(Waifu, {'pk':pk})
        ip = request.headers['X-Forwarded-For']
        try:
            if ip in waifu[0].votes_l:
                return redirect("/already_voted")
            waifu[0].votes_l.append(ip)
        except:
            waifu[0].votes_l = list()
            waifu[0].votes_l.append(ip)
        waifu[0].votes = waifu[0].votes + 1

        current_app.dbbackend.save(waifu[0])
        current_app.dbbackend.commit()
        current_app.dbbackend = FileBackend("./database")
    return response

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in current_app.config['ALLOWED_EXTENSIONS']

@votes.route("/add_waifu", methods=['GET','POST'])
def add_waifu():
    if request.method == 'GET':
        return render_template("add_waifu.html")
    if request.method=='POST':
        name = request.form["name"]
        w_file = request.files["file"]
        w_type = "Waifu"
        votes = 0
        origin = request.form["origin"]
        waifu = Waifu({
            "name":name,
            "type":"Waifu",
            "votes":votes,
            "origin":origin,
            "file_path":""
        })

        if w_file and allowed_file(w_file.filename):
            current_app.dbbackend.save(waifu)

            filename = secure_filename(w_file.filename)
            folder = os.path.join(current_app.config['UPLOAD_FOLDER'], waifu.pk)

            if not os.path.exists(folder):
                os.makedirs(folder)
            file_path = os.path.join(folder, filename)
            image = Image.open(w_file)
            image = resizeimage.resize_cover(image,[185,185])
            image.save(file_path)
            waifu.file_path = os.path.join("/static/content/", waifu.pk, filename)
            current_app.dbbackend.save(waifu)
            current_app.dbbackend.commit()
            return redirect("/thankyou_add")
    pass
@votes.route("/waifu/<pk>")
def view_waifu(pk):
    try:
        waifu = current_app.dbbackend.get(Waifu,{'pk':pk})
    except Waifu.DoesNotExist:
        return abort(404)
        pass
    return render_template("waifu.html", waifu=waifu)

@votes.route("/thankyou_add")
def thankyou_add():
    return render_template("thankyou_add.html")

@votes.route("/thankyou")
def thankyou():
    return render_template("thankyou.html")

@votes.route("/already_voted")
def already_voted():
    return render_template("already_voted.html")
