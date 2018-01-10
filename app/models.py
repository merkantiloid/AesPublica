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

    calc_results = db.relationship("CalcResult", lazy="joined", back_populates="ore_calc")

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
    type = db.relationship("EveType", lazy="joined")

    ore_calc_id = db.Column(db.BigInteger, ForeignKey('ore_calcs.id'), nullable=False)
    ore_calc = db.relationship("OreCalc")

    def to_json(self, **kwargs):
        temp = {
            'id': self.id,
            'type': self.type.to_json(),
            'me': self.me,
            'te': self.te,
            'runs': ceil(self.qty/self.type.portion_size),
            'qty': self.qty,
            'excess': ceil(self.qty/self.type.portion_size)*self.type.portion_size-self.qty
        }

        return {**temp, **kwargs}


class StoreItem(db.Model):
    __tablename__ = 'store_items'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    qty = db.Column(db.BigInteger, nullable=False)

    type_id = db.Column(db.BigInteger, ForeignKey('eve_types.id'), nullable=False)
    type = db.relationship("EveType", lazy="joined")

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
    buy = db.Column(db.Float)
    sell = db.Column(db.Float)
    source = db.Column(db.String)
    updated_at = db.Column(db.String)
    type_id = db.Column(db.BigInteger, ForeignKey('eve_types.id'), nullable=False)
    type = db.relationship("EveType")


class CalcResult(db.Model):
    __tablename__ = 'calc_results'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    ore_calc_id = db.Column(db.BigInteger, ForeignKey('ore_calcs.id'), nullable=False)
    ore_calc = db.relationship("OreCalc")

    type_id = db.Column(db.BigInteger, ForeignKey('eve_types.id'), nullable=False)
    type = db.relationship("EveType", lazy="joined")

    qty = db.Column(db.BigInteger, nullable=False)

    def to_json(self, **kwargs):
        source = kwargs ['price_source'] if 'price_source' in kwargs else 'esi'
        price = Price.query.filter(Price.source == source, Price.type_id == self.type_id).order_by(Price.id.desc()).first()
        return {
            'id': self.id,
            'type': self.type.to_json(),
            'qty': self.qty,
            'price_1u': price.sell,
            'price': self.qty * price.sell,
            'volume': self.qty * self.type.volume,
        }


def sort_key(item):
    return '%d-%s' % (item['type']['group_id'] , item['type']['name'])

class MScan(db.Model):
    __tablename__ = 'mscans'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("User")

    name = db.Column(db.String)
    raw = db.Column(db.Text)
    check_date = db.Column(db.String)
    fit_times = db.Column(db.BigInteger)

    items = db.relationship("MScanItem", lazy="joined", back_populates="mscan")

    def short_json(self):
        return {'id': self.id, 'name': self.name}

    def to_json(self):
        items = [x.to_json() for x in self.items]
        items = sorted(items, key=sort_key)
        return {
            'id': self.id,
            'name': self.name,
            'raw': self.raw,
            'fit_times': self.fit_times,
            'items': items,
        }


class MScanLocation(db.Model):
    __tablename__ = 'mscan_locations'

    mscan_id = db.Column(db.Integer, db.ForeignKey('mscans.id'), primary_key=True)
    mscan = db.relationship("MScan")

    esi_location_id = db.Column(db.BigInteger, db.ForeignKey('esi_locations.id'), primary_key=True)
    esi_location = db.relationship("EsiLocation")

    esi_char_id = db.Column(db.BigInteger, db.ForeignKey('esi_chars.id'), primary_key=True)
    esi_char = db.relationship("EsiChar")


class MScanItem(db.Model):
    __tablename__ = 'mscan_items'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    mscan_id = db.Column(db.Integer, db.ForeignKey('mscans.id'), primary_key=True)
    mscan = db.relationship("MScan")

    type_id = db.Column(db.BigInteger, ForeignKey('eve_types.id'), nullable=False)
    type = db.relationship("EveType", lazy="joined")

    qty = db.Column(db.BigInteger)
    store_qty = db.Column(db.BigInteger)
    market_qty = db.Column(db.BigInteger)
    min_price = db.Column(db.Float)
    avg_price = db.Column(db.Float)

    def to_json(self):
        return {
            'type': self.type.to_json(),
            'qty': self.qty,
            'market_qty': self.market_qty,
            'min_price': self.min_price,
            'avg_price': self.avg_price,
        }