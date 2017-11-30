from .static import MaterialsByProductId, TypeById, CalcIDs
from math import ceil

def sort_key(item):
    return '%d-%s' % (TypeById[item['type_id']].group_id , item['type_name'])

class ComponentsService:

    def __init__(self, ore_calc):
        self.ore_calc = ore_calc

    def only_minerals(self, store={}, after_refine={}):
        all = self.reverse_assembly({})
        need = self.reverse_assembly(store)
        result = []
        for key in all:
            if key in CalcIDs:
                result.append({
                    'type_id': key,
                    'type_name': TypeById[key].name,
                    'all_qty': all[key],
                    'need_qty': need.get(key,0),
                    'odd_qty': after_refine.get(key,0) - need.get(key,0),
                })

        result = sorted(result, key=sort_key)

        return result

    def reverse_assembly(self, store):

        temp_store = store.copy()

        result = {}
        queue = {}
        process = {}

        for item in self.ore_calc.build_items:
            key = "%d-%d-%d" % (item.type_id, item.me, item.te)
            store_qty = self.apply_store(temp_store, item.type_id, item.qty)
            if store_qty > 0:
                queue[key] = {
                    'type_id': item.type_id,
                    'runs': ceil(store_qty / TypeById[item.type_id].portion_size),
                    'qty': store_qty,
                    'me': item.me,
                    'te': item.te
                }

        while True:
            for pkey in queue:
                i_type_id = queue[pkey]['type_id']

                if i_type_id in MaterialsByProductId:
                    for mid in MaterialsByProductId[i_type_id]:
                        mqty = MaterialsByProductId[i_type_id][mid]
                        real_qty = self.applyME(mqty, queue[pkey]['runs'], queue[pkey]['me'])
                        store_real_qty = self.apply_store(temp_store, mid, real_qty)

                        if mid in MaterialsByProductId:
                            imt_key = "%d-%d-%d" % (mid, 10, 20)
                            record = process.get(imt_key, {'type_id': mid, 'runs': 0, 'qty': 0, 'me': 10, 'te': 20})
                            record['qty'] = record['qty'] + store_real_qty
                            record['runs'] = ceil(record['qty']/TypeById[mid].portion_size)
                            process[imt_key] = record
                        else:
                            result[mid] = result.get(mid,0) + store_real_qty
                else:
                    result[i_type_id] = result.get(i_type_id,0) + queue[pkey]['qty']

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

    def apply_store(self, store, type_id, qty):
        if type_id in store and store[type_id]>0:
            if store[type_id]>qty:
                store[type_id] = store[type_id]-qty
                return 0
            else:
                temp = qty-store[type_id]
                store[type_id] = 0
                return temp

        return qty

