import json
import uuid
import os
import asyncio
import logging

from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from app.web.recipes.forms import RecipeForm, IngredientForm, StepForm, LinkForm
from app.web.recipes.service import RecipeService
from app.base.database import async_session_maker
from flask import Blueprint, current_app, \
    render_template, request, redirect, jsonify, url_for
from app.web.recipes.forms import RecipeForm, IngredientForm, StepForm
from app.web.recipes.service import RecipeService
from app.base.database import async_session_maker
from app.web.auth.service import get_user_by_token
from app.web.recipes.model import Recipe
from flask_executor import Executor
from werkzeug.exceptions import HTTPException
from flask import jsonify
from app.base.constant import ALLOWED_EXTENSIONS, IMAGE_FOLDER, MAX_CONTENT_LENGTH


logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="w")

router = Blueprint('form', __name__,
                   url_prefix='/form',
                   static_folder='/static',
                   static_url_path=os.path.abspath('app/web/view/static'),
                   template_folder=os.path.abspath('app/web/view/templates'))


@router.route('/')
def index():
    return "Главная страница рецептов"


@router.route('/graph')
def graphic_show():
    return render_template('graphic_form.html')


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def ensure_image_folder_exists():
    os.makedirs(IMAGE_FOLDER, exist_ok=True)


@router.route('/upload-images', methods=['POST'])
def upload_images():
    ensure_image_folder_exists()

    if 'images' not in request.files:
        return jsonify({'error': 'No files uploaded'}), 400

    files = request.files.getlist('images')
    step_index = request.form.get('step_index')

    filenames = []
    for file in files:
        if file.filename == '':
            continue

        if file and allowed_file(file.filename):
            # Генерируем уникальное имя файла
            ext = file.filename.rsplit('.', 1)[1].lower()
            filename = f"{uuid.uuid4().hex}.{ext}"
            filepath = os.path.join(IMAGE_FOLDER, filename)

            try:
                file.save(filepath)
                filenames.append(filename)
            except Exception as e:
                current_app.logger.error(f"Error saving file: {str(e)}")
                continue

    return jsonify({'filenames': filenames})


@router.route('/delete-image', methods=['POST'])
def delete_image():
    data = request.get_json()
    filename = data.get('filename')

    if not filename:
        return jsonify({'error': 'Filename required'}), 400

    try:
        filepath = os.path.join(IMAGE_FOLDER, filename)
        if os.path.exists(filepath):
            os.remove(filepath)
            return jsonify({'success': True})
        return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        current_app.logger.error(f"Error deleting file: {str(e)}")
        return jsonify({'error': str(e)}), 500


@router.route('/get-ingredient-form')
def get_ingredient_form():
    index = request.args.get('index', 0, type=int)
    form = RecipeForm()
    ingredient = form.ingredients.append_entry()

    # Устанавливаем пустую строку вместо None
    if ingredient.for_what.data is None:
        ingredient.for_what.data = ''

    return render_template('ingredient_partial.html',
                           ingredient=ingredient,
                           index=index)


@router.route('/get-step-form')
def get_step_form():
    index = request.args.get('index', 0, type=int)
    form = RecipeForm()
    step = form.steps.append_entry()

    # Добавляем только одну ссылку по умолчанию
    if not step.links.entries:
        step.links.append_entry()

    return render_template('step_partial.html', step=step, index=index)


@router.route('/get-link-form')
def get_link_form():
    step_index = request.args.get('step_index', 0)
    link_index = request.args.get('link_index', 0)
    form = RecipeForm()
    return render_template('link_partial.html', link=form.steps[0].links.append_entry(), step_index=step_index,
                           link_index=link_index)


@router.route('/get-recipe-link-form')
def get_recipe_link_form():
    link_index = request.args.get('link_index', 0)
    form = RecipeForm()
    link = form.links.append_entry()  # Добавляем новую запись в FieldList
    return render_template('recipe_link_partial.html', link_index=link_index)


def run_async(coro):  # функция для асинхронного запуска корутины.
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


@router.route('/create', methods=['POST', 'GET'])
async def create_recipe():
    form = RecipeForm()

    if request.method == 'GET':
        form = RecipeForm()
        # Добавляем начальные записи с пустыми данными
        if len(form.ingredients) == 0:
            ingredient = form.ingredients.append_entry()
            ingredient.form.name.data = ""
            ingredient.form.number.data = 1
            ingredient.form.quantity.data = 1

        if len(form.steps) == 0:
            step = form.steps.append_entry()
            step.form.name.data = ""
            step.form.description.data = ""
            step.form.number.data = 1

        if len(form.links) == 0:
            form.links.append_entry()

        return render_template('create_recipe_form.html', form=form)

    if request.method == 'POST':
        try:
            # Получаем данные формы
            form_data = request.form.to_dict()

            # Обрабатываем изображения
            images_data = {}
            for key, value in form_data.items():
                if key.endswith('-image-filenames') and value:
                    step_index = key.split('-')[1]
                    images_data[f'steps-{step_index}-images'] = json.loads(value)

            # Собираем данные рецепта
            recipe_data = {
                'name': form.name.data,
                'user_id': 0,  # Замените на реальный ID пользователя
                'content': {
                    'theme': form.theme.data,
                    'description': form.description.data,
                    'hashtags': [tag.strip() for tag in form.hashtags.data.split('#') if tag.strip()],
                    'categories': form.categories.data,
                    'ingredients': [
                        {
                            'number': ingredient.form.number.data,
                            'name': ingredient.form.name.data,
                            'for_what': ingredient.form.for_what.data or '',
                            'quantity': ingredient.form.quantity.data
                        } for ingredient in form.ingredients
                    ],
                    'steps': [
                        {
                            'number': step.form.number.data,
                            'name': step.form.name.data,
                            'description': step.form.description.data,
                            'explanations': step.form.explanations.data,
                            'images': images_data.get(f'steps-{i}-images', []),
                            'links': [
                                {
                                    'link_description': link.form.link_description.data,
                                    'link': link.form.link.data
                                } for link in step.links
                            ]
                        } for i, step in enumerate(form.steps)
                    ],
                    'result': form.result.data,
                    'use_ai_image': form.use_ai_image.data,
                    'use_ai_text': form.use_ai_text.data
                }
            }

            recipe_id = await RecipeService.add_recipe(**{
                'user_id': 0,
                'name': recipe_data['name'],
                'content': recipe_data
            })

            return jsonify({
                'success': True,
                'message': 'Рецепт успешно создан',
                'redirect': url_for('form.graphic_show')
            })

        except Exception as e:
            current_app.logger.error(f'Error: {str(e)}', exc_info=True)
            return jsonify({
                'success': False,
                'message': 'Внутренняя ошибка сервера'
            }), 500
