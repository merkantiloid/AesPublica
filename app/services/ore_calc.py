from ..models import OreCalc
from .static import Static
from app import db
from .loaders import load_chars


class OreCalcService:

    def __init__(self, user):
        self.user = user
        if not self.user.ore_calc:
            temp = OreCalc(
                user=self.user,
                space=Static.DEFAULT_SPACE,
                citadel_id=Static.DEFAULT_CITADEL,
                implant_id= -1,
                rig1_id= -1,
            )
            db.session.add(temp)
            db.session.commit()

        self.characters = [{'id': -1,'name': 'All 5','skills': {3385: 5, 3389: 5, 12196: 5}}] + load_chars(user.id)

    def to_json(self):
        return {
            "space": self.user.ore_calc.space,
            "citadel_id": self.user.ore_calc.citadel_id,
            "characters": self.characters,
            "esi_char_id": self.user.ore_calc.esi_char_id,
            "implant_id": self.user.ore_calc.implant_id,
            "rig1_id": self.user.ore_calc.rig1_id,
        }