from web_app.main import app as web_app
from bots.main import app as bot_app
from starlette.applications import Starlette
from web_app.support.support_mail import mail_app
from starlette.routing import Mount, Route
from starlette.middleware.wsgi import WSGIMiddleware
from starlette.responses import RedirectResponse
from asgiref.wsgi import WsgiToAsgi
from base.constant import PORT, HOST


web_app_asgi = WSGIMiddleware(web_app)
bot_app_asgi = WSGIMiddleware(bot_app)
mail_app_asgi = WSGIMiddleware(mail_app)


async def homepage(request):
    return RedirectResponse('/recipe')


app = Starlette(
    routes=[
        Route("/", homepage),
        Mount("/recipe", web_app_asgi),
        Mount("/generate_image", bot_app_asgi),
        Mount("/support/mail", mail_app_asgi),
    ]
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=8000)