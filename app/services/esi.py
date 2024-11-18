from esipy import EsiClient, EsiSecurity, EsiApp
from app.extensions import db


class EsiService:

    def __init__(self, char=None):
        self.char = char

    def _update_token(self):
        self.char.access_token = EsiSecurity.access_token
        self.char.access_expiration = EsiSecurity.token_expiry
        db.session.add(self.char)
        db.session.commit()

    def character_skills(self):
        EsiSecurity.update_token(self.char.get_sso_data())
        op = EsiApp.op['get_characters_character_id_skills'](character_id=self.char.character_id)
        data = EsiClient.request(op).data
        self._update_token()
        return data

    def character_search(self, categories, term):
        EsiSecurity.update_token(self.char.get_sso_data())
        op = EsiApp.op['get_characters_character_id_search'](character_id=self.char.character_id, categories=categories,
                                                             search=term)
        data = EsiClient.request(op).data
        self._update_token()
        return data

    def universe_names(self, ids):
        op = EsiApp.op['post_universe_names'](ids=ids)
        data = EsiClient.request(op).data
        return data

    def universe_systems(self, id):
        op = EsiApp.op['get_universe_systems_system_id'](system_id=id)
        data = EsiClient.request(op).data
        return data

    def universe_constellations(self, id):
        op = EsiApp.op['get_universe_constellations_constellation_id'](constellation_id=id)
        data = EsiClient.request(op).data
        return data

    def universe_stations(self, id):
        op = EsiApp.op['get_universe_stations_station_id'](station_id=id)
        data = EsiClient.request(op).data
        return data

    def universe_structures(self, id):
        EsiSecurity.update_token(self.char.get_sso_data())
        op = EsiApp.op['get_universe_structures_structure_id'](structure_id=id)
        data = EsiClient.request(op).data
        self._update_token()
        return data

    def markets_orders(self, region_id, type_id, kind, page):
        op = EsiApp.op['get_markets_region_id_orders'](region_id=region_id, order_type=kind, page=page, type_id=type_id)
        req = EsiClient.request(op)
        data = req.data
        pages = req.header.get('X-Pages', [1])[0]
        return data, pages

    def markets_structures(self, structure_id, page):
        EsiSecurity.update_token(self.char.get_sso_data())
        op = EsiApp.op['get_markets_structures_structure_id'](structure_id=structure_id, page=page)
        req = EsiClient.request(op)
        data = req.data
        pages = req.header.get('X-Pages', [1])[0]
        self._update_token()
        return data, pages

    def characters_assets(self, page):
        EsiSecurity.update_token(self.char.get_sso_data())
        op = EsiApp.op['get_characters_character_id_assets'](character_id=self.char.character_id, page=page)
        req = EsiClient.request(op)
        if req.status == 200:
            data = req.data
            pages = req.header.get('X-Pages', [1])[0]
            self._update_token()
            return data, pages
        else:
            print(req.data)
            return [], 1

    def _deep_set_rid(self, hash, current_id):
        if hash[current_id]['location_id'] in hash:
            hash[current_id]['rid'] = self._deep_set_rid(hash, hash[current_id]['location_id'])
        else:
            hash[current_id]['rid'] = hash[current_id]['location_id']
            return hash[current_id]['rid']

    def characters_assets_full(self):
        current = 1
        max_page = None
        hash_assets = {}
        while True:
            assets, pages = self.characters_assets(current)
            for asset in assets:
                hash_assets[asset['item_id']] = asset
            if not max_page:
                max_page = pages
            current += 1
            if current > max_page:
                break

        for asset_id in hash_assets:
            if not 'rid' in hash_assets[asset_id]:
                self._deep_set_rid(hash_assets, asset_id)

        return hash_assets
