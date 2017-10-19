from app import mainApp
from flask import render_template, jsonify
from flask_login import login_required

@mainApp.route('/')
@mainApp.route('/calc')
@login_required
def index():
    return render_template('index.html', title='Calc')

@mainApp.route('/calc/data.json')
@login_required
def calc_json():
    return jsonify({"test": 123})