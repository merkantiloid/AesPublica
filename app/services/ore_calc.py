from ..models import OreCalc
from .static import Static
from app import db

class OreCalcService:

    def __init__(self, user):
        self.user = user
        if not self.user.ore_calc:
            temp = OreCalc(user=self.user, space=Static.DEFAULT_SPACE)
            db.session.add(temp)
            db.session.commit()

    def to_json(self):
        return {
            "space": self.user.ore_calc.space,
        }