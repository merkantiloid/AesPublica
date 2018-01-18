from app import esiclient, db, esisecurity, esiapp

class EsiService:

    def __init__(self, char):
        self.char=char

    def _update_token(self):
        self.char.access_token = esisecurity.access_token
        self.char.access_expiration = esisecurity.token_expiry
        db.session.add(self.char)
        db.session.commit()

    def character_skills(self):
        esisecurity.update_token(self.char.get_sso_data())
        op = esiapp.op['get_characters_character_id_skills'](character_id=self.char.character_id)
        data = esiclient.request(op).data
        self._update_token()
        return data


    def character_search(self, categories, term):
        esisecurity.update_token(self.char.get_sso_data())
        op = esiapp.op['get_characters_character_id_search'](character_id=self.char.character_id, categories=categories, search=term)
        data = esiclient.request(op).data
        self._update_token()
        return data

    def universe_names(self, ids):
        op = esiapp.op['post_universe_names'](ids=ids)
        data = esiclient.request(op).data
        return data

    def universe_structures(self, id):
        esisecurity.update_token(self.char.get_sso_data())
        op = esiapp.op['get_universe_structures_structure_id'](structure_id=id)
        data = esiclient.request(op).data
        self._update_token()
        return data