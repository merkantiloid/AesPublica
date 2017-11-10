from app import mainApp, preston, db
from app.esi_models import EsiChar, EsiSkill
from flask import render_template, request, redirect, g
from flask_login import login_required


@mainApp.route('/characters')
@login_required
def characters():
    characters = EsiChar.query.all()
    return render_template('characters.html', title='Characters', url=preston.get_authorize_url(), characters=characters)


@mainApp.route('/characters/<int:cid>/update_skills')
@login_required
def update_skills(cid):
    char = EsiChar.query.filter(EsiChar.user_id==g.user.id, EsiChar.character_id==cid).first()
    if char:
        auth = preston.use_saved(char.refresh_token, char.access_token, char.access_expiration)
        skills = auth.characters[cid].skills()['skills']
        ids = []
        for skill in skills:
            model = EsiSkill.query.filter(EsiSkill.esi_char_id == char.id, EsiSkill.skill_id == skill['skill_id']).first()
            if not model:
                model = EsiSkill(esi_char_id = char.id, skill_id = skill['skill_id'])
            model.skillpoints_in_skill = skill['skillpoints_in_skill']
            model.current_skill_level = skill['current_skill_level']
            db.session.add(model)
            db.session.commit()
            ids.append(model.skill_id)
        db.session.execute('delete from esi_skills where esi_char_id = :id and skill_id not in :ids',  params={'id': char.id, 'ids': ids} )
        db.session.commit()

    return redirect('/characters')


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
    char.scopes = response['Scopes']
    char.token_type = response['TokenType']
    char.access_expiration = auth.access_expiration
    char.refresh_token = auth.refresh_token
    char.access_token = auth.access_token

    db.session.add(char)
    db.session.commit()

    return redirect('/characters')