#!/usr/bin/python
# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.header import Header

class Send_code():
    def Send(self,email,code):
        mail_host="smtp.zju.edu.cn"  #设置服务器
        mail_user="3150102416"    #用户名
        mail_pass="011932"   #口令


        sender = '3150102416@zju.edu.cn'
        receivers = [email]  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

        mail_msg = """
        <p>欢迎注册<a href="http://feetime.cc">Feetime</a></p>
        <p>一个属于浙大人自己的交友网站</p>
        <p>您的 验证码为 (%s)</p>
        """
        message = MIMEText(mail_msg%code, 'html', 'utf-8')
        from_ ='Feetime'
        message['From'] = from_
        message['To'] =  '浙里的你'

        subject = 'Feetime新成员 浙里资格验证：'
        message['Subject'] = Header(subject, 'utf-8')


        try:
            smtObj = smtplib.SMTP()
            smtObj.connect(mail_host, 25)
            print 1
            try:
                smtObj.login(mail_user,mail_pass)
            except:
                print "login fail"
            smtObj.sendmail(sender, receivers, message.as_string())
            print 3
            print "邮件发送成功"
        except smtplib.SMTPException:
            print "Error: 无法发送邮件"
if __name__ == "__main__":
    y = Send_code()
    y.Send("3150102416@zju.edu.cn",9999)


