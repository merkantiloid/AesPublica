from .esi import EsiService
from .locations import LocationsService
from .static import Static
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

    def _appropriate(self, flag):
        return not flag.startswith('RigSlot') \
               and not flag.startswith('LoSlot') \
               and not flag.startswith('MedSlot') \
               and not flag.startswith('HiSlot') \
               and not flag.startswith('SubSystemSlot') \
               and not flag.startswith('FighterTube') \
               and flag != 'DroneBay' \
               and flag != 'Cargo' \
               and flag != 'FleetHangar' \
               and flag != 'FighterBay' \
               and flag != 'HiddenModifiers' \
               and flag != 'SpecializedFuelBay'


    def info(self, locations, assets, items, fit_times):
        station_ids, station_region_ids, citadels, citadel_ids = self.sort_locations(locations)

        result = {}
        type_ids = []
        for item in items:
            result[item.type_id] = {'qty': 0, 'store': 0, 'min': None, 'avg': None, 'prices': []}
            type_ids.append(item.type_id)

        self.process_stations(items, result, station_ids, station_region_ids)
        self.process_citadels(citadel_ids, citadels, result, type_ids)

        chars_for_check = {}
        for asset in assets:
            if not asset.esi_char_id in chars_for_check:
                chars_for_check[asset.esi_char_id] = {'lids': [asset.esi_location_id], 'char': asset.esi_char}
            else:
                chars_for_check[asset.esi_char_id]['lids'].append(asset.esi_location_id)

        for char_id in chars_for_check:
            esi = EsiService(chars_for_check[char_id]['char'])
            hash = esi.characters_assets_full()
            for id in hash:
                if hash[id]['rid'] in chars_for_check[char_id]['lids'] \
                        and hash[id]['type_id'] in result \
                        and self._appropriate(hash[id]['location_flag']):
                    temp = result[hash[id]['type_id']]
                    temp['store'] += hash[id]['quantity']
                    print(
                        hash[id]['location_flag'],
                        Static.type_by_id(hash[id]['type_id']).name,
                        hash[id]['quantity'],
                    )

        self.post_processing(fit_times, items, result)


    def post_processing(self, fit_times, items, result):
        for item in items:
            prices = result[item.type_id]['prices']
            prices = sorted(prices, key=_sort_key)
            need = fit_times * item.qty
            temp = 0
            index = 0
            value = 0
            while index < len(prices) and temp < need:
                if temp + prices[index][0] <= need:
                    value = value + prices[index][0] * prices[index][1]
                    temp = temp + prices[index][0]
                else:
                    value = value + (need - temp) * prices[index][1]
                    temp = need
                index += 1

            if temp > 0:
                result[item.type_id]['avg'] = value / temp

            item.market_qty = result[item.type_id]['qty']
            item.store_qty = result[item.type_id]['store']
            item.min_price = result[item.type_id]['min']
            item.avg_price = result[item.type_id]['avg']
            db.session.add(item)
        db.session.commit()

    def process_citadels(self, citadel_ids, citadels, result, type_ids):
        for citadel in citadels:
            esi = EsiService(citadel.esi_char)
            current = 1
            max_page = None
            while True:
                orders, pages = esi.markets_structures(citadel.esi_location_id, current)
                for order in orders:
                    if not order['is_buy_order'] and order['location_id'] in citadel_ids and order['type_id'] in type_ids:
                        self._apply_order(result, order)
                if not max_page:
                    max_page = pages
                current += 1
                if current > max_page:
                    break

    def process_stations(self, items, result, station_ids, station_region_ids):
        esi = EsiService()
        for region_id in station_region_ids:
            for item in items:
                current = 1
                max_page = None
                while True:
                    orders, pages = esi.markets_orders(region_id, item.type.id, "sell", current)
                    for order in orders:
                        if not order['is_buy_order'] and order['location_id'] in station_ids:
                            self._apply_order(result, order)
                    if not max_page:
                        max_page = pages
                    current += 1
                    if current > max_page:
                        break

    def sort_locations(self, locations):
        citadel_ids = []
        citadels = []
        station_ids = []
        station_region_ids = []
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


        return station_ids, station_region_ids, citadels, citadel_ids