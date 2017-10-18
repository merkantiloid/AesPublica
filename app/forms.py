from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, ValidationError
from .models import User
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
