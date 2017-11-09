from .loaders import load_citadels, load_repr_implants, load_repr_rigs, load_repr_rigs_hash

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