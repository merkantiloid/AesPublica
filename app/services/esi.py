from app import esiclient, db, esisecurity, esiapp

class EsiService:

    def __init__(self, char=None):
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

    def universe_systems(self, id):
        op = esiapp.op['get_universe_systems_system_id'](system_id=id)
        data = esiclient.request(op).data
        return data

    def universe_constellations(self, id):
        op = esiapp.op['get_universe_constellations_constellation_id'](constellation_id=id)
        data = esiclient.request(op).data
        return data


    def universe_stations(self, id):
        op = esiapp.op['get_universe_stations_station_id'](station_id=id)
        data = esiclient.request(op).data
        return data

    def universe_structures(self, id):
        esisecurity.update_token(self.char.get_sso_data())
        op = esiapp.op['get_universe_structures_structure_id'](structure_id=id)
        data = esiclient.request(op).data
        self._update_token()
        return data

    def markets_orders(self, region_id, type_id, kind, page):
        op = esiapp.op['get_markets_region_id_orders'](region_id=region_id, order_type=kind, page=page, type_id=type_id)
        req = esiclient.request(op)
        data = req.data
        pages = req.header.get('X-Pages',[1])[0]
        return data, pages

    def markets_structures(self, structure_id, page):
        esisecurity.update_token(self.char.get_sso_data())
        op = esiapp.op['get_markets_structures_structure_id'](structure_id=structure_id, page=page)
        req = esiclient.request(op)
        data = req.data
        pages = req.header.get('X-Pages',[1])[0]
        self._update_token()
        return data, pages