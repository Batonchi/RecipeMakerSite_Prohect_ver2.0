from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length


class ComplaintForm(FlaskForm):
    text = TextAreaField('Текст жалобы',
                        validators=[
                            DataRequired(message='Поле не может быть пустым'),
                            Length(min=10, max=500, message='Жалоба должна быть от 10 до 500 символов')
                        ])
    is_solved = BooleanField('Проблема решена?', default=False)
    submit = SubmitField('Отправить жалобу')


class BroadcastForm(FlaskForm):
    subject = StringField('Тема рассылки',
                         validators=[DataRequired()])
    message = TextAreaField('Сообщение',
                          validators=[
                              DataRequired(),
                              Length(min=10, max=2000)
                          ])
    submit = SubmitField('Отправить рассылку')
