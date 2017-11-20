from app import mainApp
from flask import render_template, jsonify, g, request
from flask_login import login_required
from app.services import OreCalcService, Static
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


@mainApp.route('/calc/build_items_text', methods=['POST'])
@login_required
def build_items_add():
    s = OreCalcService(g.user)
    s.add_build_item(request.get_json()['text'])

    return jsonify(s.to_json())


@mainApp.route('/calc/store_items_text', methods=['POST'])
@login_required
def store_items_add():
    s = OreCalcService(g.user)
    s.add_store_item(request.get_json()['text'])

    return jsonify(s.to_json())
