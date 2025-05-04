from flask_wtf import FlaskForm
import flask_mail
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField, DateField
from wtforms.validators import DataRequired
from app.base.service import BaseService


class LoginForm(BaseService, FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegisterForm(BaseService, FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    date_of_birth = DateField('Дата рождения', validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')
