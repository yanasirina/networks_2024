import socket
import threading
from queue import Queue
from tqdm import tqdm


# Функция для сканирования одного порта
def scan_port(host, port, open_ports):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            if s.connect_ex((host, port)) == 0:
                open_ports.append(port)
    except Exception:
        pass


# Функция для работы потоков
def worker(host, queue, open_ports, progress):
    while not queue.empty():
        port = queue.get()
        scan_port(host, port, open_ports)
        progress.update(1)


# Основная функция сканирования портов
def port_scanner(host, start_port=1, end_port=65535, num_threads=100):
    print(f"Сканирование {host} на открытые порты...")

    # Очередь портов
    port_queue = Queue()
    for port in range(start_port, end_port + 1):
        port_queue.put(port)

    # Список для хранения открытых портов
    open_ports = []

    # Настройка прогресс-бара
    total_ports = end_port - start_port + 1
    with tqdm(total=total_ports, desc="Сканирование портов", unit="порт") as progress:
        # Создание потоков
        threads = []
        for _ in range(num_threads):
            thread = threading.Thread(target=worker, args=(host, port_queue, open_ports, progress))
            thread.start()
            threads.append(thread)

        # Ожидание завершения потоков
        for thread in threads:
            thread.join()

    # Вывод результатов
    open_ports.sort()
    print("\nОткрытые порты:")
    for port in open_ports:
        print(f"Порт {port} открыт")


if __name__ == "__main__":
    target_host = input("Введите IP-адрес или имя хоста для сканирования: ")
    port_scanner(target_host)
