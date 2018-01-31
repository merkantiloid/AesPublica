from app.models import MoonMat, MoonMatRig, MoonMatItem
from app import db
from .static import Static
from .parsing import parse_name_qty
from math import ceil


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
            materials = Static.materials_by_reaction_pid(item['type_id'])
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

    def materials(self):

        result = []

        for item in self.user.moon_mat.items:

            materials = Static.materials_by_reaction_pid(item.type_id)
            if materials:
                k = ceil(item.qty / materials['qty'])

                result.append({
                    'type': Static.type_by_id(item.type_id),
                    'qty': item.qty,
                    'k': k,
                    'iqty': materials['qty'],
                    'level': 0,
                })

                self.add_materials(result, 1, k, materials)

        hash = {}
        for r in result:
            if r.get('leaf',False):
                hash[r['type']['id']] = hash.get(r['type']['id'], 0) + r['iqty']*r['k']

        total = []
        for x in hash:
            total.append({
                'type': Static.type_by_id(x),
                'qty': hash[x]
            })
        total.sort(key=lambda r: r['type']['name'])

        return result, total

    def add_materials(self, result, level, k, materials):
        parts = []
        input = materials['input']
        for mid in input:
            parts.append({
                'type': Static.type_by_id(mid),
                'qty': k * input[mid],
                'iqty': input[mid],
            })
        parts.sort(key=lambda r: r['type']['name'])
        for p in parts:
            sub_materials = Static.materials_by_reaction_pid(p['type']['id'])

            temp = {
                'type': p['type'],
                'qty': p['qty'],
                'k': k,
                'iqty': p['iqty'],
                'level': level,
                'leaf': False if sub_materials else True,
            }
            result.append(temp)

            if sub_materials:
                sub_k = ceil(p['qty'] / sub_materials['qty'])
                self.add_materials(result, level+1, sub_k, sub_materials)



    def to_json(self):
        model = self.user.moon_mat

        materials, totals = self.materials()

        return {
            "spaces": Static.RSPACES,
            "rigs": Static.RRIGS,
            "settings": {
                "space": model.space,
                "rigs": [x.to_json() for x in model.rigs],
            },
            "raw": model.raw,
            "items": [x.to_json() for x in model.items],
            "materials": materials,
            "totals": totals,
        }

