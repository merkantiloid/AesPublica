from .loaders import load_citadels, load_repr_implants, load_repr_rigs, load_repr_rigs_hash, load_calc_ids
from app.eve_models import EveType, EveBlueprint
from app.esi_models import EsiChar


BlueprintById = {}
BlueprintByProductId = {}
MaterialsByProductId = {}
bps = EveBlueprint.query.all()
for bp in bps:
    BlueprintById[bp.id] = bp
    BlueprintByProductId[bp.product_id] = bp
    if 'manufacturing' in bp.props['activities'] and 'materials' in bp.props['activities']['manufacturing']:
        array = bp.props['activities']['manufacturing']['materials']
        hash = {}
        for el in array:
            hash[el['typeID']] = el['quantity']
        MaterialsByProductId[bp.product_id] = hash


TypeHashes = {}
TypeById = {}

types = EveType.query.all()
for type in types:
    TypeHashes[type.name.lower()] = type.id
    TypeById[type.id] = type

CalcIDs = load_calc_ids()


class Static:
    SPACES = {'h':'Hi-Sec', 'l':'Low-Sec', 'z':'Zero/WH'}
    DEFAULT_SPACE = 'z'

    CITADELS = load_citadels()
    DEFAULT_CITADEL = 35825 #Raitaru

    REPR_IMPLANTS = load_repr_implants()

    REPR_RIGS = load_repr_rigs()
    REPR_RIGS_HASH = load_repr_rigs_hash()

    @staticmethod
    def to_json():
        return {
            "spaces": Static.SPACES,
            "citadels": Static.CITADELS,
            "repr_implants": Static.REPR_IMPLANTS,
            "repr_rigs": Static.REPR_RIGS,
            "repr_rigs_hash": Static.REPR_RIGS_HASH,
        }


