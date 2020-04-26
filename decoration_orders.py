from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, MultipleFileField,\
    FileField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class Decoration(FlaskForm):
    name = StringField("Имя", validators=[DataRequired()])
    surname = StringField("Фамилия", validators=[DataRequired()])
    telephone = StringField("Телефон", validators=[DataRequired()])
    email = StringField("Почта", validators=[DataRequired()])
    address = StringField("Адрес доставки", validators=[DataRequired()])
    submit = SubmitField('Оформить заказ')
