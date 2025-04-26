# роутер для инициализации сайта; (базовая папка)
import requests
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
    try:
        print("Sending test email...")
        response = requests.get(
            'http://localhost:8000/support_mail//delete_all_emails/pop3',
            timeout=10
        )
        result = response.json()
        print(result)
        return 'DONE'
    except Exception as e:
        return f"Error: {str(e)}", 500
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
