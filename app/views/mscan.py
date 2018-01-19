from app import mainApp
from flask import render_template, jsonify, g, request
from flask_login import login_required
from app.services import MScanService
from app.esi_models import EsiChar

import json

@mainApp.route('/mscan')
@login_required
def mscan():
    chars = EsiChar.query.filter(EsiChar.user_id == g.user.id).all()
    return render_template(
        'mscan/index.html',
        title='Fit on Market',
        chars=chars,
    )

@mainApp.route('/mscans.json', methods=['GET'])
@login_required
def mscans_list():
    s = MScanService(g.user)
    return jsonify(s.to_json())


@mainApp.route('/mscans.json', methods=['POST'])
@login_required
def add_mscan():
    s = MScanService(g.user)
    new_id = s.add_scan(request.get_json()['name'])
    return jsonify(s.to_json(selected_id=new_id))


@mainApp.route('/mscans/<int:mscan_id>/rename.json', methods=['POST'])
@login_required
def rename_mscan(mscan_id):
    s = MScanService(g.user)
    s.rename_scan(mscan_id, request.get_json()['name'])
    return jsonify(s.to_json())


@mainApp.route('/mscans/<int:mscan_id>/delete.json', methods=['POST'])
@login_required
def delete_mscan(mscan_id):
    s = MScanService(g.user)
    s.delete_scan(mscan_id)
    return jsonify(s.to_json())


@mainApp.route('/mscans/<int:mscan_id>.json', methods=['GET'])
@login_required
def mscan_json(mscan_id):
    s = MScanService(g.user)
    return jsonify(s.to_json(selected_id=mscan_id))


@mainApp.route('/mscans/<int:mscan_id>.json', methods=['POST'])
@login_required
def update_mscan_json(mscan_id):
    s = MScanService(g.user)
    s.update_mscan(mscan_id, request.get_json())
    return jsonify(s.to_json(selected_id=mscan_id))


@mainApp.route('/mscans/<int:mscan_id>/locations.json', methods=['POST'])
@login_required
def add_mscan_location_json(mscan_id):
    s = MScanService(g.user)
    s.add_location(mscan_id, request.get_json())
    return jsonify(s.to_json(selected_id=mscan_id))


@mainApp.route('/mscans/<int:mscan_id>/locations/<int:loc_id>.json', methods=['DELETE'])
@login_required
def delete_mscan_location_json(mscan_id,loc_id):
    s = MScanService(g.user)
    s.delete_location(mscan_id, loc_id)
    return jsonify(s.to_json(selected_id=mscan_id))


@mainApp.route('/mscans/<int:mscan_id>/market_info.json', methods=['POST'])
@login_required
def market_info_json(mscan_id):
    s = MScanService(g.user)
    s.market_info(mscan_id)
    return jsonify(s.to_json(selected_id=mscan_id))