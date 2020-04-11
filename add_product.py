from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, MultipleFileField
from wtforms.validators import DataRequired


class AddProductForm(FlaskForm):
    name = StringField("Название прордукта", validators=[DataRequired()])
    size = MultipleFileField('File(s) Upload')
    img_product = MultipleFileField('File(s) Upload')
    cost = StringField("Цена", validators=[DataRequired()])
    submit = SubmitField('Добавить')