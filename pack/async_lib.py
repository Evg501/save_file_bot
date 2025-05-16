import asyncio
import os

async def wait_rename(old_name, new_name):
    for attempt in range(5):
        try:
            os.rename(old_name, new_name)
            break
        except PermissionError:
            print(f"Файл занят, ждём... Попытка {attempt + 1}")
            await asyncio.sleep(1)
    else:
        print("Не удалось переименовать файл — занят.")
    
    
async def wait_for_file_size(file_path: str, expected_size: int, timeout: int = 30, interval: float = 0.5):
    """
    Ожидает, пока размер файла не станет равным expected_size.
    
    :param file_path: Путь к файлу.
    :param expected_size: Ожидаемый размер файла в байтах.
    :param timeout: Максимальное время ожидания в секундах.
    :param interval: Интервал проверки в секундах.
    :return: True, если размер совпал, иначе False.
    """
    elapsed_time = 0

    while elapsed_time < timeout:
        if os.path.exists(file_path):
            current_size = os.path.getsize(file_path)
            if current_size == expected_size:
                print(f"✅ Размер файла совпадает с ожидаемым: {expected_size} байт")
                return True
            else:
                print(f"🔄 Размер файла: {current_size} / {expected_size} байт")

        await asyncio.sleep(interval)
        elapsed_time += interval

    print(f"❌ Таймаут: не удалось дождаться нужного размера файла за {timeout} секунд.")
    return False