from web_app.main import app as web_app
from bot.main import app as bot_app
from starlette.applications import Starlette
from starlette.routing import Mount
from starlette.middleware.wsgi import WSGIMiddleware
from asgiref.wsgi import WsgiToAsgi
from base.constant import PORT, HOST


app = Starlette(
    routes=[
        Mount("/web", WsgiToAsgi(web_app)),
        Mount("/bot", WsgiToAsgi(bot_app)),
    ]
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=8000)
