from app.models import OreCalc, BuildItem, StoreItem
from .static import Static
from app import db
from .loaders import load_chars
from .parsing import parse_name_qty
from .components import ComponentsService
from .reprocess import ReprocessService

class OreCalcService:

    def __init__(self, user):
        self.user = user
        if not self.user.ore_calc:
            temp = OreCalc(
                user=self.user,
                space=Static.DEFAULT_SPACE,
                citadel_id=Static.DEFAULT_CITADEL,
                implant_id= -1,
                rig1_id= -1,
            )
            db.session.add(temp)
            db.session.commit()

        self.characters = load_chars(user.id)

    def to_json(self):
        model = self.user.ore_calc

        ReprocessService(model).reprocess()

        return {
            "settings": {
                "space": model.space,
                "citadel_id": model.citadel_id,
                "characters": self.characters,
                "esi_char_id": model.esi_char_id,
                "implant_id": model.implant_id,
                "rig1_id": model.rig1_id,
                "rig2_id": model.rig2_id,
                "rig3_id": model.rig3_id,
            },
            "build_items_text": model.build_items_text,
            "build_items": [x.to_json() for x in model.build_items],
            'minerals': ComponentsService(model).only_minerals(),
            "store_items_text": model.store_items_text,
            "store_items": [x.to_json() for x in model.store_items],
        }


    def add_build_item(self, text):
        items = parse_name_qty(text)
        ids = []
        ore_calc = self.user.ore_calc
        for item in items:
            ids.append( item['type_id'] )
            model = BuildItem.query.filter(BuildItem.ore_calc_id == ore_calc.id, BuildItem.type_id == item['type_id']).first()
            if not model:
                model = BuildItem(ore_calc_id = ore_calc.id, type_id = item['type_id'])
            model.qty = item['qty']
            model.me = item['me']
            model.te = item['te']
            db.session.add(model)

        if len(ids) == 0:
            db.session.execute('delete from build_items where ore_calc_id = :id',  params={'id': ore_calc.id} )
        else:
            db.session.execute('delete from build_items where ore_calc_id = :id and type_id not in :ids',  params={'id': ore_calc.id, 'ids': ids} )

        ore_calc.build_items_text = text
        db.session.add(ore_calc)

        db.session.commit()


    def add_store_item(self, text):
        items = parse_name_qty(text)
        ids = []
        ore_calc = self.user.ore_calc
        for item in items:
            ids.append( item['type_id'] )
            model = StoreItem.query.filter(StoreItem.ore_calc_id == ore_calc.id, StoreItem.type_id == item['type_id']).first()
            if not model:
                model = StoreItem(ore_calc_id = ore_calc.id, type_id = item['type_id'])
            model.qty = item['qty']
            db.session.add(model)

        if len(ids) == 0:
            db.session.execute('delete from store_items where ore_calc_id = :id',  params={'id': ore_calc.id} )
        else:
            db.session.execute('delete from store_items where ore_calc_id = :id and type_id not in :ids',  params={'id': ore_calc.id, 'ids': ids} )

        ore_calc.store_items_text = text
        db.session.add(ore_calc)

        db.session.commit()

