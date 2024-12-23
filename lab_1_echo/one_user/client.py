import socket


if __name__ == '__main__':
    sock = socket.socket()
    sock.connect(('localhost', 9090))
    messages = [
        b'hello, world!',
        b'one more message',
        b'last message',
        b'exit'
    ]
    for msg in messages:
        sock.send(msg)
        data = sock.recv(1024)
        print(data)

    sock.close()
