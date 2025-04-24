from flask_wtf import FlaskForm
import flask_mail
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField, DateField
from wtforms.validators import DataRequired
from base.service import BaseService


class LoginForm(BaseService, FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign In')


class RegisterForm(BaseService, FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    date_of_birth = DateField('Date of birth', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_again = PasswordField('Repeat password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')