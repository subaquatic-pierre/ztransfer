from flask import Blueprint, request, render_template, current_app, redirect
import os
from flask.json import jsonify
from flask_mail import Message
from server.email import send_email

main = Blueprint("main", __name__)


# Show home page template
@main.route("/")
def home():
    return render_template("main/index.html")


@main.route("/upload-files", methods=["POST"])
def upload_files():
    if request.method == "POST":
        # to_email = request.form.get("to_email")
        # from_email = request.form.get("from_email")
        to_email = "subuatic.pierre@gmail.com"
        from_email = "pierre@divesandybeach.com"
        message = request.form.get("message")

        # Send email
        subject = "File Upload"
        text_message = message
        html_message = render_template(
            "email/upload.html",
            data={
                "to_email": to_email,
                "from_email": from_email,
                "message": message,
                "url": "https://www.somecoolurl.com",
            },
        )
        recipients = [from_email, to_email]

        files = request.files.getlist("files[]")
        send_email(recipients, subject, text_message, html_message, files[0])

        for file in files:
            file_path = os.path.join(current_app.root_path, "uploads", file.filename)
            file.save(file_path)

    return jsonify({"url": "https://www.somecoolurl.com"})
