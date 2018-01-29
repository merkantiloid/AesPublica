from app.models import MoonMat, MoonMatRig, MoonMatItem
from app import db
from .static import Static
from .parsing import parse_name_qty


class MoonMatService:

    def __init__(self, user):
        self.user = user
        if not self.user.moon_mat:
            temp = MoonMat(
                user=self.user,
                space="z"
            )
            db.session.add(temp)
            db.session.commit()

    def add_rig(self, rig_id):
        model = self.user.moon_mat
        temp = MoonMatRig.query.filter(MoonMatRig.moon_mat_id==model.id, MoonMatRig.rig_id==rig_id).first()
        if not temp:
            temp = MoonMatRig(moon_mat_id=model.id, rig_id=rig_id)
            db.session.add(temp)
            db.session.commit()

    def delete_rig(self, rig_id):
        model = self.user.moon_mat
        temp = MoonMatRig.query.filter(MoonMatRig.moon_mat_id==model.id, MoonMatRig.rig_id==rig_id).first()
        if temp:
            db.session.delete(temp)
            db.session.commit()


    def update(self, params):
        model = self.user.moon_mat
        if 'raw' in params:
            model.raw = params.get('raw',None)
        db.session.add(model)
        db.session.commit()

    def parse(self):
        model = self.user.moon_mat
        items = parse_name_qty(model.raw)
        ids = []
        for item in items:
            materials = Static.materials_by_reaction_id(item['type_id'])
            if materials:
                ids.append( item['type_id'] )
                db_item = MoonMatItem.query.filter(MoonMatItem.moon_mat_id == model.id, MoonMatItem.type_id == item['type_id']).first()
                if not db_item:
                    db_item = MoonMatItem(moon_mat_id = model.id, type_id = item['type_id'])
                db_item.qty = item['qty']
                db.session.add(db_item)
        if len(ids) == 0:
            db.session.execute('delete from moon_mat_items where moon_mat_id = :id',  params={'id': model.id} )
        else:
            db.session.execute('delete from moon_mat_items where moon_mat_id = :id and type_id not in :ids',  params={'id': model.id, 'ids': ids} )
        db.session.commit()



    def to_json(self):
        model = self.user.moon_mat

        return {
            "spaces": Static.RSPACES,
            "rigs": Static.RRIGS,
            "settings": {
                "space": model.space,
                "rigs": [x.to_json() for x in model.rigs],
            },
            "raw": model.raw,
            "items": [x.to_json() for x in model.items],
        }

