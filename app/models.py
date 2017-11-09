from app import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), index=True, unique=True, nullable=False)
    hash = db.Column(db.String(255))
    lang = db.Column(db.String(255))

    ore_calc = db.relationship("OreCalc", uselist=False, back_populates="user")
    esi_chars = db.relationship("EsiChar", back_populates="user")

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<User: [%r] %r (%r)>' % (self.id, self.name, self.lang)


class OreCalc(db.Model):
    __tablename__ = 'ore_calcs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("User", back_populates="ore_calc")
    space = db.Column(db.String)
    citadel_id = db.Column(db.BigInteger)
    character_id = db.Column(db.BigInteger)
    implant_id = db.Column(db.BigInteger)
    rig1_id = db.Column(db.BigInteger)
    rig2_id = db.Column(db.BigInteger)
    rig3_id = db.Column(db.BigInteger)
