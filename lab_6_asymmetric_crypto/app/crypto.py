import os

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7
from cryptography.hazmat.backends import default_backend


# Параметры протокола
P = 23  # Простое число
G = 5   # Основание

KEY_FILE = "private_key.txt"
PUBLIC_FILE = "public_key.txt"


# Функция для вычисления степени по модулю
def mod_exp(base, exp, mod):
    return pow(base, exp, mod)


# Функция для симметричного шифрования
def encrypt_message(key, plaintext):
    iv = os.urandom(16)  # Initialization Vector
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padder = PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(plaintext.encode()) + padder.finalize()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    return iv + ciphertext


# Функция для симметричного расшифрования
def decrypt_message(key, ciphertext):
    iv = ciphertext[:16]
    actual_ciphertext = ciphertext[16:]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    unpadder = PKCS7(algorithms.AES.block_size).unpadder()
    padded_data = decryptor.update(actual_ciphertext) + decryptor.finalize()
    plaintext = unpadder.update(padded_data) + unpadder.finalize()
    return plaintext.decode()


# Функции для работы с ключами
def save_keys(private_key, public_key):
    with open(KEY_FILE, "w") as key_file:
        key_file.write(str(private_key))
    with open(PUBLIC_FILE, "w") as public_file:
        public_file.write(str(public_key))


def load_keys():
    if os.path.exists(KEY_FILE) and os.path.exists(PUBLIC_FILE):
        with open(KEY_FILE, "r") as key_file:
            private_key = int(key_file.read())
        with open(PUBLIC_FILE, "r") as public_file:
            public_key = int(public_file.read())
        return private_key, public_key
    return None, None
