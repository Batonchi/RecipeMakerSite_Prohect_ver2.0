import datetime
import requests
from flask import Flask, render_template, request, redirect, url_for, make_response
from sqlalchemy.future import select
from base.constant import HOST, PORT, SECRET_KEY
from web_app.users.model import User, UserToken
from web_app.users.service import UserService
from base.database import async_session_maker
from web_app.auth.service import hash_password, create_token
from web_app.auth.forms import LoginForm, RegisterForm
from dotenv import load_dotenv
from web_app.auth.router import router as auth_router
import os


app = Flask(__name__, static_url_path='/web_app/view/static', template_folder='view')
app.secret_key = SECRET_KEY
app.register_blueprint(auth_router)


@app.route('/')
def main_page():
    try:
        print("Sending test email...")
        response = requests.get(
            'http://localhost:8000/support_mail//delete_all_emails/pop3',
            timeout=10
        )
        result = response.json()
        print(result)
        return 'DONE'
    except Exception as e:
        return f"Error: {str(e)}", 500


# @app.route('/login')
# def login_page():
#     form = LoginForm()
#     return render_template('login.html', form=form)


# @app.route('/login', methods=['GET', 'POST'])
# async def login():
#     form = LoginForm()
#     if request.method == 'POST' and form.validate_on_submit():
#         async with async_session_maker() as session:  # создание сессии
#             """Проверяем пароль и почту; создаем токен"""
#             result1 = await session.execute(select(User).where(User.email == form.email.data))
#             result2 = await session.execute(select(User).where(User.password == hash_password(form.password.data)))
#             user = result1.scalars().first()
#             if user and result2.scalars().first():
#                 # # Создаем новый токен и сохраняем его в базе данных
#                 #
#                 # response = make_response(redirect(url_for('main_page')))
#                 # response.set_cookie('auth_token', token, httponly=True)
#                 return response
#             else:
#                 return render_template('login.html', form=form, message="Почта или пароль введены неверно.")
#     return render_template('login.html', form=form)


# @app.route('/register', methods=['GET', 'POST'])
# async def register():
#     form = RegisterForm()  # форма регистрации
#     if request.method == 'POST' and form.validate_on_submit():
#         if form.password.data != form.password_again.data:
#             return render_template('reg.html', form=form, message="Пароли не совпадают")
#         async with async_session_maker() as session:  # создание сессии
#             result = await session.execute(select(User).where(User.email == form.email.data))
#             if result.scalars().first():
#                 return render_template('reg.html', form=form, message="Такой пользователь уже существует")
#         await UserService.insert(**{
#             "name": form.name.data,
#             "surname": form.surname.data,
#             'created_date': datetime.datetime.now(),
#             'last_visit_date': datetime.datetime.now(),
#             'email': form.email.data,
#             'date_of_birth': form.date_of_birth.data,
#             'password': hash_password(form.password.data)
#         })  # добавляем нового пользователя в таблицу, бд
#         return redirect('/web/login')
#     return render_template('reg.html', form=form)
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
