# Словарь для сопоставления MIME-типов с расширениями файлов
mime_to_extension = {
    "text/plain": ".txt",
    "application/pdf": ".pdf",
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "application/msword": ".doc",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
    "application/vnd.ms-excel": ".xls",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": ".xlsx",
    "application/zip": ".zip",
    "application/json": ".json",
    "application/xml": ".xml",
    "audio/mpeg": ".mp3",
    "video/mp4": ".mp4",
    "application/octet-stream": ".bin",  # Бинарный файл (по умолчанию)
    # Добавьте другие MIME-типы и их расширения по необходимости
}

def get_extension_from_mime(mime_type):
    """
    Функция для получения расширения файла по его MIME-типу.
    
    :param mime_type: MIME-тип файла (например, 'image/jpeg')
    :return: Расширение файла (например, '.jpg') или None, если MIME-тип неизвестен
    """
    if mime_to_extension.get(mime_type.lower())==None:
        print(mime_type, ' неизвестен')
    return mime_to_extension.get(mime_type.lower())

# Пример использования
if __name__ == "__main__":
    # Примеры MIME-типов
    mime_types = [
        "image/jpeg",
        "application/pdf",
        "text/html",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "unknown/type"
    ]
    
    for mime in mime_types:
        extension = get_extension_from_mime(mime)
        if extension:
            print(f"MIME-тип '{mime}' соответствует расширению '{extension}'")
        else:
            print(f"MIME-тип '{mime}' неизвестен или не поддерживается")