from app.models import MScan
from app.esi_models import EsiChar
from app import db


class MScanService:

    def __init__(self, user):
        self.user=user

    def list(self):
        mscans=MScan.query.filter(MScan.user_id == self.user.id).order_by(MScan.name).all()
        result = []
        for scan in mscans:
            result.append(scan.short_json())
        return result

    def add_scan(self, name):
        if bool(name.strip()):
            temp = MScan(
                name=name,
                user_id=self.user.id
            )
            db.session.add(temp)
            db.session.commit()
            return temp.id
        return None

    def rename_scan(self, id, name):
        temp = MScan.query.filter(MScan.user_id == self.user.id, MScan.id == id).first()
        if temp and bool(name.strip()):
            temp.name=name
            db.session.add(temp)
            db.session.commit()

    def delete_scan(self, id):
        temp = MScan.query.filter(MScan.user_id == self.user.id, MScan.id == id).first()
        if temp:
            db.session.delete(temp)
            db.session.commit()

    def to_json(self, selected_id=None):
        selected = None
        if selected_id:
            selected = {'id': selected_id}
        return {
            'list': self.list(),
            'selected': selected
        }


