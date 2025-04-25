# роутер для инициализации сайта; (базовая папка)
from flask import Flask, render_template, request, redirect, url_for
from base.constant import HOST, PORT
from dotenv import load_dotenv
# from web_app.auth.router import router as auth_router
import os


app = Flask(__name__,
            static_url_path='/web_app/view/static',
            template_folder='/web_app/view')

# app.register_blueprint(auth_router)




@app.route('/')
def main_page():
    return 'hi'
#
#
# @app.route('/contact')
# def contact_page():
#     pass
#
#
# @app.route('/about')
# def about_page():
#     pass
#
#
# @app.route('/send_complaint')
# def send_request():
#     pass