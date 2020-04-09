from flask import Flask, render_template, redirect, request, make_response, session, abort, jsonify
from flask_wtf import FlaskForm
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired
from data import db_session, users
from loginform import LoginForm
from register import RegisterForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    sessions = db_session.create_session()
    return sessions.query(users.User).get(user_id)


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


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        sessions = db_session.create_session()
        user = sessions.query(users.User).filter(users.User.email == form.email.data).first()
        if user and user.password == form.password.data:
            login_user(user, remember=form.remember_me.data)
            return redirect('/')
        return render_template('login.html', message='Неправильный логин или пароль', form=form)
    return render_template('login.html', title='Авторизация', form=form)


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
