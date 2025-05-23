from flask import Blueprint, render_template, request, redirect, url_for
from app.web.recipes.forms import RecipeForm, IngredientForm, StepForm
from app.web.recipes.service import RecipeService
from app.base.database import async_session_maker
from flask import Blueprint, current_app, \
    render_template, request, redirect
from app.web.recipes.forms import RecipeForm, IngredientForm, StepForm
from app.web.recipes.service import RecipeService
from app.base.database import async_session_maker
from app.web.auth.service import get_user_by_token
from flask_executor import Executor
from werkzeug.exceptions import HTTPException
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
        while form.ingredients:
            form.ingredients.pop_entry()
        while form.steps:
            form.steps.pop_entry()
        while form.links:
            form.links.pop_entry()

        form.ingredients.append_entry()
        step = form.steps.append_entry()
        # Добавляем только одну ссылку по умолчанию
        step.links.append_entry()
        form.links.append_entry()

        return render_template('create_recipe_form.html', form=form)

    if request.method == 'POST':
        form = RecipeForm(request.form)
        if not form.validate():
            return render_template('create_recipe_form.html', form=form, error="Проверьте заполнение полей")

        try:
            current_user = run_async(get_user_by_token())
            recipe_data = {
                'name': form.name.data,
                'user_id': current_user.id,
                'content': {
                    'theme': form.theme.data,
                    'description': form.description.data,
                    'hashtags': [tag.strip() for tag in form.hashtags.data.split('#') if tag.strip()],
                    'categories': form.categories.data,
                    'ingredients': [
                        {
                            'number': ingredient.number.data,
                            'name': ingredient.name.data,
                            'for_what': ingredient.for_what.data or '',  # Пустая строка вместо None
                            'quantity': ingredient.quantity.data
                        } for ingredient in form.ingredients
                    ],
                    'steps': [
                        {
                            'number': step.number.data,
                            'name': step.name.data,
                            'description': step.description.data,
                            'explanations': step.explanations.data,
                            'links': [
                                {
                                    'link_description': link.link_description.data,
                                    'link': link.link.data
                                } for link in step.links
                            ]
                        } for step in form.steps
                    ],
                    'result': form.result.data,
                    'use_ai_image': form.use_ai_image.data,
                    'use_ai_text': form.use_ai_text.data
                }
            }
            future = current_app.executor.submit(run_async, RecipeService.add_recipe(**recipe_data))
            future.result()
            return redirect(url_for('recipe.index'))
        except Exception as e:
            print(f"Ошибка создания рецепта: {e}")
            return render_template('create_recipe_form.html', form=form, error=str(e))
