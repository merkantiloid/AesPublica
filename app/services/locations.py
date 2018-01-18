from app.esi_models import EsiLocation
from app.services import EsiService
from app import db

class LocationsService:

    def __init__(self, char):
        self.char = char

    def station_names(self, ids):
        result = []

        if len(ids)>0:
            with_names = EsiLocation.query.filter(EsiLocation.id.in_(ids)).all()
            for l in with_names:
                result.append({'id': l.id, 'name': l.name, 'category': l.category})
                ids.remove(l.id)

            if len(ids)>0:
                data = EsiService(self.char).universe_names(ids)
                for st in data:
                    result.append({'id': st['id'], 'name': st['name'], 'category': st['category']})
                    temp = EsiLocation(id=st['id'], name=st['name'], category=st['category'])
                    db.session.add(temp)
                db.session.commit()

        return result