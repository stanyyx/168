import email
import smtplib
import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailClient:
    def __init__(self, login_, password_):
        self.connect = {'login': login_, 'password': password_}

    def sendmail(self, server_, port_, recipients_, subject_, body_):
        try:
            email_message = MIMEMultipart()
            email_message['From'] = self.connect['login']
            email_message['To'] = ', '.join(recipients_)
            email_message['Subject'] = subject_
            email_message.attach(MIMEText(body_))
            sendmail_instance = smtplib.SMTP(server_, port_)
            sendmail_instance.ehlo()
            sendmail_instance.starttls()
            sendmail_instance.ehlo()
            sendmail_instance.login(self.connect['login'], self.connect['password'])
            result = sendmail_instance.sendmail(email_message['From'], email_message['To'], email_message.as_string())
            sendmail_instance.quit()
            return result
        except Exception as e:
            return f'Failed to send email: {e}'

    def receive_mail(self, server_, mailbox_, header_=None):
        receive_mail_instance = imaplib.IMAP4_SSL(server_)
        try:
            receive_mail_instance.login(self.connect['login'], self.connect['password'])
            receive_mail_instance.list()
            receive_mail_instance.select(mailbox_)
            criterion = '(HEADER Subject "%s")' % header_ if header_ else 'ALL'
            result, data = receive_mail_instance.uid('search', None, criterion)
            assert data[0], 'There are no letters with current header'
            latest_email_uid = data[0].split()[-1]
            print(latest_email_uid.decode('utf-8'))
            result, data = receive_mail_instance.uid('fetch', latest_email_uid.decode('utf-8'), '(RFC822)')
            raw_email = data[0][1]
            email_result_receive = email.message_from_string(raw_email.decode('utf-8'))
            receive_mail_instance.logout()
            return email_result_receive
        except Exception as e:
            return f'Failed to receive email:{e}'


if __name__ == '__main__':
    gmail = EmailClient('someuser@gmail.com', 'somepassword')
    print(gmail.sendmail(
        'smtp.gmail.com',
        587,
        ['oneuser@one.com', 'seconduser@two.com'],
        'Test message',
        'Body of test message'
    ))
    print(gmail.receive_mail('imap.gmail.com', 'inbox'))
