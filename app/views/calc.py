from app import mainApp
from flask import render_template, jsonify
from flask_login import login_required
from app.services import Calc, Static

@mainApp.route('/')
@mainApp.route('/calc')
@login_required
def calc():
    return render_template('calc.html', title='Calc', static=Static.to_json())

@mainApp.route('/calc/data.json')
@login_required
def calc_json():
    c = Calc('z')
    return jsonify(c.to_json())