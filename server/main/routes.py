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
        to_email = request.form.get("to_email")
        from_email = request.form.get("from_email")
        message = request.form.get("message")

        print(f"From Email: {from_email} \n To Email: {to_email} \n Message: {message}")

        files = request.files.getlist("files[]")

        for file in files:
            file_path = os.path.join(current_app.root_path, "uploads", file.filename)
            file.save(file_path)

    return jsonify({"url": "https://www.somecoolurl.com"})
