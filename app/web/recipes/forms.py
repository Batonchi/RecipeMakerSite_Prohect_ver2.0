from flask_wtf import FlaskForm
from flask_wtf.file import MultipleFileField
from wtforms import StringField, TextAreaField, FieldList, FormField, \
    FileField, SubmitField, BooleanField, SelectMultipleField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange, Optional
from wtforms.widgets import TextArea


class LinkForm(FlaskForm):
    link_description = StringField('Описание ссылки', validators=[DataRequired()])
    link = StringField('Ссылка', validators=[DataRequired()])


# Вложенная форма для ингредиентов
class IngredientForm(FlaskForm):
    number = IntegerField('Номер', validators=[DataRequired(), NumberRange(min=1)], default=1)
    name = StringField('Название', validators=[DataRequired()], default="")
    for_what = StringField('Для чего', validators=[Length(max=255)], default="")
    quantity = IntegerField('Количество', validators=[DataRequired(), NumberRange(min=1)], default=1)


# Вложенная форма для этапа
class StepForm(FlaskForm):
    number = IntegerField('Номер', validators=[DataRequired(), NumberRange(min=1)], default=1)
    name = StringField('Название этапа', validators=[DataRequired(), Length(max=255)], default="")
    description = TextAreaField('Описание этапа', validators=[DataRequired()], default="")
    explanations = TextAreaField('Пояснения', validators=[DataRequired()], default="")
    images = MultipleFileField('Картинки')
    links = FieldList(FormField(LinkForm), min_entries=1)  # Добавить FieldList для ссылок


# Форма рецепта
class RecipeForm(FlaskForm):
    name = StringField('Название рецепта', validators=[DataRequired()])
    theme = TextAreaField('О чем; тема', validators=[DataRequired()], widget=TextArea())
    description = TextAreaField('Описание', validators=[DataRequired()], widget=TextArea())
    hashtags = TextAreaField('Хэштеги (#text)', validators=[DataRequired()], widget=TextArea())
    categories = SelectMultipleField('Категория рецепта', choices=['Шаблоны', 'Алгоритмы', 'Инфографики', 'Кулинария',
                                                                   'Чертежи', 'Другое'], validators=[DataRequired()])
    ingredients = FieldList(FormField(IngredientForm), min_entries=1)
    steps = FieldList(FormField(StepForm), min_entries=1)
    result = TextAreaField('Результат', validators=[DataRequired()], widget=TextArea())
    links = FieldList(FormField(LinkForm), min_entries=1)
    use_ai_image = BooleanField('Использовать нейросеть для генерации фото', validators=[Optional()], default=False)
    use_ai_text = BooleanField('Использовать нейросети для проверки и улучшения текста', validators=[Optional()],
                               default=False)
    cancel = SubmitField('Отменить')
    submit = SubmitField('Создать')
