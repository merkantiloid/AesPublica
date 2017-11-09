from app import mainApp, preston, db
from app.esi_models import EsiChar
from flask import render_template, request, redirect, g
from flask_login import login_required


@mainApp.route('/characters')
@login_required
def characters():
    characters = EsiChar.query.all()
    return render_template('characters.html', title='Characters', url=preston.get_authorize_url(), characters = characters)


@mainApp.route('/probleme_callback')
@login_required
def probleme_callback():
    code = request.args.get('code', '')
    auth = preston.authenticate(code)

    response = auth.whoami()

    char = EsiChar.query.filter(EsiChar.user_id==g.user.id, EsiChar.character_id==response['CharacterID']).first()
    if not char:
        char = EsiChar(user_id=g.user.id, character_id=response['CharacterID'])
    char.character_name = response['CharacterName']
    char.expires_on = response['ExpiresOn']
    char.scopes = response['Scopes']
    char.token_type = response['TokenType']
    char.refresh_token = auth.refresh_token
    char.code = code

    db.session.add(char)
    db.session.commit()

    return redirect('/characters')