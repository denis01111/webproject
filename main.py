from flask import Flask, render_template, redirect, request, make_response, session, abort, jsonify
from flask_wtf import FlaskForm
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired
from data import db_session, users, product, order
from loginform import LoginForm
from register import RegisterForm
from add_product import AddProductForm
from decoration_orders import Decoration
from Profile import ProfileForm
import zipfile
import os
from werkzeug.utils import secure_filename
import PIL
from PIL import Image

arr_category = ['Одежда', 'Обувь', 'Электроника', 'Здоровье', 'Дом', 'Книги', 'Ювелирные изделия'
                'Спорт', 'Автотовары']

product_add_one = {'Категория': '', 'Название': '', 'Описание': '', 'Изображение': '', 'Размер': '',
                   'Цена': ''}

arr_to_basket = {}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    sessions = db_session.create_session()
    return sessions.query(users.User).get(user_id)


@app.route('/clothes', methods=['GET', 'POST'])
def clothes():
    try:
        sessions = db_session.create_session()
        products = sessions.query(product.Product).filter(product.Product.category == 'Одежда')
        return render_template("product_display.html", products=products)
    except:
        return 'There was a problem deleting that task'


@app.route('/shoes')
def shoes():
    try:
        sessions = db_session.create_session()
        products = sessions.query(product.Product).filter(product.Product.category == 'Обувь')
        return render_template("product_display.html", products=products)
    except:
        return 'There was a problem deleting that task'


@app.route('/electronics', methods=['GET', 'POST'])
def electronics():
    try:
        sessions = db_session.create_session()
        products = sessions.query(product.Product).filter(product.Product.category == 'Электроника')
        return render_template("product_display.html", products=products)
    except:
        return 'There was a problem deleting that task'


@app.route('/health', methods=['GET', 'POST'])
def health():
    try:
        sessions = db_session.create_session()
        products = sessions.query(product.Product).filter(product.Product.category == 'Здоровье')
        return render_template("product_display.html", products=products)
    except:
        return 'There was a problem deleting that task'


@app.route('/home', methods=['GET', 'POST'])
def home():
    try:
        sessions = db_session.create_session()
        products = sessions.query(product.Product).filter(product.Product.category == 'Дом')
        return render_template("product_display.html", products=products)
    except:
        return 'There was a problem deleting that task'


@app.route('/books', methods=['GET', 'POST'])
def books():
    try:
        sessions = db_session.create_session()
        products = sessions.query(product.Product).filter(product.Product.category == 'Книги')
        return render_template("product_display.html", products=products)
    except:
        return 'There was a problem deleting that task'


@app.route('/jewelry', methods=['GET', 'POST'])
def jewelry():
    try:
        sessions = db_session.create_session()
        products = sessions.query(product.Product).filter(product.Product.category
                                                          == 'Ювелирные изделия')
        return render_template("product_display.html", products=products)
    except:
        return 'There was a problem deleting that task'


@app.route('/sport', methods=['GET', 'POST'])
def sport():
    try:
        sessions = db_session.create_session()
        products = sessions.query(product.Product).filter(product.Product.category == 'Спорт')
        return render_template("product_display.html", products=products)
    except:
        return 'There was a problem deleting that task'


@app.route('/car', methods=['GET', 'POST'])
def car():
    try:
        sessions = db_session.create_session()
        products = sessions.query(product.Product).filter(product.Product.category == 'Автотовары')
        return render_template("product_display.html", products=products)
    except:
        return 'There was a problem deleting that task'


@app.route('/')
def delete():
    try:
        sessions = db_session.create_session()
        print(1)
        products = sessions.query(product.Product)
        print(2)
        return render_template("product_display.html", products=products, title='Главная')
    except:
        return 'There was a problem deleting that task'


@app.route('/exit')
def logout():
    logout_user()
    return redirect('/')


