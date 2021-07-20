from re import A, I
import smtplib
from server.config import Config
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

config = Config()

server_url = config.MAIL_SERVER
default_email = config.MAIL_DEFAULT_SENDER
username = config.MAIL_USERNAME
password = config.MAIL_PASSWORD


def get_server():
    return smtplib.SMTP_SSL(server_url, 465)


# Must add from_email
def send_email(recipients, subject, text_content, html_content, attachment=None):
    msg = MIMEMultipart("alternative")
    msg["From"] = default_email
    msg["To"] = ", ".join(recipients)
    msg["Subject"] = subject

    html = MIMEText(html_content, "html")
    plain_text = MIMEText(text_content, "plain")

    msg.attach(html)
    msg.attach(plain_text)

    server = get_server()
    server.login(username, password)
    server.sendmail(default_email, recipients, msg.as_string())
    server.quit()
