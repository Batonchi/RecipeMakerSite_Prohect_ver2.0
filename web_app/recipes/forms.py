from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FieldList, FormField,\
    FileField, SubmitField, BooleanField, SelectMultipleField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange
from wtforms.widgets import TextArea


# Вложенная форма для ингредиентов
class IngredientForm(FlaskForm):
    number = IntegerField('Номер', validators=[DataRequired(), NumberRange(min=1)])
    name = StringField('Название', validators=[DataRequired()])
    for_what = StringField('Для чего', validators=[Length(max=255)])
    quantity = IntegerField('Количество', validators=[DataRequired()])


# Вложенная форма для этапа
class StepForm(FlaskForm):
    number = IntegerField('Номер', validators=[DataRequired(), NumberRange(min=1)])
    name = StringField('Название этапа', validators=[DataRequired(), Length(max=255)])
    description = TextAreaField('Описание этапа', validators=[DataRequired()])
    explanations = TextAreaField('Пояснения', validators=[DataRequired()])
    images = FileField('Картинки', render_kw={"multiple": True})  # для загрузки нескольких картинок
    link = StringField('Ссылка', validators=[DataRequired()])
    link_description = StringField('Описание ссылки', validators=[DataRequired()])


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
    result_link = StringField('Ссылка на результат', validators=[DataRequired()])
    result_link_description = StringField('Описание ссылки на результат', validators=[DataRequired()])
    use_ai_image = BooleanField('Использовать нейросеть для генерации фото', validators=[DataRequired()])
    use_ai_text = BooleanField('Использовать нейросети для проверки и улучшения текста', validators=[DataRequired()])
    cancel = SubmitField('Отменить')
    submit = SubmitField('Создать')
