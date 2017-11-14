from app import mainApp
from flask import request, jsonify
from flask_login import login_required
from app.services import SearchService

@mainApp.route('/search/type')
@login_required
def search_type():
    s = SearchService("type")
    s.search(request.args.get('term', ''))
    return jsonify(s.to_json())