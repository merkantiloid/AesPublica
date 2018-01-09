from app import mainApp
from flask import render_template, jsonify, g, request
from flask_login import login_required
from app.services import MScanService
from app.forms import SettingsForm
from app.esi_models import EsiChar

import json

@mainApp.route('/mscan')
@login_required
def mscan():

    chars = EsiChar.query.filter(EsiChar.user_id == g.user.id).all()

    return render_template(
        'mscan/index.html',
        title='Fit on Market',
        characters=chars,
    )



@mainApp.route('/mscans.json')
@login_required
def list():
    s = MScanService(g.user)
    return jsonify(s.list())

