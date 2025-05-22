from flask import Flask, render_template
from app.base.constant import SECRET_KEY
from app.web.recipes.forms import RecipeForm

import os


def create_app():
    app = Flask(__name__,
                static_url_path='/static',
                static_folder=os.path.abspath('app/web/view/static'),
                template_folder=os.path.abspath('app/web/view/templates'))

    app.secret_key = SECRET_KEY

    # Импорт и регистрация blueprint'ов
    from app.web.auth.router import router as auth_router
    from app.web.recipes.router import router as recipes_router
    from app.web.support.router import router as support_router

    # app.register_blueprint(admin_router)
    app.register_blueprint(auth_router)
    app.register_blueprint(recipes_router)
    app.register_blueprint(support_router)

    @app.route('/', methods=['GET', 'POST'])
    def index():
        return render_template('create_recipe_form.html', form=RecipeForm(), title='Создание Рецепта')

    return app
