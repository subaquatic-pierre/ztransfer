import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Set secret code for application to prevent CSRF token (cross site request forgery token) used by WTForms, should set environment vairable
    SECRET_KEY = os.environ.get("SECRET_KEY")

    # Database setup
    SQLALCHEMY_DATABASE_URI = os.environ.get("DB_URI")
