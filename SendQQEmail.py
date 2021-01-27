# 发送多种类型的邮件
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

msg_from = 'xxxxx@qq.com'  # 发送方邮箱
passwd = 'xxxxx'  # 就是上面的授权码

to = ['xxxxxx@qq.com']  # 接受方邮箱
# 接收方与发送方邮箱可以都是自己


def send(title,conntent):
    # 设置邮件内容
    # MIMEMultipart类可以放任何内容
    msg = MIMEMultipart()
    conntent = str(datetime.today())[:19] + "\n" + conntent
    print(conntent)
    # 把内容加进去
    msg.attach(MIMEText(conntent, 'plain', 'utf-8'))

    # 设置邮件主题
    msg['Subject'] = title

    # 发送方信息
    msg['From'] = msg_from

    # 开始发送

    # 通过SSL方式发送，服务器地址和端口
    s = smtplib.SMTP_SSL("smtp.qq.com", 465)
    # 登录邮箱
    s.login(msg_from, passwd)
    # 开始发送
    s.sendmail(msg_from, to, msg.as_string())
    print("邮件发送成功！")


def success():
    conntent = "打卡成功！"
    send(conntent,conntent)


def failure(title,conntent):
    send(title,conntent)
