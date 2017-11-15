from ..models import OreCalc
from .static import Static
from app import db
from .loaders import load_chars
from .parsing import parse_name_qty


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
        model = self.user.ore_calc
        return {
            "settings": {
                "space": model.space,
                "citadel_id": model.citadel_id,
                "characters": self.characters,
                "esi_char_id": model.esi_char_id,
                "implant_id": model.implant_id,
                "rig1_id": model.rig1_id,
            },
            "build_items_text": model.build_items_text,
        }


    def add_build_item(self, text):
        print(parse_name_qty(text))