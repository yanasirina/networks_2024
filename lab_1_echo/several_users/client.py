import socket
import threading


def receive_messages(sock):
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            print(data.decode())
        except Exception as e:
            print(f"Error receiving message: {e}")
            break


if __name__ == '__main__':
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', 9090)

    # Сообщаем серверу о подключении
    client_socket.sendto(b'Client connected!', server_address)

    threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()

    print("Type your messages (type 'exit' to leave):")
    while True:
        message = input()
        client_socket.sendto(message.encode(), server_address)
        if message.lower() == 'exit':
            print("Exiting chat...")
            break

    client_socket.close()
