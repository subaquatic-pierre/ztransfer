from flask import Blueprint, request, render_template
from flask.json import jsonify

main = Blueprint("main", __name__)


# Show home page template
@main.route("/")
def home():
    return render_template("main/index.html")


@main.route("/upload-files")
def upload_files():
    print(request.data)
    reply = {"status": "good job"}

    return jsonify(reply)
