from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, MultipleFileField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class AddProductForm(FlaskForm):
    name = StringField("Название прордукта", validators=[DataRequired()])
    size = MultipleFileField('File(s) Upload')
    img_product = MultipleFileField('File(s) Upload')
    cost = StringField("Цена", validators=[DataRequired()])
    product_category = StringField("категория", validators=[DataRequired()])
    submit = SubmitField('Добавить')
