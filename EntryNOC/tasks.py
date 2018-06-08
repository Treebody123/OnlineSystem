from __future__ import absolute_import
from celery import shared_task,task
from .models import EntryNOC
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import datetime
from django.contrib.auth.models import User

# @shared_task
# def SayHello():
#     print('Hello World')

def send_email(to_email,cc_email,mail_msg):
    email_host = 'rb-smtp-int.bosch.com'
    from_email = 'Yu.liu7@cn.bosch.com'

    msg = MIMEMultipart()
    msg['Subject'] = 'Notification to Quality finding'  # 标题
    msg['From'] = from_email  # 邮件显示发件人地址
    msg['To'] = to_email  # needs to debug
    msg['Cc'] = cc_email

    msg.attach(MIMEText(mail_msg, 'html', 'utf-8'))

    smtp = smtplib.SMTP()
    smtp.connect(email_host, 25)
    smtp.sendmail(from_email, to_email, msg.as_string())
    smtp.quit()


@task
def Email_remind_NOC():
    entrynoc_all = EntryNOC.objects.all()
    cur_year = datetime.datetime.now().year
    cur_month = datetime.datetime.now().month
    cur_day = datetime.datetime.now().day
    to_email_list = []
    cc_email_list = []

    for i in entrynoc_all:
        i_update_date = i.last_modify
        if (i_update_date.year == cur_year):
            if (i_update_date.month == cur_month):
                if ((cur_day - i_update_date.day)> 7) :
                    to_email_list.append(i.finding_responsible.email)
                    cc_userlist = User.objects.filter(groups__name='NOC_Management')
                    for user in cc_userlist:
                        cc_email_list.append(user.email)
                    mail_msg = 'Please be remind that your quality case {} has not been updated over 1 week since assigned.'.format(i.ticket_num)
                    mail_msg += '''
                    <p><a href="http://127.0.0.1:8000:"> visit Quality Track System</a></p>
                    '''
                    send_email(to_email_list,cc_email_list,mail_msg)


