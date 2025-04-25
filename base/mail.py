from flask import render_template
from flask_mail import Mail, Message
from flask import Flask
from typing import Tuple


class ServerMailVariants:
    SMTP_SERVER = {'server': 'smtp.mail.com', 'port_ssl': 465}
    POP3_SERVER = {'server': 'pop.mail.com', 'port_ssl': 995}
    IMAP_SERVER = {'server': 'imap.mail.com', 'port_ssl': 993}


class MailClient:
    USERNAME: str
    PASSWORD: str

    def __init__(self, **data):
        self.mail_app = Flask(__name__)
        self.mail_app.config.USERNAME = data['USERNAME']
        self.mail_app.config.PASSWORD = data['PASSWORD']
        self.mail_app.config.USE_TLS = False
        self.mail_app.config.USE_SSL = True

    def get_app(self):
        return self.mail_app


class BaseSMPTMailClient(MailClient):

    def __init__(self, **data):
        super().__init__(**data)
        self.mail_app.config.SERVER = ServerMailVariants.SMTP_SERVER['server']
        self.mail_app.config.PORT = ServerMailVariants.SMTP_SERVER['port_ssl']
        self.mail = Mail(self.mail_app)

    # def send_mail(self, to: str | list, body: Tuple[str, str], subject: str = 'Оповещение') -> Tuple[bool, str] | bool:
    #     try:
    #         msg = Message(subject, sender=self.mail_app.config['USERNAME'],
    #                       recipients=([to] if isinstance(to, str) else list(map(str, to))))
    #         if body[1] == 'string':
    #             msg.body = body
    #         elif body[1] == 'html':
    #             msg.body = render_template(body[0])
    #         self.mail.send(msg)
    #         return True
    #     except Exception as e:
    #         return False, str(e)


class BaseImapPop3SmtpClient(BaseSMPTMailClient):

    def __init__(self, **data):
        super().__init__(**data)
        self.mail_app.config.update({
            'SMTP_SERVER': ServerMailVariants.SMTP_SERVER['server'],
            'SMTP_PORT': ServerMailVariants.SMTP_SERVER['port_ssl'],
            'POP3_SERVER': ServerMailVariants.POP3_SERVER['server'],
            'POP3_PORT': ServerMailVariants.POP3_SERVER['port_ssl'],
            'IMAP_SERVER': ServerMailVariants.IMAP_SERVER['server'],
            'IMAP_PORT': ServerMailVariants.IMAP_SERVER['port_ssl']
        })
        self.mail = Mail(self.mail_app)
