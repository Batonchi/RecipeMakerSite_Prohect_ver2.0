import hashlib
from jose import JWTError, jwt
from werkzeug.exceptions import HTTPException
from app.web.users.service import UserService
from app.base.constant import *
from flask import request
from app.base.database import async_session_maker


def create_token(email: str, password: str):
    data = {"email": email, "password": password}
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


def hash_password(password: str):
    alg = hashlib.sha256()
    alg.update(password.encode())
    return alg.hexdigest()


async def get_user_by_token():
    token = request.cookies.get('auth_token')
    if not token:
        raise HTTPException(status_code=409, detail="Пожалуйста войдите в аккаунт!")
    try:
        data = jwt.decode(token, SECRET_KEY, ALGORITHM)

        async with async_session_maker() as session:
            user = await UserService.get_one_or_none(
                session,
                email=data['email'],
                password=hash_password(data['password'])
            )
            if not user:
                raise HTTPException(status_code=409, detail="Пользователь не найден!")
            return user
    except Exception as e:
        raise HTTPException(status_code=409, detail="Ошибка авторизации")


async def get_admin_by_token():
    user = await get_user_by_token()
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="У вас нет доступа!")
    return user
