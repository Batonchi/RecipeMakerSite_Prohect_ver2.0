from flask import Blueprint, render_template, request, redirect, make_response, flash
from werkzeug.exceptions import HTTPException
from app.web.auth.forms import LoginForm, RegisterForm
from app.web.auth.service import create_token, hash_password
from app.web.users.service import UserService
from app.base.database import async_session_maker
import os

router = Blueprint('auth', __name__,
                   url_prefix='/auth',
                   static_url_path='/static',
                   static_folder=os.path.abspath('app/web/view/static'),
                   template_folder=os.path.abspath('app/web/view/templates'))


# Декоратор для проверки аутентификации через куки
def login_required(f):
    def wrapper(*args, **kwargs):
        auth_token = request.cookies.get('auth_token')
        if not auth_token:
            flash('Пожалуйста, войдите в систему', 'danger')
            return redirect('/recipe/auth/login')
        return f(*args, **kwargs)

    return wrapper


# Логин
@router.route('/login', methods=['GET'])
async def login_page():
    return render_template('login.html', form=LoginForm())


@router.route('/login', methods=['POST'])
async def login_handler():
    form = LoginForm()

    # если нажата кнопка "создать аккаунт"
    if form.create_account.data:
        return redirect('/recipe/auth/register')

    if not form.validate_on_submit():
        flash("Пожалуйста, заполните все поля корректно.", 'danger')
        return render_template('login.html', form=form)

    try:
        async with async_session_maker() as session:  # сессия
            async with session.begin():
                email = form.email.data
                password = form.password.data
                user = await UserService.get_one_or_none(session, email=email)  # получаем none или юзера (почту)

                if not user or user.password != hash_password(password):  # если что-то не так, то до свидания
                    flash("Неверный email или пароль.", 'danger')
                    return render_template('login.html', form=form)

                # Создаем токен и устанавливаем куки
                token = create_token(email, password)
                response = make_response(redirect('/recipe'))
                response.set_cookie('auth_token', token, httponly=True)
                response.set_cookie('user_id', str(user.id))

                await session.close()
                return response
    except Exception as e:
        print(f"Login error: {e}")
        return render_template('login.html', form=form)


# Регистрация
@router.route('/register', methods=['GET'])
async def register_page():
    return render_template('new_registration.html', form=RegisterForm())


@router.route('/register', methods=['GET', 'POST'])
async def register_handler():
    form = RegisterForm()

    if request.method == 'POST' and form.validate_on_submit():
        print('Форма валидна')
        if form.password.data != form.password_again.data:
            flash("Пароли не совпадают.", 'danger')
            return render_template('new_registration.html', form=form)

        try:
            async with async_session_maker() as session:
                existing_user = await UserService.get_one_or_none(session, email=form.email.data)
                if existing_user:
                    flash("Пользователь с таким email уже существует.", 'danger')
                    return render_template('new_registration.html', form=form)

                new_user = await UserService.insert(
                    session,
                    name=form.name.data,
                    surname=form.surname.data,
                    email=form.email.data,
                    date_of_birth=form.date_of_birth.data,
                    password=hash_password(form.password.data),
                    is_admin=False
                )
                print(new_user)
                flash("Регистрация прошла успешно! Теперь вы можете войти.", 'success')
                return redirect('/recipe/auth/login')

        except Exception as e:
            print(f"Registration error: {e}")
            flash("Произошла ошибка при регистрации.", 'danger')

    return render_template('new_registration.html', form=form)


@router.route('/logout')
async def logout():
    response = make_response(redirect('/'))
    response.delete_cookie('auth_token')
    response.delete_cookie('user_id')

    flash("Вы вышли из системы.", 'info')
    return response
