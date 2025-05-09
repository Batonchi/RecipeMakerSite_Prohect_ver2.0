from flask_restful import Api, Resource
from flask import redirect, Flask
from web_app import create_app
from web_app.support.support_mail import mail_app
from web_app.notification.notification_mail import notification_mail_app
from bots.main import app as bot_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware
import asyncio


main_app = Flask(__name__)
api = Api(main_app)


class HomePage(Resource):
    def get(self):
        return redirect('/recipe')


api.add_resource(HomePage, '/')

web_app = create_app()

main_app.wsgi_app = DispatcherMiddleware(main_app.wsgi_app, {
    '/recipe': web_app,
    '/support/mail': mail_app,
    '/notification/mail': notification_mail_app,
    '/work_with_text_bot': bot_app
})

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    # asyncio для работы с Flask
    asyncio.set_event_loop(loop)
    try:
        main_app.run(debug=True)
    finally:
        loop.close()
