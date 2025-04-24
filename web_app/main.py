# роутер для инициализации сайта; (базовая папка)
from flask import Flask, render_template, request, redirect, url_for
from base.constant import HOST, PORT, SECRET_KEY
from web_app.users.model import User
from base.database import async_session_maker
from dotenv import load_dotenv
from web_app.auth.router import router as auth_router
import os

from web_app.auth.forms import LoginForm, RegisterForm


app = Flask(__name__, static_url_path='/web_app/view/static', template_folder='view')

app.secret_key = SECRET_KEY
# app.register_blueprint(auth_router)


@app.route('/')
def main_page():
    return 'hi'


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        '''Здесь я создаю сессию и проверяю пароль с почту; работа с бд'''
        return redirect(url_for('main_page'))
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('reg.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        '''создаем сессию бд и проверяем: есть ли такой пользователь с такой почтой'''
        # session =
        # if :
        #     return render_template('reg.html', title='Регистрация',
        #                            form=form,
        #                            message="Такой пользователь уже есть")
        # user = User(
        #     name=form.name.data,
        #     surname=form.surname.data,
        #     created_date='',
        #     last_visit_date='',
        #     date_of_birth=form.date_of_birth.data,
        #     email=form.email.data,
        # )
        # user.set_password(form.password.data)
        # session.add(user)
        # session.commit()
        return redirect('/login')
    return render_template('reg.html', title='Sign Up', form=form)
#
#
# @app.route('/contact')
# def contact_page():
#     pass
#
#
# @app.route('/about')
# def about_page():
#     pass
#
#
# @app.route('/send_complaint')
# def send_request():
#     pass
