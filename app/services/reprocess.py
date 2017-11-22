from app.services.static import ReprocessByTypeId, AllOres, ReprRigsHash, ReprImplantsHash, TypeById
from app.esi_models import EsiSkill
import math

class ReprocessService:

    def __init__(self, ore_calc):
        self.ore_calc = ore_calc

        self.base_scrap = 0.5

        self.implant = ReprImplantsHash[self.ore_calc.implant_id]['value']

        self.skills = {}
        for s in EsiSkill.query.filter(EsiSkill.esi_char_id==self.ore_calc.esi_char_id).all():
            self.skills[s.skill_id] = s.current_skill_level

        self.skill_metallurgy = self.skills.get(12196, (5 if self.ore_calc.esi_char_id==-1 else 0) )
        self.repr = self.skills.get(3385, (5 if self.ore_calc.esi_char_id==-1 else 0) )
        self.repr_eff = self.skills.get(3389, (5 if self.ore_calc.esi_char_id==-1 else 0) )


    def reprocess(self, only_ore = False, deep = True):
        result = {}
        process = {}
        queue = {}

        for item in self.ore_calc.store_items:
            queue[item.type_id] = queue.get(item.type_id,0) + item.qty

        while True:

            for store_type_id in queue:
                if store_type_id in AllOres:
                    for part_id in ReprocessByTypeId[store_type_id]:
                        chunks = math.floor(queue[store_type_id] / TypeById[store_type_id].portion_size)
                        ore_skill_id = AllOres[store_type_id]['skill_id']
                        ore_skill = self.skills.get(ore_skill_id, (5 if self.ore_calc.esi_char_id==-1 else 0) )
                        qty = math.floor(
                            ReprocessByTypeId[store_type_id][part_id] *
                            chunks *
                            self.base_scrap *
                            (1+self.implant/100) *
                            (1+3*self.repr/100) *
                            (1+2*self.repr_eff/100) *
                            (1+2*ore_skill/100)
                        )
                        if deep:
                            process[part_id] = process.get(part_id,0) + qty
                        else:
                            result[part_id] = result.get(part_id,0) + qty
                elif not only_ore and store_type_id in ReprocessByTypeId:
                    for part_id in ReprocessByTypeId[store_type_id]:
                        chunks = math.floor(queue[store_type_id] / TypeById[store_type_id].portion_size)
                        qty = math.floor(
                            ReprocessByTypeId[store_type_id][part_id] *
                            chunks *
                            self.base_scrap *
                            (1+2*self.skill_metallurgy/100)
                        )
                        if deep:
                            process[part_id] = process.get(part_id,0) + qty
                        else:
                            result[part_id] = result.get(part_id,0) + qty
                else:
                    result[store_type_id] = result.get(store_type_id,0) + queue[store_type_id]

            if len(process) == 0:
                break
            else:
                queue = process
                process = {}


        for key in result:
            print(TypeById[key].name, result[key])

        return result