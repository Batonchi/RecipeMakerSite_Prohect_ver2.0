import flask
from flask import Flask, render_template, request, redirect, make_response
from werkzeug.exceptions import HTTPException
from app.web.auth.forms import LoginForm, RegisterForm
from app.web.auth.service import create_token, hash_password
from app.web.users.service import UserService


router = flask.Blueprint('auth', __name__,
                         url_prefix='/auth',
                         static_folder='..web/view/static',
                         template_folder='..web/view/')

@router.get('/login')
async def login_page():
    return render_template('login.html', form=LoginForm())


@router.post('/login')
async def login():
    form = LoginForm()

    if form.create_account.data:
        return redirect('/recipe/auth/register')

    if form.validate_on_submit():
        try:
            email = request.form.get('email')
            password = request.form.get('password')
            user = await UserService.get_one_or_none(email=email)
            if not user or user.password != hash_password(password):
                return render_template('login.html', form=form, message="Вы допустили ошибку в вводимых данных.")
            token = create_token(email, password)
            response = make_response(redirect('/recipe'))
            response.set_cookie('auth_token', token, httponly=True)
            return response
        except Exception as e:
            print(f"Login error: {e}")
            return render_template('login.html', form=form, message="Произошла ошибка при входе.")


@router.get('/logout')
async def logout():
    response = make_response(redirect('/'))
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
    try:
        await UserService.insert(
            **{
                "name": form.name.data,
                "surname": form.surname.data,
                'email': form.email.data,
                'date_of_birth': form.date_of_birth.data,
                'password': hash_password(form.password.data)
            }
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=409)
    return redirect('/auth/login')

