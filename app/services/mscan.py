from app.models import MScan
from app.esi_models import EsiChar

class MScanService:

    def __init__(self, user):
        self.user = user

    def list(self):
        mscans = MScan.query.filter(EsiChar.user_id == self.user.id).all()

        result = []
        for scan in mscans:
            result.append(scan.short_json())

        return result


