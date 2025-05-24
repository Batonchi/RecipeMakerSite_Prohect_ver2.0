from flask import Blueprint, current_app, \
    render_template, request, redirect, jsonify, url_for
from app.web.recipes.forms import RecipeForm, IngredientForm, StepForm
from app.web.recipes.service import RecipeService
from app.base.database import async_session_maker
from app.web.auth.service import get_user_by_token
from app.web.recipes.model import Recipe
from flask_executor import Executor
from werkzeug.exceptions import HTTPException
from sqlalchemy import select
import os
import asyncio

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


@router.route('/get-step-form')
def get_step_form():
    index = request.args.get('index', 0)
    form = RecipeForm()
    return render_template('step_partial.html', step=form.steps.append_entry(), index=index)


@router.route('/get-ingredient-form')
def get_ingredient_form():
    index = request.args.get('index', 0)
    form = RecipeForm()
    return render_template('ingredient_partial.html', ingredient=form.ingredients.append_entry(), index=index)


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


@router.route('/create', methods=['GET', 'POST'])
async def create_recipe():
    form = RecipeForm()

    if request.method == 'GET':
        form.ingredients.entries.clear()
        form.steps.entries.clear()
        form.ingredients.append_entry({
            'number': 1,
            'name': 'Пример ингредиента',
            'for_what': '',
            'quantity': 1
        })
        form.steps.append_entry({
            'number': 1,
            'name': 'Пример шага',
            'description': 'Описание шага',
            'explanations': '',
            'links': [{}]
        })
        return render_template('create_recipe_form.html', form=form)

    if not form.validate():
        current_app.logger.error(f"Form validation failed: {form.errors}")
        return jsonify({
            'success': False,
            'error': 'Пожалуйста, заполните все обязательные поля',
            'details': form.errors
        }), 400

    try:
        current_user = await get_user_by_token()
        if not current_user:
            return jsonify({'success': False, 'error': 'Пользователь не найден'}), 401

        recipe_data = {
            'name': form.name.data,
            'user_id': current_user.id,
            'content': {
                'theme': form.theme.data,
                'description': form.description.data,
                'hashtags': [tag.strip() for tag in form.hashtags.data.split('#') if
                             tag.strip()] if form.hashtags.data else [],
                'categories': form.categories.data,
                'ingredients': [],
                'steps': [],
                'result': form.result.data,
                'use_ai_image': form.use_ai_image.data,
                'use_ai_text': form.use_ai_text.data
            }
        }

        # Обработка ингредиентов
        for i, ingredient in enumerate(form.ingredients):
            recipe_data['content']['ingredients'].append({
                'number': i + 1,
                'name': ingredient.name.data or f"Ингредиент {i + 1}",
                'for_what': ingredient.for_what.data or '',
                'quantity': ingredient.quantity.data or 1
            })

        # Обработка шагов
        for i, step in enumerate(form.steps):
            step_data = {
                'number': i + 1,
                'name': step.name.data or f"Шаг {i + 1}",
                'description': step.description.data or f"Описание шага {i + 1}",
                'explanations': step.explanations.data or '',
                'links': []
            }

            if hasattr(step, 'links'):
                for link in step.links:
                    if link.link.data and link.link_description.data:
                        step_data['links'].append({
                            'link_description': link.link_description.data,
                            'link': link.link.data
                        })

            recipe_data['content']['steps'].append(step_data)

        await RecipeService.add_recipe(**recipe_data)
        return jsonify({
            'success': True,
            'message': 'Рецепт успешно создан!',
            'redirect_url': url_for('recipe.index')
        })

    except Exception as e:
        current_app.logger.error(f"Error creating recipe: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ошибка сервера: ' + str(e)
        }), 500


@router.route('/all_recipes', methods=['GET'])
async def show_recipes():
    category_filter = request.args.getlist('category')

    async with async_session_maker() as session:
        query = select(Recipe)
        if category_filter:
            query = query.where(Recipe.content['categories'].contains(category_filter))
        result = await session.execute(query)
        recipes = result.scalars().all()

    return render_template('all_recipes.html', recipes=recipes, selected_categories=category_filter)
