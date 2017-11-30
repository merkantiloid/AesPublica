from app.models import OreCalc, BuildItem, StoreItem, Price, CalcResult
from .static import Static, ReprocessByTypeId, TypeById
from app import db
from .loaders import load_chars
from .parsing import parse_name_qty
from .components import ComponentsService
from .reprocess import ReprocessService
from .optimize import OptimizeService
from .price import PriceService
from math import ceil


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
        rservice = ReprocessService(model)

        reprocessed = rservice.reprocess_store(only_ore=True)
        after_refine = rservice.reprocess_result()
        minerals = ComponentsService(model).only_minerals(reprocessed, after_refine)

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
            'minerals': minerals,
            "store_items_text": model.store_items_text,
            "store_items": [x.to_json() for x in model.store_items],
            "ore_settings": model.checked_ores(),
            "calc_results": [x.to_json() for x in model.calc_results],
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

    def save_ore_settings(self, text):
        ore_calc = self.user.ore_calc
        ore_calc.ore_settings = text
        db.session.add(ore_calc)
        db.session.commit()


    def calc_result(self):
        model = self.user.ore_calc
        service = ReprocessService(model)
        reprocessed = service.reprocess_store(only_ore=True)
        goal_minerals = ComponentsService(model).only_minerals(reprocessed)

        ordered_minerals = []
        minerals = []
        for goal_mineral in goal_minerals:
            if goal_mineral['need_qty']>0:
                ordered_minerals.append(goal_mineral['type_id'])
                minerals.append(goal_mineral['need_qty'])

        ordered_ores = model.checked_ores()

        PriceService().esi(ordered_ores)

        ores = []
        ore_prices = []
        for ore_id in ordered_ores:
            ore = []
            for mineral_id in ordered_minerals:
                if mineral_id in ReprocessByTypeId[ore_id]:
                    rqty = service.reprocess_ore(ore_id, TypeById[ore_id].portion_size, mineral_id)
                    ore.append(rqty)
                else:
                    ore.append(0)
            ores.append(ore)

            price = Price.query.filter(Price.source=='esi', Price.type_id==ore_id).one()
            ore_prices.append(price.value)

        # print('minerals')
        # print(minerals)
        #
        # print('ores')
        # for index, d in enumerate(ores):
        #   print(TypeById[ordered_ores[index]].name, d)
        #
        # print('ore_prices')
        # print(ore_prices)

        result_ores = OptimizeService().calc(minerals=minerals, ores=ores, ore_prices=ore_prices)
        db.session.execute('delete from calc_results where ore_calc_id = :id',  params={'id': model.id} )
        for index, x in enumerate(result_ores):
            if x>0:
                # print( TypeById[ordered_ores[index]].name, x, ceil(x)*TypeById[ordered_ores[index]].portion_size )
                ore_id = ordered_ores[index]
                calc_result = CalcResult(ore_calc_id=model.id, type_id=ore_id, qty=ceil(x)*TypeById[ore_id].portion_size)
                db.session.add(calc_result)
        db.session.commit()