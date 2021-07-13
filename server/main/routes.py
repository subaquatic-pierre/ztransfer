from flask import Blueprint
from flask import render_template

main = Blueprint("main", __name__)


# Show home page template
@main.route("/")
def home():
    return render_template("/index.html")
