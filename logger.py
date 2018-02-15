from time import localtime, strftime
from mail import MyMail


class Logger(object):

    def __init__(self, log_file, mail_to, sys_name='unknown'):
        self.log_file = log_file
        self.mail_to = mail_to
        self.sys_name = sys_name

    def write_to_log(self, result_type, tab, test_text, total_time, msg_code, log_title,log_url, log_img=None):
        full_msg = str(result_type) + ';' + strftime('%Y-%m-%d %H:%M:%S', localtime()) + ';' + str(log_url) + ';' + \
                   str(log_title) + ';' + str(tab) + ';' + str(test_text) + ';' + str(total_time) + ';MsgID: ' + \
                   str(msg_code) + '\r\n'
        if result_type == 'ERROR':
            full_mail_msg = full_msg.replace(';', '\r\n')
            MyMail.send_mail(log_title + ' has failed in ' + self.sys_name, full_mail_msg, self.mail_to, log_img)
        elif result_type == 'WARNING':
            pass
        with open(self.log_file, 'a') as f:
            f.write(full_msg)