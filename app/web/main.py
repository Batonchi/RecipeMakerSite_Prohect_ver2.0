from flask import Flask
from app.web.auth.router import router as auth_router
from app.base.constant import SECRET_KEY
import os


app = Flask(__name__, static_url_path='/web/view/static', template_folder='view')
app.secret_key = SECRET_KEY
app.register_blueprint(auth_router)


@app.route('/', methods=['GET', 'POST'])
def index():
    return 'hi'


