import os
from re import A
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from server.config import Config


# Initialize SQLAlchemy for db functions
db = SQLAlchemy()
mail = Mail()

# Define a create app function to make the application more modular, configure all extensions before creating app, then use the __init function within the craete_app
# function to config extensions to use the app
def create_app():
    # Application variable assigned to Flask object
    app = Flask(__name__)
    # Configure app from Config class defined in config.py module
    app.config.from_object(Config)

    # Initialize extensions with init_app to configure to use app
    db.init_app(app)
    mail.init_app(app)

    # Blueprints used to make modules more modular wtihin app
    # The blueprints are llocated withhhin their own directory within the flaskblog main app
    # each blueprint is the imported into each other module which needs it
    # be sure to import the Blueprint module from flask extension
    # inside each sub module an __init__.py file needs to be created to be seen as a module
    from server.main.routes import main
    from server.errors.handlers import errors

    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
