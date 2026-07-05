from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

def encrypt_file(file_path, key):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    with open(file_path, 'rb') as f:
        data = f.read()

    # pad to block size
    pad_len = 16 - (len(data) % 16)
    data += bytes([pad_len]) * pad_len

    encrypted_data = encryptor.update(data) + encryptor.finalize()

    with open(file_path + ".enc", 'wb') as f:
        f.write(iv + encrypted_data)

def decrypt_file(file_path, key):
    with open(file_path, 'rb') as f:
        iv = f.read(16)
        data = f.read()

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    decrypted_data = decryptor.update(data) + decryptor.finalize()

    # remove padding
    pad_len = decrypted_data[-1]
    decrypted_data = decrypted_data[:-pad_len]

    original_file = file_path.replace(".enc", "")
    with open(original_file, 'wb') as f:
        f.write(decrypted_data)
