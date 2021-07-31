import os
from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))


def use_dot_env(var_name):
    value = os.environ.get(var_name)
    print(value)
    return value


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", use_dot_env("SECRET_KEY"))

    # Mail Settings
    MAIL_SERVER = os.getenv("MAIL_SERVER", use_dot_env("MAIL_SERVER"))
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", use_dot_env("MAIL_USERNAME"))
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", use_dot_env("MAIL_PASSWORD"))
    MAIL_DEFAULT_SENDER = os.getenv(
        "MAIL_DEFAULT_SENDER", use_dot_env("MAIL_DEFAULT_SENDER")
    )
    MAIL_USE_TLS = True

    # Database settings
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite://")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Media settings
    STATIC_FOLDER = f"{os.getenv('APP_FOLDER')}/app/static"
    MEDIA_FOLDER = f"{os.getenv('APP_FOLDER')}/app/media"
