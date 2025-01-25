import socket
import random

from crypto import load_keys, mod_exp, save_keys, P, G, encrypt_message, decrypt_message


def client():
    # Загружаем или генерируем ключи клиента
    a, A = load_keys()
    if a is None or A is None:
        a = random.randint(1, P - 1)
        A = mod_exp(G, a, P)
        save_keys(a, A)

    # Создаем сокет
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect(('localhost', 12345))

        # Отправляем A серверу
        client_socket.sendall(str(A).encode())
        print(f"Отправлено A серверу: {A}")

        # Получаем B от сервера
        data = client_socket.recv(1024).decode()
        B = int(data)
        print(f"Получено B от сервера: {B}")

        # Вычисляем общий секрет K
        K = mod_exp(B, a, P)
        key = K.to_bytes(16, 'big')[:16]  # Приводим ключ к длине 16 байт

        # Отправляем зашифрованное сообщение серверу
        message = "Привет, сервер!"
        encrypted_message = encrypt_message(key, message)
        client_socket.sendall(encrypted_message)
        print(f"Отправлено зашифрованное сообщение серверу: {message}")

        # Получаем зашифрованный ответ от сервера
        encrypted_response = client_socket.recv(1024)
        decrypted_response = decrypt_message(key, encrypted_response)
        print(f"Получен и расшифрован ответ от сервера: {decrypted_response}")


if __name__ == '__main__':
    client()