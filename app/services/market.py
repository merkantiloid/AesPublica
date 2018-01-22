from .esi import EsiService
from .locations import LocationsService
from app import db

def _sort_key(item):
    return item[1]

class MarketService:

    def __init__(self):
        pass

    def _apply_order(self, result, order):
        temp = result[order['type_id']]
        temp['qty'] += order['volume_remain']
        if not temp['min'] or temp['min']>order['price']:
            temp['min'] = order['price']
        temp['prices'].append([order['volume_remain'],order['price']])

    def info(self, locations, items, fit_times):
        station_ids = []
        station_region_ids = []
        citadels = []
        citadel_ids = []
        for str in locations:
            loc = str.esi_location
            if loc.category == "station":
                station_ids.append(loc.id)
                if not loc.system_id or not loc.region_id:
                    esi = EsiService(str.esi_char)
                    st_data = esi.universe_stations(loc.id)
                    loc.region_id = LocationsService().update_region_id(loc, st_data['system_id'])

                if loc.region_id not in station_region_ids:
                    station_region_ids.append(loc.region_id)

            if loc.category == "citadel":
                citadels.append(str)
                citadel_ids.append(loc.id)
                if not loc.system_id or not loc.region_id:
                    esi = EsiService(str.esi_char)
                    st_data = esi.universe_structures(loc.id)
                    LocationsService().update_region_id(loc, st_data['solar_system_id'])

        result = {}
        type_ids = []
        for item in items:
            result[item.type_id] = {'qty': 0, 'min': None, 'avg': None, 'prices': []}
            type_ids.append(item.type_id)

        esi = EsiService()
        for region_id in station_region_ids:
            for item in items:
                current = 1
                max_page = None
                while True:
                    orders,pages = esi.markets_orders(region_id, item.type.id, "sell",current)
                    for order in orders:
                        if not order['is_buy_order'] and order['location_id'] in station_ids:
                            self._apply_order(result, order)
                    if not max_page:
                        max_page = pages
                    current += 1
                    if current > max_page :
                        break

        for citadel in citadels:
            esi = EsiService(citadel.esi_char)
            current = 1
            max_page = None
            while True:
                orders,pages = esi.markets_structures(citadel.esi_location_id, current)
                for order in orders:
                    if not order['is_buy_order'] and order['location_id'] in citadel_ids and order['type_id'] in type_ids:
                        self._apply_order(result, order)
                if not max_page:
                    max_page = pages
                current += 1
                if current > max_page :
                    break

        for item in items:
            prices = result[item.type_id]['prices']
            prices = sorted(prices, key=_sort_key)
            need = fit_times * item.qty
            temp = 0
            index = 0
            value = 0
            while index<len(prices) and temp < need:
                if temp + prices[index][0] <= need:
                    value = value + prices[index][0]*prices[index][1]
                    temp = temp + prices[index][0]
                else:
                    value = value + (need-temp)*prices[index][1]
                    temp = need
                index += 1

            if temp>0:
                result[item.type_id]['avg'] = value/temp

            item.market_qty = result[item.type_id]['qty']
            item.min_price = result[item.type_id]['min']
            item.avg_price = result[item.type_id]['avg']
            db.session.add(item)
        db.session.commit()


