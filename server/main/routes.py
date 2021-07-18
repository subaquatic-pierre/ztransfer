from flask import Blueprint, request, render_template, current_app, redirect
import os
from flask.helpers import url_for
from flask.json import jsonify

main = Blueprint("main", __name__)


# Show home page template
@main.route("/")
def home():
    return render_template("main/index.html")


@main.route("/upload-files", methods=["POST"])
def upload_files():
    if request.method == "POST":
        files = request.files.getlist("files[]")
        for file in files:
            print(file)
            file.save(os.path.join(current_app.root_path, "uploads", file.filename))

    return redirect(url_for("main.home"))
