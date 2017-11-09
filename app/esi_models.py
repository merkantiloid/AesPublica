from app import db


class EsiChar(db.Model):
    __tablename__ = 'esi_chars'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    character_id = db.Column(db.BigInteger)
    character_name = db.Column(db.String(255), nullable=False)
    expires_on = db.Column(db.String(31), nullable=False)
    scopes = db.Column(db.String(4095), nullable=False)
    token_type = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'))
    user = db.relationship("User", back_populates="esi_chars")
    refresh_token = db.Column(db.String(255))
    code = db.Column(db.String(255))


