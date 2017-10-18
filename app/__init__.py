from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

mainApp = Flask(__name__)
mainApp.config.from_object('config')
db = SQLAlchemy(mainApp)

lm = LoginManager()
lm.init_app(mainApp)


from .models import User


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


from app import views