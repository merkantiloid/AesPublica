from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField
from wtforms.validators import DataRequired, ValidationError
from .models import User, OreCalc
from app.extensions import db  # Импорт из extensions
import bcrypt


class LoginForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

    def validate_name(form, field):
        user = User.query.filter(User.name == field.data).first()
        if not user:
            raise ValidationError('Invalid name')

    def validate_password(form, field):
        user = User.query.filter(User.name == form.name.data).first()
        if user and not bcrypt.hashpw(field.data.encode(), user.hash.encode()) == user.hash.encode():
            raise ValidationError('Invalid password')


class RegisterForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

    def validate_name(form, field):
        user = User.query.filter(User.name==field.data).first()
        if user:
            raise ValidationError('Name already taken')

class SettingsForm(FlaskForm):
    space = StringField('space', validators=[DataRequired()])
    citadel_id = IntegerField('citadel_id', validators=[DataRequired()])
    esi_char_id = IntegerField('esi_char_id', validators=[DataRequired()])
    implant_id = IntegerField('implant_id', validators=[DataRequired()])
    rig1_id = IntegerField('rig1_id', validators=[DataRequired()])
    rig2_id = IntegerField('rig2_id', validators=[DataRequired()])
    rig3_id = IntegerField('rig3_id', validators=[DataRequired()])

    def save(self, user):
        model = user.ore_calc
        if model:
            model.space = self.space.data
            model.citadel_id = self.citadel_id.data
            model.esi_char_id = self.esi_char_id.data
            model.implant_id = self.implant_id.data
            model.rig1_id = self.rig1_id.data
            model.rig2_id = self.rig2_id.data
            model.rig3_id = self.rig3_id.data
            db.session.add(model)
            db.session.commit()


class BuildItemForm(FlaskForm):
    type_id = IntegerField('type_id', validators=[DataRequired()])
    me = IntegerField('me', validators=[DataRequired()])
    te = IntegerField('te', validators=[DataRequired()])
    qty = IntegerField('qty', validators=[DataRequired()])