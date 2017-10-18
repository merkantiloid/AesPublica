from flask import render_template, redirect
from flask_login import login_user, login_required, logout_user

from app import mainApp, db
from .forms import LoginForm, RegisterForm
from .models import User
import bcrypt

@mainApp.route('/')
@mainApp.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')


@mainApp.route('/login', methods=['GET'])
def login_get():
    form = LoginForm()
    return render_template('login.html', form=form)


@mainApp.route('/login', methods=['POST'])
def login():
    form = LoginForm()
    if not form.validate_on_submit():
        return render_template('login.html', form=form)
    registered_user = User.query.filter_by(name=form.name.data).first()
    login_user(registered_user)
    return redirect("/index")


@mainApp.route('/logout')
def logout():
    logout_user()
    return redirect('/login')


@mainApp.route('/register' , methods=['GET'])
def register_get():
    form = RegisterForm()
    return render_template('register.html', form=form)


@mainApp.route('/register' , methods=['POST'])
def register():
    form = RegisterForm()
    if not form.validate_on_submit():
        return render_template('register.html', form=form)
    hash = bcrypt.hashpw(form.password.data.encode(), bcrypt.gensalt())
    user = User(name=form.name.data, hash=hash)
    db.session.add(user)
    db.session.commit()

    return redirect("/index")