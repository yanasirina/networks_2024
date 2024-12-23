import socket
import time


if __name__ == '__main__':
    sock = socket.socket()
    sock.bind(('', 9090))
    sock.listen(1)
    conn, addr = sock.accept()

    while True:
         data = conn.recv(1024)
         if not data:
             time.sleep(0.5)  # чтобы не перегружать сервер
             continue
         if data == b'exit':
             break
         conn.send(data.upper())

    conn.close()
