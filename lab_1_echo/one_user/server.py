import socket


def start_server(host, port):
    # Создаем сокет
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print(f"Сервер запущен на {host}:{port}")
    print("Начало прослушивания порта...")

    while True:
        # Принимаем подключение от клиента
        client_socket, client_address = server_socket.accept()
        print(f"Подключение от клиента: {client_address}")

        try:
            while True:
                # Получаем данные от клиента порциями по 1 КБ
                data = client_socket.recv(1024)
                if not data:
                    # Если данных нет, значит клиент отключился
                    print(f"Отключение клиента: {client_address}")
                    break

                # Выводим полученные данные и отправляем их обратно
                print(f"Получены данные от клиента: {data.decode()}")
                print("Отправка данных клиенту...")
                client_socket.sendall(data)
        finally:
            client_socket.close()
            print("Соединение с клиентом закрыто.")


def stop_server():
    print("Сервер остановлен.")


if __name__ == "__main__":
    start_server("127.0.0.1", 65432)
