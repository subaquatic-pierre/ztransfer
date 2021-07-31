from flask import Flask, render_template, send_from_directory

app = Flask(__name__)


@app.route("/")
def home(*args, **kwargs):
    return render_template("/index.html")


@app.route("/static/<path:filename>")
def staticfiles(filename):
    return send_from_directory(app.config["STATIC_FOLDER"], filename)


@app.route("/media/<path:filename>")
def mediafiles(filename):
    return send_from_directory(app.config["MEDIA_FOLDER"], filename)
