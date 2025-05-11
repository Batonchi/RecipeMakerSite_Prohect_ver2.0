from flask import Flask
from flask_executor import Executor
from app.base.constant import SECRET_KEY


def create_app():
    app = Flask(__name__,
                static_url_path='/web_app_init/view/static',
                template_folder='view')
    app.secret_key = SECRET_KEY

    # Инициализируем эту хрень для асинхронных задач
    executor = Executor(app)
    app.executor = executor

    # Импорт и регистрация blueprint'ов
    from app.web.auth.router import router as auth_router
    from app.web.recipes.router import router as recipe_router

    app.register_blueprint(auth_router)
    app.register_blueprint(recipe_router)

    return app
