from flask import Flask, render_template, redirect, request, make_response, session, abort, jsonify
from flask_wtf import FlaskForm
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired
from data import db_session, users, product
from loginform import LoginForm
from register import RegisterForm
from add_product import AddProductForm
import zipfile
import os
from product import products


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
    return render_template('clothes.html', title='Одежда',
                           products=products['Одежда'])


@app.route('/shoes')
def shoes():
    return render_template('shoes.html', title='Обувь',
                           products=products['Обувь'])


@app.route('/electronics', methods=['GET', 'POST'])
def electronics():
    return render_template('electronics.html', title='Электроника',
                           products=products['Электроника'])


@app.route('/health', methods=['GET', 'POST'])
def health():
    return render_template('health.html', title='Здоровье',
                           products=products['Здоровье'])


@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html', title='Дом',
                           products=products['Дом'])


@app.route('/books', methods=['GET', 'POST'])
def books():
    return render_template('books.html', title='Книги',
                           products=products['Книги'])


@app.route('/jewelry', methods=['GET', 'POST'])
def jewelry():
    return render_template('jewelry.html', title='Ювелирные изделия',
                           products=products['Ювелирные изделия'])


@app.route('/girls', methods=['GET', 'POST'])
def girls():
    return render_template('girls.html', title='Женщинам',
                           products=products['Женщинам'])


@app.route('/sport', methods=['GET', 'POST'])
def sport():
    return render_template('sport.html', title='Спорт',
                           products=products['Спорт'])


@app.route('/car', methods=['GET', 'POST'])
def car():
    return render_template('car.html', title='Автотовары',
                           products=products['Автотовары'])


@app.route('/')
def delete():
    try:
        return render_template('base.html', title="Магазин")
    except:
        return 'There was a problem deleting that task'


@app.route('/exit')
def logout():
    logout_user()
    return redirect('/')


@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    form = AddProductForm()
    print(form.validate_on_submit())
    if form.validate_on_submit():
        session = db_session.create_session()
        add_product = AddProductForm()
        add_product.name = form.name.data
        add_product.cost = form.cost.data
        add_product.img_product = '123'
        add_product.size = '123'
        add_product.product_category = '123'
        current_user.news.append(add_product)
        session.merge(current_user)
        session.commit()
        return redirect('/')
    return render_template('add_product.html', title='Добавление новости',
                           form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    print(form.errors)
    print(form.validate_on_submit())
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


def main():
    db_session.global_init('db/blogs.sqlite')
    app.run()


if __name__ == '__main__':
    main()
