from flask import render_template, redirect
from app import mainApp, db
from .forms import LoginForm, RegisterForm
from .models import User
import bcrypt

@mainApp.route('/')
@mainApp.route('/index')

def index():
    user = {'nickname': 'Miguel'}  # fake user
    posts = [  # fake array of posts
        {
            'author': {'nickname': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)


@mainApp.route('/login', methods=['GET'])
def login_get():
    form = LoginForm()
    return render_template('login.html', form=form)


@mainApp.route('/login', methods=['POST'])
def login():
    form = LoginForm()
    if not form.validate_on_submit():
        return render_template('login.html', form=form)
    return redirect("/index")


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