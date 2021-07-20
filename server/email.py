from re import A
from threading import Thread
from flask import current_app
import smtplib


def send_email(app):
    config = app.config

    print(config.get("MAIL_SERVER"))
    server = smtplib.SMTP_SSL(config.get("MAIL_SERVER"), 465)

    server.login(config.get("MAIL_USERNAME"), config.get("MAIL_PASSWORD"))

    server.sendmail(
        "pierre@divesandybeach.com", "subaquatic.pierre@gmail.com", msg="Test message"
    )

    server.quit()
