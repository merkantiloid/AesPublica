from app.esi_models import EsiLocation
from .esi import EsiService
from app import db


class LocationsService:

    def __init__(self, char=None):
        self.char = char
        self.esi = EsiService(self.char)

    def search_location(self, term):
        result = []

        ids = self.esi.character_search('station,structure', term)

        sids = ids.get('station', [])
        if len(sids) > 0:
            names = self.station_names(sids)
            result = result + names

        cids = ids.get('structure', [])
        if len(cids) > 0:
            names = self.citadel_names(cids)
            result = result + names

        return result

    def station_names(self, ids):
        result = []

        if len(ids) > 0:
            with_names = EsiLocation.query.filter(EsiLocation.id.in_(ids)).all()
            for l in with_names:
                result.append({'id': l.id, 'name': l.name, 'category': l.category})
                ids.remove(l.id)

            if len(ids) > 0:
                data = self.esi.universe_names(ids)
                for st in data:
                    result.append({'id': st['id'], 'name': st['name'], 'category': st['category']})
                    temp = EsiLocation(id=st['id'], name=st['name'], category=st['category'])
                    db.session.add(temp)
                db.session.commit()

        return result

    def citadel_names(self, ids):
        result = []

        if len(ids) > 0:
            with_names = EsiLocation.query.filter(EsiLocation.id.in_(ids)).all()
            for l in with_names:
                result.append({'id': l.id, 'name': l.name, 'category': l.category})
                ids.remove(l.id)

            if len(ids) > 0:
                for id in ids:
                    st = self.esi.universe_structures(id)
                    if 'error' in st:
                        print(st['error'])
                    else:
                        result.append({'id': id, 'name': st['name'], 'category': 'citadel'})
                        temp = EsiLocation(id=id, name=st['name'], category='citadel')
                        db.session.add(temp)
                db.session.commit()

        return result

    def update_region_id(self, location, system_id):
        sys_data = self.esi.universe_systems(system_id)
        con_data = self.esi.universe_constellations(sys_data["constellation_id"])
        location.system_id = system_id
        location.region_id = con_data["region_id"]
        db.session.add(location)
        db.session.commit()
        return location.region_id
