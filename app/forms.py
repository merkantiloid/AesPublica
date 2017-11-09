from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField
from wtforms.validators import DataRequired, ValidationError
from .models import User, OreCalc
from app import db
import bcrypt


class LoginForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

    def validate_name(form, field):
        user = User.query.filter(User.name == field.data).first()
        if not user:
            raise ValidationError('Invalid name')

    def validate_password(form, field):
        user = User.query.filter(User.name == form.name).first()
        if user and not bcrypt.hashpw(field.data.encode(), user.hash.encode()) == user.hash.encode():
            raise ValidationError('Invalid password')


class RegisterForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])


class SettingsForm(FlaskForm):
    space = StringField('space', validators=[DataRequired()])
    citadel_id = IntegerField('citadel_id', validators=[DataRequired()])
    character_id = IntegerField('character_id', validators=[DataRequired()])
    implant_id = IntegerField('implant_id', validators=[DataRequired()])
    rig1_id = IntegerField('rig1_id', validators=[DataRequired()])

    def save(self, user):
        model = OreCalc.query.filter(OreCalc.user_id == user.id).first()
        if model:
            model.space = self.space.data
            model.citadel_id = self.citadel_id.data
            model.character_id = self.character_id.data
            model.implant_id = self.implant_id.data
            model.rig1_id = self.rig1_id.data
            db.session.add(model)
            db.session.commit()
