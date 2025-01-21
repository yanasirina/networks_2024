import asyncio


async def handle_client(reader, writer):
    """Обработка подключенного клиента."""
    addr = writer.get_extra_info('peername')
    print(f"Подключение от {addr}")

    try:
        while True:
            # Чтение данных от клиента
            data = await reader.read(1024)
            if not data:
                break  # Клиент закрыл соединение

            message = data.decode()
            print(f"Получено сообщение: {message} от {addr}")

            # Отправка данных обратно клиенту
            writer.write(data)
            await writer.drain()

    except asyncio.CancelledError:
        print(f"Соединение с {addr} было прервано.")
    finally:
        print(f"Отключение клиента {addr}")
        writer.close()
        await writer.wait_closed()


async def main(host='127.0.0.1', port=8888):
    """Запуск эхо-сервера."""
    server = await asyncio.start_server(handle_client, host, port)
    addr = server.sockets[0].getsockname()
    print(f"Эхо-сервер запущен на {addr}")

    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
