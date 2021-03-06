﻿from flask import Flask, render_template, redirect, request, make_response, session, abort, jsonify
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
import os
from werkzeug.utils import secure_filename
import PIL
from PIL import Image
from flask import Flask

arr_category = ["Электроника", 'Дом', 'Книги', 'Мужчинам', 'Подарки', 'Зоотовары', 'Спорт',
                'Автотовары']
product_add_one = {'Категория': '', 'Название': '', 'Описание': '', 'Изображение': '', 'Цена': '',
                   'Количесвто': ''}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_session.global_init('db/blogs.sqlite')
    sessions = db_session.create_session()
    return sessions.query(users.User).get(user_id)


@app.route('/electronics', methods=['GET', 'POST'])
def electronics():
    try:
        db_session.global_init('db/blogs.sqlite')
        sessions = db_session.create_session()
        products = sessions.query(product.Product).filter(product.Product.category == 'Электроника')
        return render_template("product_display.html", products=products)
    except:
        return 'There was a problem deleting that task'


@app.route('/health', methods=['GET', 'POST'])
def health():
    try:
        db_session.global_init('db/blogs.sqlite')
        sessions = db_session.create_session()
        products = sessions.query(product.Product).filter(product.Product.category == 'Здоровье')
        return render_template("product_display.html", products=products)
    except:
        return 'There was a problem deleting that task'


@app.route('/men', methods=['GET', 'POST'])
def men():
    try:
        db_session.global_init('db/blogs.sqlite')
        sessions = db_session.create_session()
        products = sessions.query(product.Product).filter(product.Product.category == 'Мужчинам')
        return render_template("product_display.html", products=products)
    except:
        return 'There was a problem deleting that task'


@app.route('/prize', methods=['GET', 'POST'])
def prize():
    try:
        db_session.global_init('db/blogs.sqlite')
        sessions = db_session.create_session()
        products = sessions.query(product.Product).filter(product.Product.category == 'Подарки')
        return render_template("product_display.html", products=products)
    except:
        return 'There was a problem deleting that task'


@app.route('/cat', methods=['GET', 'POST'])
def cat():
    try:
        db_session.global_init('db/blogs.sqlite')
        sessions = db_session.create_session()
        products = sessions.query(product.Product).filter(product.Product.category == 'Зоотовары')
        return render_template("product_display.html", products=products)
    except:
        return 'There was a problem deleting that task'


@app.route('/home', methods=['GET', 'POST'])
def home():
    try:
        db_session.global_init('db/blogs.sqlite')
        sessions = db_session.create_session()
        products = sessions.query(product.Product).filter(product.Product.category == 'Дом')
        return render_template("product_display.html", products=products)
    except:
        return 'There was a problem deleting that task'


@app.route('/books', methods=['GET', 'POST'])
def books():
    try:
        db_session.global_init('db/blogs.sqlite')
        sessions = db_session.create_session()
        products = sessions.query(product.Product).filter(product.Product.category == 'Книги')
        return render_template("product_display.html", products=products)
    except:
        return 'There was a problem deleting that task'


@app.route('/sport', methods=['GET', 'POST'])
def sport():
    try:
        db_session.global_init('db/blogs.sqlite')
        sessions = db_session.create_session()
        products = sessions.query(product.Product).filter(product.Product.category == 'Спорт')
        return render_template("product_display.html", products=products)
    except:
        return 'There was a problem deleting that task'


@app.route('/car', methods=['GET', 'POST'])
def car():
    db_session.global_init('db/blogs.sqlite')
    sessions = db_session.create_session()
    products = sessions.query(product.Product).filter(product.Product.category == 'Автотовары')
    return render_template("product_display.html", products=products)


@app.route('/')
def delete():
    db_session.global_init('db/blogs.sqlite')
    sessions = db_session.create_session()
    products = sessions.query(product.Product)
    return render_template("product_display.html", products=products, title='Главная')


@app.route('/exit')
def logout():
    logout_user()
    return redirect('/')


