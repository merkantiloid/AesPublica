from app import db


class EveType(db.Model):
    __tablename__ = 'eve_types'
    id = db.Column(db.BigInteger, primary_key=True)
    group_id = db.Column(db.BigInteger)
    market_group_id = db.Column(db.BigInteger)
    volume = db.Column(db.Float)
    name = db.Column(db.String)
    portion_size = db.Column(db.BigInteger)
    published = db.Column(db.Boolean)


class EveMarketGroup(db.Model):
    __tablename__ = 'eve_market_groups'
    id = db.Column(db.BigInteger, primary_key=True)
    description = db.Column(db.String)
    has_types = db.Column(db.Boolean)
    name = db.Column(db.String)
    icon_id = db.Column(db.BigInteger)
    parent_id = db.Column(db.BigInteger)
