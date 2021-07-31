from flask import Blueprint, request, render_template, current_app, redirect
import os
from flask.json import jsonify
from app.email import send_email

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

        # Send email
        subject = "File Upload"
        html_message = render_template(
            "email/upload.html",
            data={
                "to_email": to_email,
                "from_email": from_email,
                "message": message,
                "url": "https://www.somecoolurl.com",
            },
        )
        recipients = [to_email, from_email]

        files = request.files.getlist("files[]")
        send_email(recipients, subject, html_message)

        for file in files:
            file_path = os.path.join(current_app.root_path, "upload", file.filename)
            file.save(file_path)

    return jsonify({"url": "https://www.somecoolurl.com"})
