from base.mail import BaseImapPop3SmtpClient
from base.constant import SUPPORT_MAIL_PASSWORD, MAIL_USERNAME
from starlette.applications import Starlette
from starlette.routing import Mount

complex_client = BaseImapPop3SmtpClient(**{
    'USERNAME': MAIL_USERNAME,
    'PASSWORD': SUPPORT_MAIL_PASSWORD
})
mail_app = complex_client.get_app()


@mail_app.route('/')
def index():
    return 'hi'
