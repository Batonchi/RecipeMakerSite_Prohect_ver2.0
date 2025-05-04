from flask import Blueprint, render_template, request, redirect, url_for
from app.web.recipes.forms import RecipeForm, IngredientForm, StepForm
from app.web.recipes.service import RecipeService
from app.base.database import async_session_maker

router = Blueprint('recipes', __name__,
                   url_prefix='/recipe',
                   static_folder='..web_app/view/static',
                   template_folder='..web_app/view/')


@router.route('/create', methods=['POST', 'GET'])
async def create_recipe():
    form = RecipeForm()
    if request.method == 'GET':
        print('in')
        # Явно инициализируем FieldList с одним пустым экземпляром каждой вложенной формы
        form = RecipeForm(ingredients=[IngredientForm()], steps=[StepForm()])
    if request.method == 'POST':
        if form.validate_on_submit():
            if form.submit.data:  # Проверяем, была ли нажата кнопка "Создать"
                # Сбор данных из формы
                recipe_data = {
                    'name': form.name.data,
                    'content': {
                        'theme': form.theme.data,
                        'description': form.description.data,
                        'hashtags': form.hashtags.data.split('#') if form.hashtags.data else [],  # Разделяем хэштеги
                        'categories': form.categories.data,
                        'ingredients': [
                            {
                                'number': i.data['number'],
                                'name': i.data['name'],
                                'purpose': i.data['purpose'],
                                'quantity': i.data['quantity'],
                            } for i in form.ingredients
                        ],
                        'steps': [
                            {
                                'number': s.data['number'],
                                'name': s.data['name'],
                                'description': s.data['description'],
                                'explanation': s.data['explanation'],
                                'image_url': s.data['image_url'],
                                'link': s.data['link'],
                                'link_description': s.data['link_description'],
                            } for s in form.steps
                        ],
                        'result': form.result.data,
                        'result_link': form.result_link.data,
                        'result_link_description': form.result_link_description.data,
                        'use_ai_image': form.use_ai_image.data,
                        'use_ai_text': form.use_ai_text.data,
                    }
                    # user_id:
                    # 'user_id': current_user.id
                }

                # Добавление рецепта в базу данных
                await RecipeService.insert(**recipe_data)

                # Перенаправление после успешного создания
                return redirect('main_page')
            elif form.cancel.data:  # Проверяем, была ли нажата кнопка "Отменить"
                return redirect('/create')
    return render_template('recipe.html', form=form)

