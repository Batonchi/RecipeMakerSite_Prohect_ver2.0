from flask_restful import Api, Resource
from flask import redirect, Flask
from app.web.support.support_mail import mail_app
from app.web.notification.notification_mail import notification_mail_app
from app.web.main import app as web_app
from app.bots.main import app as bot_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware


app = Flask(__name__)
api = Api(app)


class HomePage(Resource):
    def get(self):
        return redirect('/recipe')


class Health(Resource):
    def get(self):
        return {'status': 'healthy'}, 200


api.add_resource(HomePage, '/')
api.add_resource(Health, '/health')


app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/recipe': web_app,
    '/support/mail': mail_app,
    '/notification/mail': notification_mail_app,
    '/work_with_text_bot': bot_app
})
#
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
