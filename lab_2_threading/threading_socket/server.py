import socket
import threading


def handle_client(client_socket, client_address):
    print(f"New connection from {client_address}")
    with client_socket:
        while True:
            data = client_socket.recv(1024)
            if not data:
                print(f"Connection with {client_address} closed.")
                break
            client_socket.sendall(data)


def threaded_echo_server(host='127.0.0.1', port=12345):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        print(f"Threaded Echo Server is running on {host}:{port}")
        while True:
            client_socket, client_address = server_socket.accept()
            thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            thread.start()


if __name__ == '__main__':
    threaded_echo_server()
