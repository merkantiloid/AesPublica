from app import mainApp, preston
from flask import request, jsonify
from flask_login import login_required
from app.services import SearchService
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
        auth = preston.use_saved(char.refresh_token, char.access_token, char.access_expiration)
        ids = auth.characters[char.character_id].search(categories='station,structure', search=term)
        print(ids)

    return jsonify({})