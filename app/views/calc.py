from app import mainApp
from flask import render_template, jsonify, g
from flask_login import login_required
from app.services import OreCalcService, Static, SearchService
from app.forms import SettingsForm


@mainApp.route('/')
@mainApp.route('/calc')
@login_required
def calc():
    return render_template('calc.html', title='Calc', static=Static.to_json())


@mainApp.route('/calc/data.json')
@login_required
def calc_json():
    s = OreCalcService(g.user)
    return jsonify(s.to_json())


@mainApp.route('/calc/save_settings', methods=['POST'])
@login_required
def save_settings():
    form = SettingsForm()
    form.save(g.user)
    s = OreCalcService(g.user)
    return jsonify(s.to_json())


@mainApp.route('/calc/search_blueprint')
@login_required
def search_blueprint():
    s = SearchService("type")
    s.search("rhea")
    return jsonify(s.to_json())
