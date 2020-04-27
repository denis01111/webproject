from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField
from wtforms.validators import DataRequired, Optional


class ProfileForm(FlaskForm):
    email = StringField("Почта", validators=[Optional()])
    password_new = PasswordField('Новый пароль', validators=[Optional()])
    telephone = StringField("Почта", validators=[Optional()])
    img = FileField('Фотография', validators=[Optional()])
    password = PasswordField('Пароль', validators=[Optional()])
    city = StringField("Город", validators=[Optional()])
    submit = SubmitField('Изменить')