@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    form = AddProductForm()
    if request.method == 'POST':
        db_session.global_init('db/blogs.sqlite')
        sessions = db_session.create_session()
        products = product.Product()
        if form.category.data in arr_category:
            product_add_one['Категория'] = form.category.data
            return render_template('name_product.html', form=form)

        if form.name.data:
            product_add_one['Название'] = form.name.data
            return render_template('about_product.html', form=form)

        if form.about.data:
            product_add_one['Описание'] = form.about.data
            return render_template('img_product.html', form=form)

        if form.img.data:
            names = 'static/img/'
            profiles = request.files['img']
            image_location = names + str(len(sessions.query(product.Product.id).all()) + 1) + '.png'

            profiles.save(image_location)
            base_height = 100
            img = Image.open(image_location)
            height_cent = (base_height / float(img.size[1]))
            weight_size = int((float(img.size[0]) * float(height_cent)))
            img = img.resize((weight_size, base_height), PIL.Image.ANTIALIAS)
            img.save(image_location)
            product_add_one['Изображение'] = image_location
            return render_template('count_product.html', form=form)

        if form.count.data:
            try:
                trues = int(form.count.data)
                product_add_one['Количество'] = form.count.data
                return render_template('price_product.html', form=form)
            except:
                return render_template('count_product.html', title='Добавление продукта',
                                       form=form,
                                       message="Вы ввели некоректно колличество!")

        if form.cost.data:
            try:
                trues = int(form.cost.data)
                product_add_one['Цена'] = form.cost.data
                products.name = product_add_one['Название']
                products.img = product_add_one['Изображение']
                products.add_to_basket_id = '/add_in_basket/' + \
                                            str(len(sessions.query(product.Product.id).all()) + 1)
                products.about = product_add_one['Описание']
                products.cost = product_add_one['Цена']
                products.category = product_add_one['Категория']
                products.count = product_add_one['Количество']
                sessions.add(products)
                sessions.commit()
                product_add_one.clear()
            except:
                return render_template('price_product.html', title='Добавление продукта',
                                       form=form,
                                       message="Вы ввели некоректно цену")
        return redirect('/')
    return render_template('add_product.html', title='Добавление продукта', form=form)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    db_session.global_init('db/blogs.sqlite')
    sessions = db_session.create_session()
    user = sessions.query(users.User).filter(users.User.id == current_user.get_id()).first()
    return render_template('Profile.html', title='Авторизация', user=user)


