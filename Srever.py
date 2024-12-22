import socket
import threading
import os
import time
clients = {}
client_names = {}

count = 1

def handle_client(client_socket):
  while True:
    try:
      #print(client_socket)
      message = client_socket.recv(1024).decode('utf-8')
      if message:
        if client_socket not in client_names:
          client_names[client_socket] = message
          #broadcast(f"{client_names[client_socket]} присоединился к чату.", client_socket)
        else:
          if message.startswith("you "):
            formatted_message = f"{client_names[client_socket]} (лично): {message[4:]}"
            send_private_message(formatted_message, client_socket)
          if message.startswith("."):
            if message.startswith(".img"):
              print("Loading...")
              file = open(f'{client_names[client_socket]}.png', mode="wb")


              size_bytes = client_socket.recv(4)
              size = int.from_bytes(size_bytes, byteorder='big')
              print(size)

              received_bytes = 0
              while received_bytes < size:
                try:
                  print(f"{received_bytes} / {size}")
                  data = client_socket.recv(1024)
                  if not data:  # Проверка на пустые данные
                    print(f"Ошибка при получении изображения: Клиент отключился")
                    break

                  file.write(data)
                  received_bytes += len(data)
                except Exception as e:
                  print(f"Ошибка при получении изображения: {e}")
                  break

              file.close()
              print("Complete")
              os.startfile(f'{client_names[client_socket]}.png')
            else:
              print(message[1:])
          else:
            print(f"Получено сообщение от {client_names[client_socket]}: {message}")
            broadcast(f"{client_names[client_socket]}: {message}", client_socket)
      else:
        remove(client_socket)
        break
    except:
      continue

def broadcast(message, client_socket):
  for client in clients.keys():
    print(client)
    if client != client_socket:
      try:
        client.send(message.encode('utf-8'))
      except:
        remove(client)

def send_private_message(message, sender_socket):
  try:
    if ':' not in message:
      return

    recipient_info = message.split(':')[1].strip()
    if not recipient_info:
      return

    recipient_name = recipient_info.split(' ')[0]

    flag = True
    for client, name in client_names.items():
      #print(recipient_name)
      if recipient_name == '.':
        return
      if name == recipient_name:
        flag = False
        message = ' '.join([el for el in message.split(" ") if el != f'{name}'])
        client.send(message.encode('utf-8'))
        message = message.replace("(лично)", "").strip()
        print(f"(лично для {name}) от {message}")
        return
    if flag:
      print(f"Пользователь {recipient_name} не найден.")
      out_mes = f"Пользователь {recipient_name} не найден."
      sender_socket.send(out_mes.encode('utf-8'))



  except Exception as e:
    print(f"Ошибка при отправке личного сообщения: {e}")
def remove(client_socket):
  global count
  count = count - 1
  print(f"Клиент {client_names[client_socket]} отключился")
  if client_socket in clients:
    del clients[client_socket]
    if client_socket in client_names:
      del client_names[client_socket]

def accept_connections(server):

  while True:
    client_socket, addr = server.accept()
    clients[client_socket] = addr
    global count
    name = client_socket.recv(1024).decode('utf-8')
    name += str(count)
    count += 1
    print(f"Подключен {addr} под псевдонимом {name}")
    client_names[client_socket] = name
    #broadcast(f"{name} присоединился к чату.", client_socket)

    thread = threading.Thread(target=handle_client, args=(client_socket,))
    thread.start()


def start_server():
  server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server.bind(('localhost', 9090))
  server.listen(5)
  print("Server started")


  accept_thread = threading.Thread(target=accept_connections, args=(server,))
  accept_thread.start()

  while True:
    message = input()
    if message.startswith("you "):
      formatted_message = f"Сервер (лично): {message[4:]}"
      send_private_message(formatted_message, None)
    else:
      broadcast(f"Сервер: {message}", None)
    if message.lower() == 'exit':
      break

  for client in clients.keys():
    client.close()
  server.close()


start_server()
