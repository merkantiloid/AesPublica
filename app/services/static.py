from .loaders import load_citadels, load_citadels_hash, load_repr_implants, load_repr_rigs, load_repr_rigs_hash, \
    load_calc_ids, load_ores, load_reactor_rigs
from app.eve_models import EveType, EveBlueprint, EveTypeMaterial
from app.esi_models import EsiChar
from munch import Munch
from functools import lru_cache

_HASHES = {}
for type in EveType.query.filter(EveType.published==True).all():
    _HASHES[type.name.lower()] = type.id

CalcIDs = load_calc_ids()

AllOres = load_ores()

AllOresGrouped = {
    '1_ore_h': {'name': 'Hi-Sec Ores', 'items': {}},
    '2_ore_l': {'name': 'Low-Sec Ores', 'items': {}},
    '3_ore_z': {'name': 'Zero-Sec Ores', 'items': {}},
    '4_ice':   {'name': 'Ice', 'items': {}},
    '5_ore_m': {'name': 'Moon Extra Ores', 'items': {}}
}

for id in AllOres:
    ore = AllOres[id]
    if ore['ore_type_text'] != '5_ore_m' and ore['ore_type'] == 1 and ore['compressed_id'] or \
            ore['ore_type_text'] == '5_ore_m' and ore['ore_type'] == 4 and ore['compressed_id']:
        key = ore['skill_id'] if ore['ore_type_text'] != '4_ice' else ore['base_ore_id']
        AllOresGrouped[ore['ore_type_text']]['items'][key] = {'base_name': ore['name'], 'ores': []}

for id in AllOres:
    ore = AllOres[id]
    key = ore['skill_id'] if ore['ore_type_text'] != '4_ice' else ore['base_ore_id']
    AllOresGrouped[ore['ore_type_text']]['items'][key]['ores'].append(ore)

ReprRigsHash = load_repr_rigs_hash()

ReprImplants = load_repr_implants()
ReprImplantsHash = {}
for x in ReprImplants:
    ReprImplantsHash[x['id']] = x


class Static:
    SPACES = {'h':'Hi-Sec', 'l':'Low-Sec', 'z':'Zero/WH'}
    RSPACES = {'l':'Low-Sec', 'z':'Zero/WH'}
    DEFAULT_SPACE = 'z'

    CITADELS = load_citadels()
    CITADELS_HASH = load_citadels_hash()

    DEFAULT_CITADEL = 35825 #Raitaru

    REPR_RIGS = load_repr_rigs()

    RRIGS = load_reactor_rigs()


    @staticmethod
    def to_json():
        return {
            "spaces": Static.SPACES,
            "citadels": Static.CITADELS,
            "repr_implants": ReprImplants,
            "repr_rigs": Static.REPR_RIGS,
            "repr_rigs_hash": ReprRigsHash,
            "ores": AllOresGrouped,
        }

    @lru_cache()
    def type_hash_to_id(hash):
        if hash in _HASHES:
            return _HASHES[hash]
        else:
            return None

    @lru_cache()
    def type_by_id(id):
        type = EveType.query.get(id)
        if type:
            return Munch(type.to_json())
        else:
            return None

    @lru_cache()
    def materials_by_id(pid):
        bp = EveBlueprint.query.filter(EveBlueprint.product_id==pid).first()
        if bp:
            if 'manufacturing' in bp.props['activities'] and 'materials' in bp.props['activities']['manufacturing']:
                array = bp.props['activities']['manufacturing']['materials']
                hash = {}
                for el in array:
                    hash[el['typeID']] = el['quantity']
                return hash
        return None

    @lru_cache()
    def materials_by_reaction_pid(rpid):
        bp = EveBlueprint.query.filter(EveBlueprint.product_id==rpid).first()
        if bp:
            if 'reaction' in bp.props['activities'] and 'materials' in bp.props['activities']['reaction']:
                array = bp.props['activities']['reaction']['materials']
                hash = {}
                for el in array:
                    hash[el['typeID']] = el['quantity']
                return {'qty': bp.props['activities']['reaction']['products'][0]['quantity'], 'input': hash}
        return None

    @lru_cache()
    def bid_by_pid(pid):
        data = EveBlueprint.query.filter(EveBlueprint.product_id==pid).first()

        if data:
            return data.id
        else:
            return None

    @lru_cache()
    def reprocess_by_id(id):
        data = EveTypeMaterial.query.filter(EveTypeMaterial.type_id == id).all()
        hash = {}
        for r in data:
            hash[r.material_id] = r.qty
        return hash

