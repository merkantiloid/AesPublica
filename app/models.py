from app import db
from app.eve_models import EveType
from sqlalchemy import ForeignKey
from math import ceil


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
    esi_char_id = db.Column(db.BigInteger)
    implant_id = db.Column(db.BigInteger)
    rig1_id = db.Column(db.BigInteger)
    rig2_id = db.Column(db.BigInteger)
    rig3_id = db.Column(db.BigInteger)

    ore_settings = db.Column(db.String)

    build_items_text = db.Column(db.Text)
    build_items = db.relationship("BuildItem", back_populates="ore_calc")

    store_items_text = db.Column(db.Text)
    store_items = db.relationship("StoreItem", back_populates="ore_calc")

    def checked_ores(self):
        if not self.ore_settings:
            return []

        result = []
        parts = self.ore_settings.split(',')
        for part in parts:
            try:
                result.append( int(part) )
            except ValueError:
                pass
        return result


class BuildItem(db.Model):
    __tablename__ = 'build_items'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    qty = db.Column(db.BigInteger, nullable=False)
    me = db.Column(db.Integer, nullable=False)
    te = db.Column(db.Integer, nullable=False)

    type_id = db.Column(db.BigInteger, ForeignKey('eve_types.id'), nullable=False)
    type = db.relationship("EveType")

    ore_calc_id = db.Column(db.BigInteger, ForeignKey('ore_calcs.id'), nullable=False)
    ore_calc = db.relationship("OreCalc")

    def to_json(self):
        return {
            'id': self.id,
            'type': self.type.to_json(),
            'me': self.me,
            'te': self.te,
            'runs': ceil(self.qty/self.type.portion_size),
            'qty': self.qty,
            'excess': ceil(self.qty/self.type.portion_size)*self.type.portion_size-self.qty
        }


class StoreItem(db.Model):
    __tablename__ = 'store_items'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    qty = db.Column(db.BigInteger, nullable=False)

    type_id = db.Column(db.BigInteger, ForeignKey('eve_types.id'), nullable=False)
    type = db.relationship("EveType")

    ore_calc_id = db.Column(db.BigInteger, ForeignKey('ore_calcs.id'), nullable=False)
    ore_calc = db.relationship("OreCalc")

    def to_json(self):
        return {
            'id': self.id,
            'type': self.type.to_json(),
            'qty': self.qty,
        }


class Price(db.Model):
    __tablename__ = 'prices'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.Float)
    source = db.Column(db.String)
    updated_at = db.Column(db.String)
    type_id = db.Column(db.BigInteger, ForeignKey('eve_types.id'), nullable=False)
    type = db.relationship("EveType")


