from flask import Blueprint, current_app, \
    render_template, request, redirect
from web_app.recipes.forms import RecipeForm, IngredientForm, StepForm
from web_app.recipes.service import RecipeService
from base.database import async_session_maker
from web_app.auth.service import get_user_by_token
from flask_executor import Executor
from starlette.exceptions import HTTPException
import asyncio

router = Blueprint('recipes', __name__,
                   url_prefix='/recipe',
                   static_folder='..web_app/view/static',
                   template_folder='..web_app/view/')


@router.route('/')
def index():
    return "Главная страница рецептов"


def run_async(coro):  # функция для асинхронного запуска корутины.
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


@router.route('/create', methods=['POST', 'GET'])
async def create_recipe():
    # Get-запросы = просто отобразить форму
    if request.method == 'GET':
        form = RecipeForm(ingredients=[IngredientForm()], steps=[StepForm()])
        return render_template('recipe.html', form=form)

    form = RecipeForm()
    if form.validate_on_submit():
        print("Форма валидна, обрабатываем данные...")
        if form.submit.data:
            try:
                current_user = run_async(get_user_by_token())
                print(f"Пользователь: {current_user.id}")

                # Подготовка данных рецепта
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
                # Используем executor для асинхронных операций
                future = current_app.executor.submit(
                    run_async,
                    RecipeService.add_recipe(**recipe_data)
                )
                future.result()

                return redirect('/recipe')
            except Exception as e:
                print(f"Ошибка создания рецепта: {e}")
                return render_template('recipe.html', form=form, error="Не удалось создать рецепт")
        elif form.cancel.data:  # Проверяем, была ли нажата кнопка "Отменить"
            return redirect('/create')
    return render_template('recipe.html', form=form)

