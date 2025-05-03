import email
import imaplib
import poplib
from typing import Tuple

from flask_mail import Message, Mail
from base.mail import BaseImapPop3SmtpClient
from base.constant import SUPPORT_MAIL_PASSWORD, MAIL_USERNAME
from flask import jsonify, request

complex_client = BaseImapPop3SmtpClient(**{
    'USERNAME': MAIL_USERNAME,
    'PASSWORD': SUPPORT_MAIL_PASSWORD
})
mail_app = complex_client.get_app()


@mail_app.route('/')
def hi():
    return 'hi'


@mail_app.route('/get_email/pop3')
def get_email_with_pop():
    try:
        mail = poplib.POP3_SSL(mail_app.config['POP3_SERVER'],
                               mail_app.config['POP3_PORT'])
        mail.user(mail_app.config['MAIL_USERNAME'])
        mail.pass_(mail_app.config['MAIL_PASSWORD'])
        l_mails = len(mail.list()[1])
        emails = []
        for i in range(1, l_mails + 1):
            bytes_null, msg_lines, int_null = mail.retr(i)
            msg_content = b'\n'.join(msg_lines).decode('utf-8')
            emails.append(msg_content)

        mail.quit()
        return jsonify({'emails': emails})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@mail_app.route('/get_emails/imap')
def get_emails_imap():
    try:
        mail = imaplib.IMAP4_SSL(mail_app.config['IMAP_SERVER'], mail_app.config['IMAP_PORT'])
        mail.login(mail_app.config['MAIL_USERNAME'], mail_app.config['MAIL_PASSWORD'])
        mail.select('INBOX')
        status, messages = mail.search(None, 'ALL')
        email_ids = messages[0].split()
        emails = []
        for e_id in email_ids:
            _, msg_data = mail.fetch(e_id, '(RFC822)')
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)

            subject = msg.get('Subject', 'No Subject')
            from_ = msg.get('From', 'Unknown Sender')
            date = msg.get('Date', 'No Date')

            body = ''
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    if content_type == 'text/plain':
                        payload = part.get_payload(decode=True)
                        if payload:
                            body = payload.decode('utf-8', errors='replace')
                            break
            else:
                payload = msg.get_payload(decode=True)
                if payload:
                    body = payload.decode('utf-8', errors='replace')

            emails.append({
                'subject': subject,
                'from': from_,
                'date': date,
                'body': body
            })
        mail.logout()
        return jsonify({'emails': emails})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@mail_app.route('/send_email', methods=['POST'])
def send_email():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Request must be JSON'}), 400

        required = ['to', 'body']
        if not all(field in data for field in required):
            return jsonify({'error': f'Missing required fields: {required}'}), 400

        response, code = complex_client.send_mail(
            to=data['to'],
            body=(data['body'], 'string'),
            subject=data.get('subject', 'Оповещение')
        )
        return response, code

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@mail_app.route('/delete_email/pop3/<int:email_id>', methods=['DELETE'])
def delete_email_with_pop(email_id):
    try:
        mail = poplib.POP3_SSL(mail_app.config['POP3_SERVER'],
                               mail_app.config['POP3_PORT'])
        mail.user(mail_app.config['MAIL_USERNAME'])
        mail.pass_(mail_app.config['MAIL_PASSWORD'])
        response, listings, octets = mail.list()
        if email_id < 1 or email_id > len(listings):
            mail.quit()
            return jsonify({'error': 'Invalid email ID'}), 404
        mail.dele(email_id)
        mail.quit()
        return jsonify({'status': 'success', 'message': f'Email {email_id} marked for deletion'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@mail_app.route('/delete_all_emails/pop3', methods=['DELETE'])
def delete_all_emails_with_pop():
    try:
        mail = poplib.POP3_SSL(mail_app.config['POP3_SERVER'],
                               mail_app.config['POP3_PORT'])
        mail.user(mail_app.config['MAIL_USERNAME'])
        mail.pass_(mail_app.config['MAIL_PASSWORD'])
        response, listings, octets = mail.list()
        for i in range(1, len(listings) + 1):
            mail.dele(i)
        mail.quit()
        return jsonify({'status': 'success', 'message': 'All emails marked for deletion'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
