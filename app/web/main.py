from flask import Flask, render_template
from app.web.auth.router import router as auth_router
from app.base.constant import SECRET_KEY
from app.web.recipes.router import router as recipes_router
import os

app = Flask(__name__,
            static_url_path='/static',
            static_folder=os.path.abspath('app/web/view/static'),
            template_folder=os.path.abspath('app/web/view/templates'))


app.secret_key = SECRET_KEY

app.register_blueprint(auth_router)
app.register_blueprint(recipes_router)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('graphic_form.html')


if __name__ == '__main__':
    app.run(debug=True)
