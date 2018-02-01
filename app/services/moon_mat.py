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

    def get_max_bonus(self, type_id):
        model = self.user.moon_mat

        mbonus = 0
        tbonus = 0
        bid = Static.bid_by_pid(type_id)
        type_group_id = Static.type_by_id(bid).group_id

        for rig in model.rigs:
            rig_info = Static.RRIGS_HASH[rig.rig_id]
            rig_mbonus = rig_info['mat_bonus']*rig_info[model.space]
            m_applicable = rig_info['group_id'] in Static.RIG_APPLY['materials'].get(type_group_id,[])
            if m_applicable and mbonus > rig_mbonus:
                mbonus = rig_mbonus

            rig_tbonus = rig_info['time_bonus']*rig_info[model.space]
            t_applicable = rig_info['group_id'] in Static.RIG_APPLY['time'].get(type_group_id,[])
            if t_applicable and tbonus > rig_tbonus:
                tbonus = rig_tbonus

        return mbonus, tbonus

    def materials(self):
        model = self.user.moon_mat
        result = []

        for item in model.items:
            mbonus, tbonus = self.get_max_bonus(item.type_id)

            materials = Static.materials_by_reaction_pid(item.type_id)
            if materials:
                k = ceil(item.qty / materials['qty'])

                result.append({
                    'type': Static.type_by_id(item.type_id),
                    'initial': item.qty,
                    'qty': materials['qty']*k,
                    'k': k,
                    'iqty': materials['qty'],
                    'level': 0,
                })

                self.add_materials(result, 1, k, materials, mbonus, tbonus)

        hash = {}
        for r in result:
            if r.get('leaf',False):
                hash[r['type']['id']] = hash.get(r['type']['id'], 0) + r['qty']

        total = []
        for x in hash:
            total.append({
                'type': Static.type_by_id(x),
                'qty': hash[x]
            })
        total.sort(key=lambda r: r['type']['name'])

        return result, total

    def add_materials(self, result, level, k, materials, mbonus, tbonus):
        parts = []
        input = materials['input']
        for mid in input:
            parts.append({
                'type': Static.type_by_id(mid),
                'iqty': input[mid],
            })
        parts.sort(key=lambda r: r['type']['name'])

        for p in parts:
            sub_materials = Static.materials_by_reaction_pid(p['type']['id'])

            temp = {
                'type': p['type'],
                'qty': ceil(p['iqty']*k*(1+mbonus/100)),
                'k': k,
                'iqty': p['iqty'],
                'mbonus': mbonus,
                'level': level,
                'leaf': False if sub_materials else True,
            }
            result.append(temp)

            if sub_materials:
                sub_mbonus, sub_tbonus = self.get_max_bonus(p['type']['id'])
                sub_k = ceil(temp['qty'] / sub_materials['qty'])
                self.add_materials(result, level+1, sub_k, sub_materials, sub_mbonus, sub_tbonus)



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

