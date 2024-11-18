from app.services.static import AllOres, ReprImplantsHash, ReprRigsHash, Static
from app.esi_models import EsiSkill
import math


class ReprocessService:

    def __init__(self, ore_calc):
        self.ore_calc = ore_calc

        self.base_scrap = 0.5

        self.base_ore = 0
        for rid in [self.ore_calc.rig1_id, self.ore_calc.rig2_id, self.ore_calc.rig3_id]:
            rig = ReprRigsHash[rid]['value']
            space = ReprRigsHash[rid][self.ore_calc.space]
            bonus = 1 + Static.CITADELS_HASH[self.ore_calc.citadel_id]['bonus'] / 100.0

            if self.base_ore < rig * space * bonus:
                self.base_ore = rig * space * bonus

        self.implant = ReprImplantsHash[self.ore_calc.implant_id]['value']

        self.skills = {}
        for s in EsiSkill.query.filter(EsiSkill.esi_char_id == self.ore_calc.esi_char_id).all():
            self.skills[s.skill_id] = s.current_skill_level

        self.skill_metallurgy = self.skills.get(12196, (5 if self.ore_calc.esi_char_id == -1 else 0))
        self.repr = self.skills.get(3385, (5 if self.ore_calc.esi_char_id == -1 else 0))
        self.repr_eff = self.skills.get(3389, (5 if self.ore_calc.esi_char_id == -1 else 0))

    def reprocess_ore(self, ore_id, qty, mineral_id):
        chunks = math.floor(qty / Static.type_by_id(ore_id).portion_size)
        ore_skill_id = AllOres[ore_id]['skill_id']
        ore_skill = self.skills.get(ore_skill_id, (5 if self.ore_calc.esi_char_id == -1 else 0))
        reprocessed = Static.reprocess_by_id(ore_id)

        return math.floor(
            reprocessed[mineral_id] *
            chunks *
            self.base_ore *
            (1 + self.implant / 100) *
            (1 + 3 * self.repr / 100) *
            (1 + 2 * self.repr_eff / 100) *
            (1 + 2 * ore_skill / 100)
        )

    def reprocess_result(self):
        return self.reprocess(self.ore_calc.calc_results, True, False)

    def reprocess_store(self, only_ore=False, deep=True):
        return self.reprocess(self.ore_calc.store_items, only_ore, deep)

    def reprocess(self, items, only_ore, deep):
        result = {}
        process = {}
        queue = {}

        for item in items:
            queue[item.type_id] = queue.get(item.type_id, 0) + item.qty

        while True:

            for store_type_id in queue:
                reprocessed = Static.reprocess_by_id(store_type_id)

                if store_type_id in AllOres:
                    for part_id in reprocessed:
                        qty = self.reprocess_ore(store_type_id, queue[store_type_id], part_id)
                        if deep:
                            process[part_id] = process.get(part_id, 0) + qty
                        else:
                            result[part_id] = result.get(part_id, 0) + qty
                elif not only_ore and reprocessed:
                    for part_id in reprocessed:
                        chunks = math.floor(queue[store_type_id] / Static.type_by_id(store_type_id).portion_size)
                        qty = math.floor(
                            reprocessed[part_id] *
                            chunks *
                            self.base_scrap *
                            (1 + 2 * self.skill_metallurgy / 100)
                        )
                        if deep:
                            process[part_id] = process.get(part_id, 0) + qty
                        else:
                            result[part_id] = result.get(part_id, 0) + qty
                else:
                    result[store_type_id] = result.get(store_type_id, 0) + queue[store_type_id]

            if len(process) == 0:
                break
            else:
                queue = process
                process = {}

        # for key in result:
        #     print(TypeById[key].name, result[key])

        return result
