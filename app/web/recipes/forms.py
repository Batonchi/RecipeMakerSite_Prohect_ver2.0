from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FieldList, FormField, \
    FileField, SubmitField, BooleanField, SelectMultipleField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange, Optional
from wtforms.widgets import TextArea


class LinkForm(FlaskForm):
    class Meta:
        csrf = False
    link_description = StringField('Описание ссылки', validators=[DataRequired()])
    link = StringField('Ссылка', validators=[DataRequired()])


# Вложенная форма для ингредиентов
class IngredientForm(FlaskForm):
    class Meta:
        csrf = False
    number = IntegerField('Номер', validators=[DataRequired(), NumberRange(min=1)], default=1)
    name = StringField('Название', validators=[DataRequired()], default="")
    for_what = StringField('Для чего', validators=[Optional()], default="")
    quantity = IntegerField('Количество', validators=[DataRequired(), NumberRange(min=1)], default=1)


class StepForm(FlaskForm):
    class Meta:
        csrf = False
    number = IntegerField('Номер', validators=[DataRequired(), NumberRange(min=1)], default=1)
    name = StringField('Название этапа', validators=[DataRequired()], default="")
    description = TextAreaField('Описание этапа', validators=[DataRequired()], default="")
    explanations = TextAreaField('Пояснения', validators=[Optional()], default="")
    links = FieldList(FormField(LinkForm), min_entries=1, default=[{}])


# Форма рецепта
class RecipeForm(FlaskForm):
    name = StringField('Название рецепта', validators=[DataRequired()], default="name")
    theme = TextAreaField('О чем; тема', validators=[DataRequired()], widget=TextArea(), default="theme")
    description = TextAreaField('Описание', validators=[DataRequired()], widget=TextArea(), default='description')
    hashtags = TextAreaField('Хэштеги (#text)', validators=[DataRequired()], widget=TextArea(), default='#recipe')
    categories = SelectMultipleField('Категория рецепта', choices=['Шаблоны', 'Алгоритмы', 'Инфографики', 'Кулинария',
                                                                   'Чертежи', 'Другое'], validators=[DataRequired()],
                                     default=['Другое'])
    ingredients = FieldList(FormField(IngredientForm), min_entries=1)
    steps = FieldList(FormField(StepForm), min_entries=1)
    result = TextAreaField('Результат', validators=[DataRequired()], widget=TextArea())
    links = FieldList(FormField(LinkForm), min_entries=1)
    use_ai_image = BooleanField('Использовать нейросеть для генерации фото', validators=[DataRequired()])
    use_ai_text = BooleanField('Использовать нейросети для проверки и улучшения текста', validators=[DataRequired()])
    cancel = SubmitField('Отменить')
    submit = SubmitField('Создать')
