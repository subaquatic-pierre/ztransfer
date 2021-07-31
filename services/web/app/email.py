import smtplib
from app.config import Config
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
def send_email(recipients, subject, html_content):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = default_email
    msg["To"] = ", ".join(recipients)

    html = MIMEText(html_content, "html")
    text = MIMEText("This is not the text i want to send", "plain")

    msg.attach(text)
    msg.attach(html)

    server = get_server()
    server.login(username, password)
    server.sendmail(default_email, recipients, msg.as_string())
    server.quit()
