from app.extensions import db  # Импорт из extensions
from sqlalchemy import ForeignKey


class EveTypeSimple:
    def __init__(self, complex):
        self.id = complex.id
        self.name = complex.name
        self.portion_size = complex.portion_size
        self.group_id = complex.group_id
        self.volume = complex.volume

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'portion_size': self.portion_size,
            'group_id': self.group_id,
            'volume': self.volume,
        }


class EveType(db.Model):
    __tablename__ = 'eve_types'
    id = db.Column(db.BigInteger, primary_key=True)
    group_id = db.Column(db.BigInteger)
    market_group_id = db.Column(db.BigInteger)
    volume = db.Column(db.Float)
    name = db.Column(db.String)
    portion_size = db.Column(db.BigInteger)
    published = db.Column(db.Boolean)

    def simple(self):
        return EveTypeSimple(self)

    def to_json(self):
        return self.simple().to_json()


class EveMarketGroup(db.Model):
    __tablename__ = 'eve_market_groups'
    id = db.Column(db.BigInteger, primary_key=True)
    description = db.Column(db.String)
    has_types = db.Column(db.Boolean)
    name = db.Column(db.String)
    icon_id = db.Column(db.BigInteger)
    parent_id = db.Column(db.BigInteger)


class EveGroup(db.Model):
    __tablename__ = 'eve_groups'
    id = db.Column(db.BigInteger, primary_key=True)
    category_id = db.Column(db.BigInteger)
    icon_id = db.Column(db.BigInteger)
    published = db.Column(db.Boolean)
    name = db.Column(db.String)


class EveCategory(db.Model):
    __tablename__ = 'eve_categories'
    id = db.Column(db.BigInteger, primary_key=True)
    icon_id = db.Column(db.BigInteger)
    published = db.Column(db.Boolean)
    name = db.Column(db.String)


class EveTypeAttribute(db.Model):
    __tablename__ = 'eve_type_attributes'
    type_id = db.Column(db.BigInteger, primary_key=True)
    attribute_id = db.Column(db.BigInteger, primary_key=True)
    value = db.Column(db.Float)


class EveAttribute(db.Model):
    __tablename__ = 'eve_attributes'
    id = db.Column(db.BigInteger, primary_key=True)
    code = db.Column(db.String)
    name = db.Column(db.String)
    category_id = db.Column(db.BigInteger)
    default_value = db.Column(db.Float)
    description = db.Column(db.String)
    icon_id = db.Column(db.BigInteger)
    unit_id = db.Column(db.BigInteger)
    published = db.Column(db.Boolean)
    stackable = db.Column(db.Boolean)
    high_is_good = db.Column(db.Boolean)


class EveBlueprintSimple():
    def __init__(self, complex):
        self.id = complex.id
        self.product_id = complex.product_id


class EveBlueprint(db.Model):
    __tablename__ = 'eve_blueprints'
    id = db.Column(db.BigInteger, primary_key=True)

    product_id = db.Column(db.BigInteger)

    props = db.Column(db.JSON)

    def simple(self):
        return EveBlueprintSimple(self)


class EveTypeMaterial(db.Model):
    __tablename__ = 'eve_type_materials'

    type_id = db.Column(db.BigInteger, primary_key=True)
    material_id = db.Column(db.BigInteger, primary_key=True)
    qty = db.Column(db.BigInteger)
