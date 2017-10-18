from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user

mainApp = Flask(__name__)
mainApp.config.from_object('config')
db = SQLAlchemy(mainApp)

lm = LoginManager()
lm.init_app(mainApp)


from .models import User


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@mainApp.before_request
def before_request():
    g.user = current_user

from app import views