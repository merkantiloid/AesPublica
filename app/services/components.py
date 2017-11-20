from .static import MaterialsByProductId, TypeById, CalcIDs
from math import ceil

def sort_key(item):
    return '%d-%s' % (TypeById[item['type_id']].group_id , item['type_name'])

class ComponentsService:

    def __init__(self, ore_calc):
        self.ore_calc = ore_calc

    def only_minerals(self):
        all = self.disassemble()
        result = []
        for key in all:
            if key in CalcIDs:
                result.append({'type_id': key, 'type_name': TypeById[key].name, 'qty': all[key]})

        result = sorted(result, key=sort_key)

        return result

    def disassemble(self):

        result = {}
        queue = {}
        process = {}

        for item in self.ore_calc.build_items:
            key = "%d-%d-%d" % (item.type_id, item.me, item.te)
            queue[key] = {
                'type_id': item.type_id,
                'runs': ceil(item.qty / TypeById[item.type_id].portion_size),
                'qty': item.qty,
                'me': item.me,
                'te': item.te
            }

        while True:
            for pkey in queue:
                i_type_id = queue[pkey]['type_id']

                if i_type_id in MaterialsByProductId:
                    for mid in MaterialsByProductId[i_type_id]:
                        mqty = MaterialsByProductId[i_type_id][mid]
                        real_qty = self.applyME(mqty, queue[pkey]['runs'], queue[pkey]['me']) #todo portion_size

                        if mid in MaterialsByProductId:
                            imt_key = "%d-%d-%d" % (mid, 10, 20)
                            record = process.get(imt_key, {'type_id': mid, 'runs': 0, 'qty': 0, 'me': 10, 'te': 20})
                            record['qty'] = record['qty'] + real_qty
                            record['runs'] = ceil(record['qty']/TypeById[mid].portion_size)
                            process[imt_key] = record
                        else:
                            result[mid] = result.get(mid,0) + real_qty

            if len(process) == 0:
                break
            else:
                queue = process
                process = {}

        return result

    def applyME(self, cnt, runs, me, bonus1=0, bonus2=0):
        if cnt==1:
            return runs
        return ceil( cnt * runs * (1-me/100) * (1-bonus1/100) * (1-bonus2/100) )

        return runs
