from app import views

from flask import Flask, g, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
# from app.filters import fldate # from app.filters import fldate - GPt chat замена относ. пути на абсолют.

from esipy.app import EsiApp
from esipy import EsiClient
from esipy import EsiSecurity

from datetime import datetime, timezone
import logging
from logging.handlers import RotatingFileHandler
from .extensions import db, lm
from .models import User
from app.views import register_blueprints  # Импортируем функцию для регистрации Blueprint

# import os


# Функция создания приложения
def create_app():
    app = Flask(__name__)
    app.config.from_object('config')
    app.config.from_envvar('ESI_CONFIG', silent=True)

    # Инициализация db и lm
    db.init_app(app)
    lm.init_app(app)

    # Вставляем логику до и после запроса
    @app.before_request
    def before_request():
        g.user = current_user

    @app.after_request
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

    # Логирование
    if not app.debug:
        handler = RotatingFileHandler('log/aes-publica.log', maxBytes=10000000, backupCount=3)
        handler.setLevel(logging.INFO)
        handler.setFormatter(logging.Formatter(
            '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
        ))
        app.logger.addHandler(handler)

    # Инициализация ESI
    esiapp = EsiApp(meta_url=app.config.get('ESI_SWAGGER_JSON', ''))
    esiapp.prepare()
    esisecurity = EsiSecurity(
        app=esiapp,
        redirect_uri=app.config.get('ESI_CALLBACK_URL', ''),
        client_id=app.config.get('ESI_CLIENT_ID', ''),
        secret_key=app.config.get('ESI_SECRET', ''),
    )
    esiclient = EsiClient(
        security=esisecurity,
        cache=None,
        headers={'User-Agent': 'Aes Publica'}
    )

    # Регистрируем фильтры Jinja
    def fldate(value):
        return datetime.fromtimestamp(value, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')

    app.jinja_env.filters['fldate'] = fldate

    # Импортируем и регистрируем views
    with app.app_context():
        from . import views  # Импортируем views после создания app контекста

    with app.app_context():
        register_blueprints(app)  # Регистрируем все Blueprint

    return app


@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@lm.unauthorized_handler
def unauthorized_callback():
    return redirect('/login')
