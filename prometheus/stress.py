import multiprocessing
import time
import math

def cpu_load(duration):
    """Функция создает нагрузку на одно ядро CPU"""
    end_time = time.time() + duration
    while time.time() < end_time:
        # Выполняем бессмысленные вычисления
        math.sqrt(12345) ** 2

if __name__ == "__main__":
    duration = 60  # секунд
    cores = multiprocessing.cpu_count()  # количество доступных ядер

    print(f"Создаем нагрузку на {cores} CPU ядра на {duration} секунд...")

    processes = []
    for _ in range(cores):
        p = multiprocessing.Process(target=cpu_load, args=(duration,))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    print("Нагрузка завершена. CPU должен вернуться к норме.")
