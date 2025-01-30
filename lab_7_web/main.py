import socket
import os
import datetime

HOST = "0.0.0.0"  # Сервер будет слушать все сетевые интерфейсы
PORT = 80  # HTTP-порт
WEB_DIR = os.getcwd()  # Рабочая директория сервера

# Определение MIME-типа по расширению файла
MIME_TYPES = {
    "html": "text/html",
    "css": "text/css",
    "js": "application/javascript",
    "png": "image/png",
    "jpg": "image/jpeg",
    "gif": "image/gif",
    "txt": "text/plain"
}


def get_mime_type(filename):
    ext = filename.split(".")[-1]
    return MIME_TYPES.get(ext, "application/octet-stream")


def handle_request(client_socket):
    request = client_socket.recv(1024).decode("utf-8")
    if not request:
        client_socket.close()
        return

    # Разбираем первую строку запроса
    first_line = request.split("\n")[0]
    method, path, _ = first_line.split()

    if path == "/":
        path = "/index.html"

    file_path = os.path.join(WEB_DIR, path.lstrip("/"))

    date_header = f"Date: {datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')}\r\n"
    server_header = "Server: SimplePythonServer\r\n"
    connection_header = "Connection: close\r\n"

    if os.path.exists(file_path) and os.path.isfile(file_path):
        with open(file_path, "rb") as file:
            response_body = file.read()
        response_header = (
            "HTTP/1.1 200 OK\r\n"
            f"Content-Type: {get_mime_type(file_path)}\r\n"
            f"Content-Length: {len(response_body)}\r\n"
            f"{date_header}"
            f"{server_header}"
            f"{connection_header}\r\n"
        )
    else:
        response_body = b"<h1>404 Not Found</h1>"
        response_header = (
            "HTTP/1.1 404 Not Found\r\n"
            "Content-Type: text/html\r\n"
            f"Content-Length: {len(response_body)}\r\n"
            f"{date_header}"
            f"{server_header}"
            f"{connection_header}\r\n"
        )

    client_socket.sendall(response_header.encode("utf-8") + response_body)
    client_socket.close()


def run_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        print(f"Сервер запущен на {HOST}:{PORT}")

        while True:
            client_socket, _ = server_socket.accept()
            handle_request(client_socket)


if __name__ == "__main__":
    run_server()
