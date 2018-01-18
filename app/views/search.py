from app import mainApp, esiclient
from flask import request, jsonify
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

    char = EsiChar.query.filter(EsiChar.id==char_id).first()

    if char:
        ids = EsiService(char).character_search('station,structure',term)

        sids = ids.get('station',[])
        if len(sids)>0:
            names = LocationsService(char).station_names(sids)
            print('stations', names)


    return jsonify({})