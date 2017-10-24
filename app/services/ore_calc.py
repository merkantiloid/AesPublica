from ..models import OreCalc
from .static import Static
from app import db

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
                rig2_id= -1,
                rig3_id= -1,
            )
            db.session.add(temp)
            db.session.commit()

        self.characters = [{'id': -1, 'name': 'All 5'}]

    def to_json(self):
        return {
            "space": self.user.ore_calc.space,
            "citadel_id": self.user.ore_calc.citadel_id,
            "characters": self.characters,
            "character_id": self.user.ore_calc.character_id,
            "implant_id": self.user.ore_calc.implant_id,
            "rig1_id": self.user.ore_calc.rig1_id,
            "rig2_id": self.user.ore_calc.rig2_id,
            "rig3_id": self.user.ore_calc.rig3_id,
        }