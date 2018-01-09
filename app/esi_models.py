from sqlalchemy import ForeignKey
from app import db
from app.eve_models import EveType


class EsiChar(db.Model):
    __tablename__ = 'esi_chars'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    character_id = db.Column(db.BigInteger)
    character_name = db.Column(db.String(255), nullable=False)
    scopes = db.Column(db.String(4095), nullable=False)
    token_type = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'))
    user = db.relationship("User", back_populates="esi_chars")

    access_expiration = db.Column(db.Float, nullable=False)
    refresh_token = db.Column(db.String(255))
    access_token = db.Column(db.String(255))

    skills = db.relationship("EsiSkill", back_populates="esi_char")


class EsiSkill(db.Model):
    __tablename__ = 'esi_skills'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    skillpoints_in_skill = db.Column(db.BigInteger, nullable=False)
    current_skill_level = db.Column(db.Integer, nullable=False)

    esi_char_id = db.Column(db.BigInteger, db.ForeignKey('esi_chars.id'))
    esi_char = db.relationship("EsiChar", back_populates="skills")

    skill_id = db.Column(db.BigInteger, ForeignKey('eve_types.id'), nullable=False)
    type = db.relationship("EveType", lazy="joined", order_by="EveType.name")


class EsiLocation(db.Model):
    __tablename__ = 'esi_locations'
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(255), nullable=False)