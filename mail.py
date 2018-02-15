import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText


class MyMail(object):
    def __init__(self):
        pass

    @staticmethod
    def send_mail(subject, text, recipient, img_path):
        msg = MIMEMultipart()
        msg_text = MIMEText(text)
        msg.attach(msg_text)
        msg['Subject'] = subject
        msg['From'] = 'PageChecker@qlik.com'
        msg['To'] = recipient
        try:
            with open(img_path,'rb') as img:
                attach_img = MIMEImage(img.read())
            msg.attach(attach_img)
        except:
            pass
        try:
            s = smtplib.SMTP('smtp.qliktech.com')
            s.send_message(msg)
            s.quit()
        except (TimeoutError, TypeError) as e:
            print("Failed to send mail to: " + recipient + ' due to: ' + str(e))