@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    form = AddProductForm()
    if request.method == 'POST':
        sessions = db_session.create_session()
        products = product.Product()
        if form.category.data not in arr_category and product_add_one['Категория'] == '':
            return render_template('add_product.html', title='Добавление продукта',
                                   form=form,
                                   message="Такой категории не существует!")

        if form.category.data in arr_category:
            product_add_one['Категория'] = form.category.data
            return render_template('name_product.html', form=form)

        if form.name.data and product_add_one['Категория']:
            product_add_one['Название'] = form.name.data
            return render_template('about_product.html', form=form)

        if form.about.data and product_add_one['Категория']:
            product_add_one['Описание'] = form.about.data
            return render_template('img_product.html', form=form)

        if form.img.data and product_add_one['Категория']:
            a = 'static/img/'
            profile = request.files['img']
            image_location = a + str(len(sessions.query(product.Product.id).all()) + 1) + '.png'
            profile.save(image_location)
            baseheight = 100
            img = Image.open(image_location)
            hpercent = (baseheight / float(img.size[1]))
            wsize = int((float(img.size[0]) * float(hpercent)))
            img = img.resize((wsize, baseheight), PIL.Image.ANTIALIAS)
            img.save(image_location)
            product_add_one['Изображение'] = image_location
            return render_template('size_product.html', form=form)

        if form.size.data and product_add_one['Категория']:
            product_add_one['Размер'] = form.size.data
            return render_template('price_product.html', form=form)

        if form.cost.data and product_add_one['Категория']:
            print(int(form.cost.data))
            try:
                trues = int(form.cost.data)
                product_add_one['Цена'] = form.cost.data
                products.name = product_add_one['Название']
                products.img = product_add_one['Изображение']
                products.add_to_basket_id = '/add_in_basket/' + \
                                            str(len(sessions.query(product.Product.id).all()) + 1)

                products.cost = product_add_one['Цена']
                products.category = product_add_one['Категория']
                sessions.add(products)
                sessions.commit()
            except:
                return render_template('price_product.html', title='Добавление продукта',
                                       form=form,
                                       message="Вы ввели некоректные данные!")
        return redirect('/')
    return render_template('add_product.html', title='Добавление продукта', form=form)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    sessions = db_session.create_session()
    user = sessions.query(users.User).filter(users.User.id == current_user.get_id()).first()
    return render_template('Profile.html', title='Авторизация',user=user)

@app.route('/profile_update', methods=['GET', 'POST'])
def profile_update():
    form = ProfileForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            sessions = db_session.create_session()
            user = sessions.query(users.User).filter(users.User.id == current_user.get_id()).first()
            if user.password != form.password.data:
                return render_template('profile_update.html', title='Обновление профиля', form=form, message='Не правильный пароль')
            if form.email.data != '':
                user.email = form.email.data
            if form.password_new.data != '':
                user.password = form.password_new.data
            if form.telephone.data != '':
                user.telephone = form.telephone.data
            if form.city.data != '':
                user.city = form.city.data
            sessions.add(user)
            sessions.commit()
            return render_template('profile.html', title='Обновление профиля', form=form,
                                   message='Данные успешно изменены', user=user)
        return render_template('profile_update.html', title='Обновление профиля', form=form, message='')
    return render_template('profile_update.html', title='Авторизация', form=form, message='')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(users.User).filter(users.User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = users.User(
            name=form.name.data,
            email=form.email.data,
            password=form.password.data
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    print(form.validate_on_submit())
    if form.validate_on_submit():
        sessions = db_session.create_session()
        user = sessions.query(users.User).filter(users.User.email == form.email.data).first()
        if user and user.password == form.password.data:
            login_user(user, remember=form.remember_me.data)
            return redirect('/')
        return render_template('login.html', message='Неправильный логин или пароль', form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/browse_product/<int:post_id>/', methods=['GET', 'POST'])
def browse_product(post_id):
    sessions = db_session.create_session()
    products = sessions.query(product.Product).filter(product.Product.id == post_id).first()
    print(products)
    return render_template("browse_product.html", products=products)


@app.route('/add_in_basket/<int:post_id>', methods=['GET', 'POST'])
def add_in_basket(post_id):
    sessions = db_session.create_session()
    result = sessions.query(product.Product).filter(product.Product.id == post_id).first()
    arr_to_basket[post_id] = result
    return redirect('/')


@app.route('/basket', methods=['GET', 'POST'])
def basket():
    all_articles = list(arr_to_basket.values())
    return render_template('basket.html', title='Корзина', products=all_articles)


@app.route("/cookie_test")
def cookie_test():
    visits_count = int(request.cookies.get("visits_count", 0))
    if visits_count:
        res = make_response(f'Вы пришли на эту страницу {visits_count + 1} раз')
        res.set_cookie("visits_count", str(visits_count + 1), max_age=60 * 60 * 24 * 365 * 2)
    else:
        res = make_response('Вы пришли на эту страницу в первый раз за 2 года')
        res.set_cookie("visits_count", "1", max_age=60 * 60 * 24 * 365 * 2)
    return res


@app.route('/session_test')
def session_test():
    session.permanent = True
    session['visits_count'] = session.get('visits_count', 0) + 1
    return f"Вы зашли на страницу {session['visits_count']} раз!"


@app.route('/arrange', methods=['GET', 'POST'])
def arrange():
    form = Decoration()
    if form.validate_on_submit():
        if request.method == 'POST':
            sessions = db_session.create_session()
            decor = order.Order()
            decor.name = form.name.data
            decor.surname = form.surname.data
            decor.telephone = form.telephone.data
            decor.email = form.email.data
            decor.products = ', '.join([str(i) for i in arr_to_basket])
            decor.address = form.address.data
            sessions.add(decor)
            sessions.commit()
        return redirect('/')
    return render_template('orders.html', title='Оформление заказа', form=form)


def main():
    db_session.global_init('db/blogs.sqlite')
    app.run(debug=True)


if __name__ == '__main__':
    main()
