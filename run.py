from flask_restful import Api, Resource
from flask import redirect, Flask
from app.web import create_app
from app.web.support.support_mail import mail_app
from app.web.notification.notification_mail import notification_mail_app
# from app.web.main import app as web_app_init
# from app.bots.main import app as bot_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware
import asyncio


main_app = Flask(__name__)
api = Api(main_app)


class HomePage(Resource):
    def get(self):
        return redirect('/recipe')


class Health(Resource):
    def get(self):
        return {'status': 'healthy'}, 200


api.add_resource(HomePage, '/')
api.add_resource(Health, '/health')

web_app_init = create_app()

main_app.wsgi_app = DispatcherMiddleware(main_app.wsgi_app, {
    '/recipe': web_app_init,
    '/support/mail': mail_app,
    '/notification/mail': notification_mail_app,
    '/work_with_text_bot': web_app_init
})

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    # asyncio для работы с Flask
    asyncio.set_event_loop(loop)
    try:
        main_app.run(debug=True, host='0.0.0.0', port=5000)
    finally:
        loop.close()
