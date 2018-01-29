from app.models import MoonMat, MoonMatRig
from app import db
from .static import Static


class MoonMatService:

    def __init__(self, user):
        self.user = user
        if not self.user.moon_mat:
            temp = MoonMat(
                user=self.user,
                space="z"
            )
            db.session.add(temp)
            db.session.commit()

    def add_rig(self, rig_id):
        model = self.user.moon_mat
        temp = MoonMatRig.query.filter(MoonMatRig.moon_mat_id==model.id, MoonMatRig.rig_id==rig_id).first()
        if not temp:
            temp = MoonMatRig(moon_mat_id=model.id, rig_id=rig_id)
            db.session.add(temp)
            db.session.commit()

    def delete_rig(self, rig_id):
        model = self.user.moon_mat
        temp = MoonMatRig.query.filter(MoonMatRig.moon_mat_id==model.id, MoonMatRig.rig_id==rig_id).first()
        if temp:
            db.session.delete(temp)
            db.session.commit()

    def to_json(self):
        model = self.user.moon_mat

        return {
            "spaces": Static.RSPACES,
            "rigs": Static.RRIGS,
            "settings": {
                "space": model.space,
                "rigs": [x.to_json() for x in model.rigs],
            }
        }

