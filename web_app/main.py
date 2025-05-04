from flask import Flask
from web_app.auth.router import router as auth_router
from web_app.recipes.router import router as recipe_router
from base.constant import SECRET_KEY
import os


app = Flask(__name__, static_url_path='/web_app/view/static', template_folder='view')
app.secret_key = SECRET_KEY
app.register_blueprint(auth_router)
app.register_blueprint(recipe_router)


@app.route('/', methods=['GET', 'POST'])
def index():
    return 'hi'


