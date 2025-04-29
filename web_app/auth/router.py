import uuid
import os
import shutil
import datetime
import flask
from flask import Flask, render_template, request, redirect, url_for, make_response
from typing import Optional
from starlette.exceptions import HTTPException
from datetime import date
from web_app.auth.forms import LoginForm, RegisterForm
from web_app.auth.service import create_token, hash_password
from web_app.users.service import UserService

router = flask.Blueprint('auth', __name__,
                         url_prefix='/auth',
                         static_folder='..web_app/view/static',
                         template_folder='..web_app/view/')


@router.get('/login')
async def login_page():
    return render_template('login.html', form=LoginForm())


@router.post('/login')
async def login():
    email = request.form.get('email')
    password = request.form.get('password')
    user = await UserService.get_one_or_none(email=email)
    if not user or user.password != hash_password(password):
        return render_template('login.html', form=LoginForm(), message="Invalid credentials")
    token = create_token(email, password)
    response = make_response(redirect(url_for('main_page')))
    response.set_cookie('auth_token', token, httponly=True)
    return response


@router.get('/logout')
async def logout():
    response = make_response(redirect(url_for('auth.login_page')))
    response.delete_cookie('auth_token')
    return response


@router.get('/register')
async def register_page():
    return render_template('reg.html', form=RegisterForm())


@router.post('/register')
async def register():
    form = RegisterForm()
    if form.password.data != form.password_again.data:
        return render_template('reg.html', form=form, message="Пароли не совпадают.")
    email = form.email.data
    existing_user = await UserService.get_one_or_none(email=email)
    if existing_user:
        return render_template('reg.html', form=form, message="Такой пользователь уже существует.")

    await UserService.insert(
        **{
            "name": form.name.data,
            "surname": form.surname.data,
            'created_date': datetime.datetime.now(),
            'last_visit_date': datetime.datetime.now(),
            'email': form.email.data,
            'date_of_birth': form.date_of_birth.data,
            'password': hash_password(form.password.data)
        }
    )
    return redirect(url_for('auth.login_page'))


# @router.post('/registration')
# async def registration(first_name: str, last_name: str, email: str, password: str, special_word: str):
#     avatar_uuid = uuid.uuid4()
#     path = os.path.join('app/view/static/images/avatars/', f'{avatar_uuid}.png')
#     shutil.copy('app/view/static/images/profile/default.png', path)
#     try:
#         await UserService.insert(first_name=first_name, last_name=last_name, email=email,
#                                  password=hash_password(password),
#                                  special_word=special_word)
#     except Exception as ex:
#         print(ex)
#         raise HTTPException(status_code=409)
#
#
# @router.get('/registration')
# async def register_page(request: Request):
#     return templates.TemplateResponse('registration.html', {'request': request})
#
#
# @router.get('/login/token')
# async def login_with_token(request: Request):
#     return templates.TemplateResponse('login_with_token.html', {'request': request})
#
#
# @router.get('/successfully')
# async def successful_page(request: Request):
#     return templates.TemplateResponse('add_special_word.html', {'request': request})
