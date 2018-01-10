from app.models import MScan, MScanItem
from app.esi_models import EsiChar
from app import db
from .parsing import parse_name_qty
from .static import Static
from .price import PriceService


class MScanService:

    def __init__(self, user):
        self.user=user

    def list(self):
        mscans=MScan.query.filter(MScan.user_id == self.user.id).order_by(MScan.name).all()
        result = []
        for scan in mscans:
            result.append(scan.short_json())
        return result

    def add_scan(self, name):
        if bool(name.strip()):
            temp = MScan(
                name=name,
                user_id=self.user.id,
                fit_times=10
            )
            db.session.add(temp)
            db.session.commit()
            return temp.id
        return None

    def rename_scan(self, id, name):
        temp = MScan.query.filter(MScan.user_id == self.user.id, MScan.id == id).first()
        if temp and bool(name.strip()):
            temp.name = name
            db.session.add(temp)
            db.session.commit()

    def delete_scan(self, id):
        temp = MScan.query.filter(MScan.user_id == self.user.id, MScan.id == id).first()
        if temp:
            db.session.delete(temp)
            db.session.commit()

    def update_mscan(self, mscan_id, params):
        temp = MScan.query.filter(MScan.user_id == self.user.id, MScan.id == mscan_id).first()
        if temp:
            temp.raw = params.get('raw',None)
            db.session.add(temp)
            db.session.commit()
            self.parse_raw(temp)

    def to_json(self, selected_id=None):
        selected = None
        if selected_id:
            temp = MScan.query.filter(MScan.user_id == self.user.id, MScan.id == selected_id).first()
            if temp:
                selected = temp.to_json()
                ids = [x['type']['id'] for x in selected['items']]
                ps = PriceService()
                ps.evemarketer(type_ids=ids)
                for x in selected['items']:
                    x['price'] = ps.jita('evemarketer', x['type']['id'])
                    x['need_qty'] = x['qty'] * temp.fit_times
        return {
            'list': self.list(),
            'selected': selected
        }

    def parse_raw(self, mscan):
        items = parse_name_qty(mscan.raw)

        ids = [x['type_id'] for x in items]
        if len(ids) == 0:
            db.session.execute('delete from mscan_items where mscan_id = :id',  params={'id': mscan.id} )
        else:
            db.session.execute('delete from mscan_items where mscan_id = :id and type_id not in :ids',  params={'id': mscan.id, 'ids': ids} )

        for item in items:
            db_item = MScanItem.query.filter(MScanItem.mscan_id==mscan.id, MScanItem.type_id==item['type_id']).first()
            if not db_item:
                db_item = MScanItem(mscan_id=mscan.id, type_id=item['type_id'])
            db_item.qty = item['qty']
            db.session.add(db_item)
        db.session.commit()

