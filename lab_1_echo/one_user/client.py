import socket


def start_client(host, port):
    # Создаем сокет
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Устанавливаем соединение с сервером
    client_socket.connect((host, port))
    print(f"Соединение с сервером {host}:{port} установлено.")

    try:
        while True:
            # Чтение строки с ввода
            message = input("Введите строку для отправки серверу (или 'exit' для выхода): ")
            if message.lower() == 'exit':
                break

            # Отправка данных серверу
            print(f"Отправка данных серверу: {message}")
            client_socket.sendall(message.encode())

            # Получаем ответ от сервера
            data = client_socket.recv(1024)
            print(f"Получены данные от сервера: {data.decode()}")
    finally:
        # Закрываем соединение
        print("Разрыв соединения с сервером.")
        client_socket.close()


if __name__ == "__main__":
    start_client("127.0.0.1", 65432)
