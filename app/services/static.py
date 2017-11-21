from .loaders import load_citadels, load_repr_implants, load_repr_rigs, load_repr_rigs_hash, load_calc_ids, load_ores
from app.eve_models import EveType, EveBlueprint, EveTypeMaterial
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
for type in EveType.query.all():
    TypeHashes[type.name.lower()] = type.id
    TypeById[type.id] = type

CalcIDs = load_calc_ids()


ReprocessByTypeId = {}
for r in EveTypeMaterial.query.all():
    if r.type_id not in ReprocessByTypeId:
        ReprocessByTypeId[r.type_id] = {}
    ReprocessByTypeId[r.type_id][r.material_id] = r.qty

AllOres = load_ores()

ReprRigsHash = load_repr_rigs_hash()

ReprImplants = load_repr_implants()
ReprImplantsHash = {}
for x in ReprImplants:
    ReprImplantsHash[x['id']] = x


class Static:
    SPACES = {'h':'Hi-Sec', 'l':'Low-Sec', 'z':'Zero/WH'}
    DEFAULT_SPACE = 'z'

    CITADELS = load_citadels()
    DEFAULT_CITADEL = 35825 #Raitaru

    REPR_RIGS = load_repr_rigs()


    @staticmethod
    def to_json():
        return {
            "spaces": Static.SPACES,
            "citadels": Static.CITADELS,
            "repr_implants": ReprImplants,
            "repr_rigs": Static.REPR_RIGS,
            "repr_rigs_hash": ReprRigsHash,
        }


