from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

def encrypt_file(input_file, output_file, key):
    # ������ ������ �� ��������� �����
    with open(input_file, 'rb') as f:
        data = f.read()

    # ��������� ���������� ������� ������������� (IV)
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # ���������� ������
    encrypted_data = cipher.encrypt(pad(data, AES.block_size))

    # ������ ������������� ������ � �������� ����
    with open(output_file, 'wb') as f:
        f.write(iv + encrypted_data)

# ������ �������������
key = get_random_bytes(32)  # 256-������ ����
encrypt_file('Client.exe', 'Client_crptd.exe', key)
