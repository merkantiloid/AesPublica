from app import mainApp, esiclient
from flask import request, jsonify, g
from flask_login import login_required
from app.services import SearchService, EsiService, LocationsService
from app.esi_models import EsiChar


@mainApp.route('/search/type')
@login_required
def search_type():
    s = SearchService("type")
    s.search(request.args.get('term', ''))
    return jsonify(s.to_json())


@mainApp.route('/search/location')
@login_required
def search_location():
    term = request.args.get('term', '')
    char_id = request.args.get('char_id', 0)

    char = EsiChar.query.filter(EsiChar.user_id==g.user.id, EsiChar.id==char_id).first()

    if char:
        result = LocationsService(char).search_location(term)
        return jsonify(result)
    else:
        return jsonify([])