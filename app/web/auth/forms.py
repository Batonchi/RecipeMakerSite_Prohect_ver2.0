from flask_wtf import FlaskForm
from flask import request
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField, DateField
from wtforms.validators import DataRequired
from base.service import BaseService


class LoginForm(BaseService, FlaskForm):
    email = EmailField('Почта', validators=[])
    password = PasswordField('Пароль', validators=[])
    remember_me = BooleanField('Запомнить меня')
    create_account = SubmitField('Создать аккаунт')
    submit = SubmitField('Войти')

    def validate(self, extra_validators=None):
        # Если нажата кнопка 'создать аккаунт', то пропускаем валидацию
        if 'create_account' in request.form:
            return True
        # Для кнопки 'Войти' добавляем валидацию
        self.email.validators = [DataRequired()]
        self.password.validators = [DataRequired()]
        return super().validate(extra_validators)


class RegisterForm(BaseService, FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    date_of_birth = DateField('Дата рождения', validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')
