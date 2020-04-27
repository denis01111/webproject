from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Optional


class ProfileForm(FlaskForm):
    email = StringField("Почта", validators=[Optional()])
    password_new = PasswordField('Новый пароль', validators=[Optional()])
    telephone = StringField("Почта", validators=[Optional()])
    img = StringField('Фотография', validators=[Optional()])
    password = PasswordField('Пароль', validators=[Optional()])
    submit = SubmitField('Sign in')
