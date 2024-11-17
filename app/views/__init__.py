from flask import Blueprint, render_template, redirect
from flask_login import login_user, logout_user
import bcrypt

from app.extensions import db  # Импорт из extensions
from .calc import calc_bp  # Импортируем Blueprint калькулятора
from ..forms import LoginForm, RegisterForm
from ..models import User

import app.views.calc
import app.views.mscan
import app.views.moonmat
from .characters import characters
from .search import search_type

views_bp = Blueprint('views', __name__)


# Регистрация Blueprint для калькулятора
def register_blueprints(app):
    app.register_blueprint(calc_bp)  # Регистрируем Blueprint в приложении


@views_bp.route('/login', methods=['GET'])
def login_get():
    form = LoginForm()
    return render_template('login.html', form=form)


@views_bp.route('/login', methods=['POST'])
def login():
    form = LoginForm()
    if not form.validate_on_submit():
        return render_template('login.html', form=form)
    registered_user = User.query.filter_by(name=form.name.data).first()
    login_user(registered_user)
    return redirect("/")


@views_bp.route('/logout')
def logout():
    logout_user()
    return redirect('/login')


@views_bp.route('/register', methods=['GET'])
def register_get():
    form = RegisterForm()
    return render_template('register.html', form=form)


@views_bp.route('/register', methods=['POST'])
def register():
    form = RegisterForm()
    if not form.validate_on_submit():
        return render_template('register.html', form=form)
    hash = bcrypt.hashpw(form.password.data.encode(), bcrypt.gensalt())
    user = User(name=form.name.data, hash=hash)
    db.session.add(user)
    db.session.commit()

    return redirect("/")
