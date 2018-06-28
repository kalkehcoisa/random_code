#!/usr/bin/env python3

from smtplib import SMTP

EMAIL_HOST_PORT = 25
EMAIL_HOST = 'smtp.email.com'
IMAP_HOST = 'mail.email.com'
EMAIL_HOST_USER = 'host_user'
EMAIL_HOST_PASSWORD = 'senha'
DEFAULT_FROM_EMAIL = 'Packtpub Getter <email@email.com.br>'


def send_mail(message, title, to_mail):
    msg_header = 'From: {sender}\n' \
        'To: Jayme {to_mail}\n' \
        'MIME-Version: 1.0\n' \
        'Content-type: text/html\n' \
        'Subject: {title}\n'.format(
            sender=DEFAULT_FROM_EMAIL,
            to_mail=to_mail,
            title=title,
        )

    msg_content = '''
<h2>{title} > <font color="green">OK</font></h2><br/><br/>
'''.format(
        title=title)
    msg_full = (''.join([msg_header, msg_content, message])).encode()

    server = SMTP()
    server.connect(EMAIL_HOST)
    server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
    server.sendmail(
        DEFAULT_FROM_EMAIL,
        to_mail,
        msg_full)
    server.quit()
