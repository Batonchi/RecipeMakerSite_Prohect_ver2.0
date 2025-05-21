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
        form.ingredients.entries.clear()
        form.steps.entries.clear()
        form.ingredients.append_entry()
        form.steps.append_entry()
        return render_template('create_recipe_form.html', form=form)

    if form.validate_on_submit():
        print("Форма валидна, обрабатываем данные...")
        if form.submit.data:
            try:
                current_user = run_async(get_user_by_token())
                print(f"Пользователь: {current_user.id}")

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
                                'number': ingredient.data['number'],
                                'name': ingredient.data['name'],
                                'for_what': ingredient.data['for_what'],
                                'quantity': ingredient.data['quantity']
                            } for ingredient in form.ingredients
                        ],
                        'steps': [
                            {
                                'number': step.data['number'],
                                'name': step.data['name'],
                                'description': step.data['description'],
                                'explanations': step.data['explanations'],
                                'link': step.data['link'],
                                'link_description': step.data['link_description']
                            } for step in form.steps
                        ],
                        'result': form.result.data,
                        'result_link': form.result_link.data,
                        'result_link_description': form.result_link_description.data,
                        'use_ai_image': form.use_ai_image.data,
                        'use_ai_text': form.use_ai_text.data
                    }
                }
                print("Данные для сохранения:", recipe_data)
                future = current_app.executor.submit(
                    run_async,
                    RecipeService.add_recipe(**recipe_data)
                )
                future.result()

                return redirect('/recipe')
            except Exception as e:
                print(f"Ошибка создания рецепта: {e}")
                return render_template('create_recipe_form.html', form=form, error="Не удалось создать рецепт")
        elif form.cancel.data:
            return redirect('/create')
    return render_template('create_recipe_form.html', form=form)
