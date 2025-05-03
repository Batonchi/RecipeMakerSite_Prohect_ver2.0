from flask_restful import Api, Resource
from flask import redirect, Flask
from web_app.support.support_mail import mail_app
from web_app.notification.notification_mail import notification_mail_app
from web_app.main import app as web_app
from bots.main import app as bot_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware


app = Flask(__name__)
api = Api(app)


class HomePage(Resource):
    def get(self):
        return redirect('/recipe')


api.add_resource(HomePage, '/')


app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/recipe': web_app,
    '/support/mail': mail_app,
    '/notification/mail': notification_mail_app,
    '/work_with_text_bot': bot_app
})

if __name__ == '__main__':
    app.run(debug=True)
