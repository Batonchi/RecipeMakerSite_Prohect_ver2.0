from flask import Flask
from flask_executor import Executor
from base.constant import SECRET_KEY


def create_app():
    app = Flask(__name__,
                static_url_path='/web_app/view/static',
                template_folder='view')
    app.secret_key = SECRET_KEY

    # Инициализируем эту хрень для асинхронных задач
    executor = Executor(app)
    app.executor = executor

    # Импорт и регистрация blueprint'ов
    from web_app.auth.router import router as auth_router
    from web_app.recipes.router import router as recipe_router

    app.register_blueprint(auth_router)
    app.register_blueprint(recipe_router)

    return app