@app.route('/profile_update', methods=['GET', 'POST'])
def profile_update():
    form = ProfileForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            db_session.global_init('db/blogs.sqlite')
            sessions = db_session.create_session()
            user = sessions.query(users.User).filter(users.User.id == current_user.get_id()).first()
            if user.password != form.password.data:
                return render_template('profile_update.html', title='Редактирование профиля',
                                       form=form,
                                       message='Неправильный пароль!')
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
        return render_template('profile_update.html', title='Обновление профиля', form=form,
                               message='')
    return render_template('profile_update.html', title='Авторизация', form=form, message='')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        db_session.global_init('db/blogs.sqlite')
        if len(form.password.data) < 8:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Короткий пароль!")
        if 'qwerty' in form.password.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароль содержит всем известную комбинацию 'qwerty'!")
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        sessions = db_session.create_session()
        if sessions.query(users.User).filter(users.User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = users.User(
            name=form.name.data,
            email=form.email.data,
            password=form.password.data
        )
        user.set_password(form.password.data)
        sessions.add(user)
        sessions.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_session.global_init('db/blogs.sqlite')
        sessions = db_session.create_session()
        user = sessions.query(users.User).filter(users.User.email == form.email.data).first()
        if user and user.password == form.password.data:
            login_user(user, remember=form.remember_me.data)
            return redirect('/')
        return render_template('login.html', message='Неправильный логин или пароль', form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/add_in_basket/<int:post_id>', methods=['GET', 'POST'])
def add_in_basket(post_id):
    db_session.global_init('db/blogs.sqlite')
    sessions = db_session.create_session()
    result_product = sessions.query(product.Product).filter(product.Product.id == post_id).first()
    result_user = sessions.query(users.User).filter(users.User.id == current_user.id).first()
    if result_user.id_product == None:
        list_basket_id_product = []
        list_basket_count_product = []
    else:
        list_basket_id_product = str(result_user.id_product).split()
        list_basket_count_product = str(result_user.count_product).split()
    if str(post_id) in list_basket_id_product:
        list_basket_count_product[list_basket_id_product.index(str(post_id))] = str(
            int(list_basket_count_product[list_basket_id_product.index(str(post_id))]) + 1)
        result_user.count_product = ' '.join(list_basket_count_product)
    else:
        list_basket_id_product.append(str(post_id))
        list_basket_count_product.append('1')
        result_user.count_product = ' '.join(list_basket_count_product)
        result_user.id_product = ' '.join(list_basket_id_product)
    sessions.commit()
    return redirect('/')


@app.route('/basket', methods=['GET', 'POST'])
def basket():
    db_session.global_init('db/blogs.sqlite')
    sessions = db_session.create_session()
    result_user = sessions.query(users.User).filter(users.User.id == current_user.id).first()
    if result_user.id_product == None or len(str(result_user.id_product).split()) == 0:
        return render_template('orders_false.html', title='Корзина')
    else:
        list_basket_id_product = str(result_user.id_product).split()
        list_basket_count_product = str(result_user.count_product).split()
    list_product = []
    for i in list_basket_id_product:
        list_product.append(sessions.query(product.Product).filter(
            product.Product.id == i).first())
    all_articles = list(map(lambda x, y: [x, y], list_product, list_basket_count_product))
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


@app.route('/del_basket/<int:post_id>', methods=['GET', 'POST'])
def del_basket(post_id):
    db_session.global_init('db/blogs.sqlite')
    sessions = db_session.create_session()
    result_product = sessions.query(product.Product).filter(product.Product.id == post_id).first()
    result_user = sessions.query(users.User).filter(users.User.id == current_user.id).first()
    if result_user.id_product == None:
        list_basket_id_product = []
        list_basket_count_product = []
    else:
        list_basket_id_product = str(result_user.id_product).split()
        list_basket_count_product = str(result_user.count_product).split()
        index = list_basket_id_product.index(str(post_id))
        list_basket_count_product[index] = str(int(list_basket_count_product[index]) - 1)
    if int(list_basket_count_product[index]) <= 0:
        del list_basket_id_product[index]
        del list_basket_count_product[index]
    result_user.count_product = ' '.join(list_basket_count_product)
    result_user.id_product = ' '.join(list_basket_id_product)
    sessions.commit()
    return redirect('/basket')


@app.route('/session_test')
def session_test():
    session.permanent = True
    session['visits_count'] = session.get('visits_count', 0) + 1
    return f"Вы зашли на страницу {session['visits_count']} раз!"


@app.route('/del_product_admin/<int:post_id>', methods=['GET', 'POST'])
def del_product_admin(post_id):
    db_session.global_init('db/blogs.sqlite')
    sessions = db_session.create_session()
    result_product = sessions.query(product.Product).filter(product.Product.id == post_id).first()
    if result_product:
        sessions.delete(result_product)
        sessions.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/arrange', methods=['GET', 'POST'])
def arrange():
    form = Decoration()
    if form.validate_on_submit():
        if request.method == 'POST':
            db_session.global_init('db/blogs.sqlite')
            sessions = db_session.create_session()
            decor = order.Order()
            decor.name = form.name.data
            decor.surname = form.surname.data
            decor.telephone = form.telephone.data
            decor.email = form.email.data
            result_user = sessions.query(users.User).filter(
                users.User.id == current_user.id).first()
            if result_user.id_product == None:
                list_basket_id_product = []
            else:
                list_basket_id_product = str(result_user.id_product).split()
                list_basket_count_product = str(result_user.count_product).split()
                decor.products = result_user.id_product
            decor.address = form.address.data
            if result_user.id_product != None:
                for id_1 in str(result_user.id_product).split():
                    pro = sessions.query(product.Product).filter(
                        product.Product.id == id_1).first()
                    if pro:
                        a = int(pro.count) - int(
                            list_basket_count_product[list_basket_id_product.index(id_1)])
                        if a < 0:
                            return render_template('orders.html', title='Оформление заказа',
                                                   form=form,
                                                   message='Такого колличества {} нет в наличии.'
                                                           ' Уменьшите колличество или выберите'
                                                           ' другой товар'.format(pro.name))
                        else:
                            pro.count = a
                    else:
                        return render_template('orders.html', title='Оформление заказа', form=form,
                                               message='Товар не найден')
            result_user.id_product = ''
            result_user.count_product = ''
            sessions.add(decor)
            sessions.commit()
        return render_template('orders_true.html', title='Оформление заказа')
    return render_template('orders.html', title='Оформление заказа', form=form)


@app.route('/about_our')
def about_our():
    return render_template('about_our.html', title='О нас')


@app.route('/error_login_in')
def error_login_in():
    db_session.global_init('db/blogs.sqlite')
    sessions = db_session.create_session()
    products = sessions.query(product.Product)
    return render_template('product_display.html', message='Вы не авторизованы!', products=products)


def main():
    db_session.global_init('db/blogs.sqlite')
    app.run()


if __name__ == '__main__':
    main()
