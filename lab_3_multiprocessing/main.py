import multiprocessing
import random
import os
import time


def generate_random_matrix(size):
    """Генерирует случайную квадратную матрицу заданной размерности."""
    return [[random.randint(1, 10) for _ in range(size)] for _ in range(size)]


def write_element_to_file(file_path, row, col, value):
    """Записывает элемент матрицы в файл."""
    with open(file_path, 'a') as file:
        file.write(f"{row} {col} {value}\n")


def compute_matrix_element(args):
    """Вычисляет один элемент результирующей матрицы."""
    matrix1, matrix2, row, col = args
    value = sum(matrix1[row][k] * matrix2[k][col] for k in range(len(matrix2)))
    return row, col, value


def worker_multiply_task(task_queue, result_file):
    """Обрабатывает задачи перемножения элементов матрицы."""
    while True:
        task = task_queue.get()
        if task is None:  # Сигнал остановки
            break
        row, col, value = compute_matrix_element(task)
        write_element_to_file(result_file, row, col, value)


def multiply_matrices_async(matrix1, matrix2, result_file, num_processes):
    """Перемножает матрицы асинхронно."""
    if len(matrix1[0]) != len(matrix2):
        raise ValueError("Количество столбцов первой матрицы должно совпадать с количеством строк второй матрицы.")

    rows, cols = len(matrix1), len(matrix2[0])

    # Удаляем файл результата, если он существует
    if os.path.exists(result_file):
        os.remove(result_file)

    # Создаем очередь задач и пул процессов
    task_queue = multiprocessing.Queue()
    processes = [
        multiprocessing.Process(target=worker_multiply_task, args=(task_queue, result_file))
        for _ in range(num_processes)
    ]

    # Запускаем процессы
    for process in processes:
        process.start()

    # Отправляем задачи на перемножение
    for row in range(rows):
        for col in range(cols):
            task_queue.put((matrix1, matrix2, row, col))

    # Отправляем сигналы остановки
    for _ in processes:
        task_queue.put(None)

    # Ожидаем завершения процессов
    for process in processes:
        process.join()


def read_result_matrix(file_path, size):
    """Читает результирующую матрицу из файла."""
    matrix = [[0] * size for _ in range(size)]
    with open(file_path, 'r') as file:
        for line in file:
            row, col, value = map(int, line.split())
            matrix[row][col] = value
    return matrix


if __name__ == "__main__":
    # Размер матриц и число процессов
    matrix_size = 4
    num_processes = multiprocessing.cpu_count()
    result_file = "result_matrix.txt"

    # Генерация матриц
    print("Генерация матриц...")
    matrix1 = generate_random_matrix(matrix_size)
    matrix2 = generate_random_matrix(matrix_size)

    print("Матрица 1:")
    for row in matrix1:
        print(row)

    print("Матрица 2:")
    for row in matrix2:
        print(row)

    # Перемножение матриц
    print("\nПеремножение матриц...")
    start_time = time.time()
    multiply_matrices_async(matrix1, matrix2, result_file, num_processes)
    end_time = time.time()

    # Чтение результата
    result_matrix = read_result_matrix(result_file, matrix_size)

    print("Результирующая матрица:")
    for row in result_matrix:
        print(row)

    print(f"\nВремя выполнения: {end_time - start_time:.2f} секунды")
