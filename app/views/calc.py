# from app import mainApp
from flask import Blueprint, render_template, jsonify, g, request
from flask_login import login_required
from app.services import OreCalcService, Static
from app.forms import SettingsForm
import json


calc_bp = Blueprint('calc', __name__)  # Создаем Blueprint для калькулятора


@calc_bp.route('/')
@calc_bp.route('/calc')
@login_required
def calc():
    return render_template(
        'calc/index.html',
        title='Calc',
        static=json.dumps(Static.to_json()),
    )


@calc_bp.route('/calc/data.json')
@login_required
def calc_json():
    s = OreCalcService(g.user)
    return jsonify(s.to_json())


@calc_bp.route('/calc/save_settings', methods=['POST'])
@login_required
def save_settings():
    form = SettingsForm()
    form.save(g.user)
    s = OreCalcService(g.user)
    return jsonify(s.to_json())


@calc_bp.route('/calc/build_items_text', methods=['POST'])
@login_required
def build_items_add():
    s = OreCalcService(g.user)
    s.add_build_item(request.get_json()['text'])

    return jsonify(s.to_json())


@calc_bp.route('/calc/store_items_text', methods=['POST'])
@login_required
def store_items_add():
    s = OreCalcService(g.user)
    s.add_store_item(request.get_json()['text'])

    return jsonify(s.to_json())


@calc_bp.route('/calc/save_ore_settings', methods=['POST'])
@login_required
def save_ore_settings():
    s = OreCalcService(g.user)
    s.save_ore_settings(request.get_json()['text'])

    return jsonify(s.to_json())


@calc_bp.route('/calc/result.json', methods=['GET'])
@login_required
def calc_result_json():
    s = OreCalcService(g.user)
    s.calc_result()

    return jsonify(s.to_json())
