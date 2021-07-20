import os
from re import A
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Set secret code for application to prevent CSRF token (cross site request forgery token) used by WTForms, should set environment vairable
    SECRET_KEY = os.environ.get("SECRET_KEY")

    # Database setup
    SQLALCHEMY_DATABASE_URI = os.environ.get("DB_URI")
    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER")
    MAIL_USE_TLS = True
    WALLET_ID = os.environ.get("WALLET_ID")
    WALLET_PUBLIC_KEY = os.environ.get("WALLET_PUBLIC_KEY")
