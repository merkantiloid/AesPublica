from app import views

from flask import Flask, g, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
# from app.filters import fldate # from app.filters import fldate - GPt chat замена относ. пути на абсолют.

from esipy.app import EsiApp
from esipy import EsiClient
from esipy import EsiSecurity

from datetime import datetime, timezone
from .models import User
# import os

mainApp = Flask(__name__)
mainApp.config.from_object('config')
mainApp.config.from_envvar('ESI_CONFIG', silent=True)

if not mainApp.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    handler = RotatingFileHandler('log/aes-publica.log', maxBytes=10000000, backupCount=3)
    handler.setLevel(logging.INFO)
    handler.setFormatter(logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    ))
    mainApp.logger.addHandler(handler)


def fldate(value):
    return datetime.fromtimestamp(value, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')


mainApp.jinja_env.filters['fldate'] = fldate

db = SQLAlchemy(mainApp)

lm = LoginManager()
lm.init_app(mainApp)


# def _hook(url):
#     return 'file://'+os.getcwd()+'/swagger.t.json'
# esiapp = App.load(mainApp.config.get('ESI_SWAGGER_JSON',''), url_load_hook=_hook)

esiapp = EsiApp(meta_url=mainApp.config.get('ESI_SWAGGER_JSON', ''))
esiapp.prepare()
esisecurity = EsiSecurity(
    app=esiapp,
    redirect_uri=mainApp.config.get('ESI_CALLBACK_URL', ''),
    client_id=mainApp.config.get('ESI_CLIENT_ID', ''),
    secret_key=mainApp.config.get('ESI_SECRET', ''),
)

esiclient = EsiClient(
    security=esisecurity,
    cache=None,
    headers={'User-Agent': 'Aes Publica'}
)


@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@lm.unauthorized_handler
def unauthorized_callback():
    return redirect('/login')


@mainApp.after_request
def save_user_action(response):
    if g.user.is_authenticated:
        db.session.add(models.UserAction(
            user_id=g.user.id,
            path=str(request.url_rule),
            created_at=datetime.now().isoformat())
        )
        db.session.commit()
    else:
        db.session.add(models.UserAction(
            user_id=-1,
            path=str(request.url_rule),
            created_at=datetime.now().isoformat())
        )
        db.session.commit()

    return response


@mainApp.before_request
def before_request():
    g.user = current_user
