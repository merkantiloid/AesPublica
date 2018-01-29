from app import mainApp
from flask import render_template, jsonify, g, request
from flask_login import login_required
from app.services import MoonMatService
from app.esi_models import EsiChar

import json

@mainApp.route('/moonmat')
@login_required
def moonmat():
    return render_template(
        'moonmat/index.html',
        title='Moon Materials'
    )

@mainApp.route('/moonmat/data.json')
@login_required
def moonmat_json():
    s = MoonMatService(g.user)
    return jsonify(s.to_json())

@mainApp.route('/moonmat/rigs.json', methods=['POST'])
@login_required
def add_rigs_json():
    s = MoonMatService(g.user)
    s.add_rig(request.get_json()['rig_id'])
    return jsonify(s.to_json())

@mainApp.route('/moonmat/rigs/<int:rig_id>.json', methods=['DELETE'])
@login_required
def delete_rigs_json(rig_id):
    s = MoonMatService(g.user)
    s.delete_rig(rig_id)
    return jsonify(s.to_json())