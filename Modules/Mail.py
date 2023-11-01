import smtplib
from smtplib import SMTPException


def mail(receivers, text):
    text = text.replace(u'\xa0', u' ')
    gmail_user = ''
    gmail_pwd = ''

    subject = 'Voltaire'
    message = f'Subject: {subject}\n\n{text}'

    try:
        server_ssl = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server_ssl.ehlo()
        server_ssl.login(gmail_user, gmail_pwd)

        server_ssl.sendmail(gmail_user, receivers, message)
        server_ssl.close()
        return True

    except SMTPException:
        return False

