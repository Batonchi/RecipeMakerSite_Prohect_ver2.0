from flask import render_template, jsonify, Response
from flask_mail import Mail, Message
from flask import Flask
from typing import Tuple, Union


class ServerMailVariants:
    SMTP_SERVER = {'server': 'smtp.mail.ru', 'port_ssl': 465}
    POP3_SERVER = {'server': 'pop.mail.ru', 'port_ssl': 995}
    IMAP_SERVER = {'server': 'imap.mail.ru', 'port_ssl': 993}


class MailClient:
    USERNAME: str
    PASSWORD: str

    def __init__(self, **data):
        self.mail_app = Flask(__name__)
        self.mail_app.config.MAIL_USERNAME = data['USERNAME']
        self.mail_app.config.MAIL_PASSWORD = data['PASSWORD']
        self.mail_app.config.MAIL_USE_TLS = False
        self.mail_app.config.MAIL_USE_SSL = True
        self.mail = None

    def get_app(self):
        return self.mail_app

    def send_mail(self, to: Union[str, list], body: Tuple[str, str], subject: str = 'Оповещение')\
            -> Union[Response, Tuple[Response, int]]:
        try:
            msg = Message(subject, sender=self.mail_app.config['USERNAME'],
                          recipients=([to] if isinstance(to, str) else list(map(str, to))))
            if body[1] == 'string':
                msg.body = body[0]
            elif body[1] == 'html':
                msg.body = render_template(body[0])
            self.mail.send(msg)
            return jsonify({'status': 'success', 'message': 'DONE'})
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500


class BaseSMPTMailClient(MailClient):

    def __init__(self, **data):
        super().__init__(**data)
        self.mail_app.config.update({
            'MAIL_SERVER': ServerMailVariants.SMTP_SERVER['server'],
            'MAIL_PORT': ServerMailVariants.SMTP_SERVER['port_ssl'],
            'MAIL_USE_TLS': False,
            'MAIL_USE_SSL': True,
            'MAIL_USERNAME': data['USERNAME'],
            'MAIL_PASSWORD': data['PASSWORD'],
            'MAIL_DEFAULT_SENDER': data['USERNAME'],
        })
        self.mail = Mail(self.mail_app)


class BaseImapPop3SmtpClient:
    def __init__(self, **data):
        self.mail_app = Flask(__name__)
        self.mail_app.config.update({
            'MAIL_SERVER': ServerMailVariants.SMTP_SERVER['server'],
            'MAIL_PORT': ServerMailVariants.SMTP_SERVER['port_ssl'],
            'MAIL_USE_TLS': False,
            'MAIL_USE_SSL': True,
            'MAIL_USERNAME': data['USERNAME'],
            'MAIL_PASSWORD': data['PASSWORD'],
            'MAIL_DEFAULT_SENDER': data['USERNAME'],
            'POP3_SERVER': ServerMailVariants.POP3_SERVER['server'],
            'POP3_PORT': ServerMailVariants.POP3_SERVER['port_ssl'],
            'IMAP_SERVER': ServerMailVariants.IMAP_SERVER['server'],
            'IMAP_PORT': ServerMailVariants.IMAP_SERVER['port_ssl']
        })
        self.mail = Mail(self.mail_app)

    def get_app(self):
        return self.mail_app

    def send_mail(self, to: Union[str, list], body: Tuple[str, str], subject: str = 'Оповещение')\
            -> Union[Response, Tuple[Response, int]]:
        try:
            msg = Message(
                subject,
                sender=self.mail_app.config['MAIL_USERNAME'],
                recipients=[to] if isinstance(to, str) else to
            )

            if body[1] == 'string':
                msg.body = body[0]
            elif body[1] == 'html':
                msg.html = body[0]

            self.mail.send(msg)
            return jsonify({'status': 'success'}), 200

        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500
