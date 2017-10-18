from flask import render_template, flash, redirect
from app import mainApp
from .forms import LoginForm

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
def login():
    form = LoginForm()
    return render_template('login.html', title='Sign In', form=form)


@mainApp.route('/login', methods=['POST'])
def login_submit():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="%s", remember_me=%s' % (form.openid.data, str(form.remember_me.data)))
        return redirect('/index')
    return render_template('login.html', title='Sign In', form=form)