import socket
import random

from crypto import load_keys, mod_exp, save_keys, P, G, encrypt_message, decrypt_message


def server():
    # Загружаем или генерируем ключи сервера
    b, B = load_keys()
    if b is None or B is None:
        b = random.randint(1, P - 1)
        B = mod_exp(G, b, P)
        save_keys(b, B)

    # Создаем сокет
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(('localhost', 12345))
        server_socket.listen(1)
        print("Сервер ожидает подключения...")

        conn, addr = server_socket.accept()
        with conn:
            print(f"Клиент подключился: {addr}")

            # Получаем открытый ключ клиента (A)
            data = conn.recv(1024).decode()
            A = int(data)
            print(f"Получено A от клиента: {A}")

            # Отправляем B клиенту
            conn.sendall(str(B).encode())
            print(f"Отправлено B клиенту: {B}")

            # Вычисляем общий секрет K
            K = mod_exp(A, b, P)
            key = K.to_bytes(16, 'big')[:16]  # Приводим ключ к длине 16 байт

            # Получаем зашифрованное сообщение от клиента
            encrypted_message = conn.recv(1024)
            decrypted_message = decrypt_message(key, encrypted_message)
            print(f"Получено и расшифровано сообщение от клиента: {decrypted_message}")

            # Отправляем зашифрованное сообщение клиенту
            response = "Сообщение получено"
            encrypted_response = encrypt_message(key, response)
            conn.sendall(encrypted_response)


if __name__ == '__main__':
    server()
