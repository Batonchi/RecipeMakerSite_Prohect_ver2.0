from typing import Tuple, Union

from base.mail import BaseSMPTMailClient
from base.constant import MAIL_USERNAME, NOTIFICATION_MAIL_PASSWORD


notification_client = BaseSMPTMailClient(**{
    'USERNAME': MAIL_USERNAME,
    'PASSWORD': NOTIFICATION_MAIL_PASSWORD
})
notification_mail_app = notification_client.get_app()


@notification_mail_app.route('/send_email/<user_id>', methods=['POST'])
def send_notification_email(to: Union[str, list], body: Tuple[str, str], subject: str = 'Оповещение'):
    return notification_client.send_mail(to, body, subject)


