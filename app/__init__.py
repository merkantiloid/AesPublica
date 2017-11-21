from flask import Flask, g, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from preston.esi import Preston
from urllib.parse import quote
from .filters import fldate

mainApp = Flask(__name__)
mainApp.config.from_object('config')
mainApp.config.from_envvar('ESI_CONFIG', silent=True)

mainApp.jinja_env.filters['fldate'] = fldate

db = SQLAlchemy(mainApp)

lm = LoginManager()
lm.init_app(mainApp)

preston = Preston(
    client_id=mainApp.config.get('ESI_CLIENT_ID',''),
    client_secret=mainApp.config.get('ESI_SECRET',''),
    callback_url=quote(mainApp.config.get('ESI_CALLBACK_URL',''), safe=''),
    scope='esi-skills.read_skills.v1',
    user_agent='Probleme',
)

from .models import User


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@lm.unauthorized_handler
def unauthorized_callback():
    return redirect('/login')


@mainApp.before_request
def before_request():
    g.user = current_user


from app import views