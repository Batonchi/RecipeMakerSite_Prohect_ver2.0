import uuid
import os
import shutil

import flask
from flask import render_template, request, redirect, url_for
from typing import Optional
from starlette.exceptions import HTTPException
from datetime import date
from web_app.auth.service import create_token, hash_password
from web_app.users.service import UserService

router = flask.Blueprint('auth', __name__,
                         url_prefix='/auth',
                         static_folder='..web_app/view/static',
                         template_folder='..web_app/view/')


@router.get('/login')
async def login_page(req: request):
    return render_template('login.html', {'request': req})


# @router.get('/logout')
# async def logout(request: Request):
#     pass
#
#
# @router.post('/login')
# async def login(response: Response, email: str, password: str):
#     user = await UserService.get_one_or_none(email=email, password=hash_password(password))
#     if not user:
#         raise HTTPException(status_code=409, detail="Пользователь не найден! Неверный логин или пароль!")
#     token = create_token(email, password)
#     response.set_cookie("token", token, httponly=True)
#     return user.user_id
#
#
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
