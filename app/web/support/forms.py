from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length

'''
Админ - получает
Пользователь - отправляет
'''


'''model.py, mail.py base service, users model'''
'''flask-wtf с bootstraps'''
# окно, где предоставляется базовая информация об админе (USERS), есть функция рассылки, есть окно получения и обработки
# Запросов от пользователей из таблицы Complaint


class ComplaintForm(FlaskForm):
    text = TextAreaField('Текст жалобы',
                        validators=[
                            DataRequired(message='Поле не может быть пустым'),
                            Length(min=10, max=500, message='Жалоба должна быть от 10 до 500 символов')
                        ])
    is_solved = BooleanField('Проблема решена?', default=False)
    submit = SubmitField('Отправить жалобу')