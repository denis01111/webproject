from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, MultipleFileField,\
    FileField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class AddProductForm(FlaskForm):
    name = StringField("Название прордукта", validators=[DataRequired()])
    cost = StringField("Цена", validators=[DataRequired()])
    img = FileField("Фотография", validators=[DataRequired()])
    category = StringField("Категория", validators=[DataRequired()])
    about = StringField("Описание товара", validators=[DataRequired()])
    submit = SubmitField('Добавить')
