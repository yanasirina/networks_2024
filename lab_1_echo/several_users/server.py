import socket
import threading


def handle_client(sock, clients, lock):
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            if not data:
                continue

            message = f"[{addr[0]}:{addr[1]}] {data.decode()}"
            print(message)

            if data == b'exit':
                with lock:
                    if addr in clients:
                        del clients[addr]
                print(f"Client {addr} disconnected.")
                continue

            # Рассылаем сообщение всем клиентам
            with lock:
                for client_addr in clients.keys():
                    sock.sendto(message.encode(), client_addr)

        except Exception as e:
            print(f"Error handling client {addr}: {e}")


if __name__ == '__main__':
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('localhost', 9090))

    clients = {}  # Список клиентов
    lock = threading.Lock()

    print("Server is running on port 9090...")
    threading.Thread(target=handle_client, args=(server_socket, clients, lock), daemon=True).start()

    while True:
        # Добавляем клиентов в список
        data, addr = server_socket.recvfrom(1024)
        with lock:
            if addr not in clients:
                clients[addr] = True
                print(f"New client connected: {addr}")
                server_socket.sendto(b"Welcome to the chat!", addr)
