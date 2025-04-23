import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import os

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Функция для обработки команды /start
async def start(update: Update, context):
    await update.message.reply_text('Привет! Отправь мне файл, и я сохраню его.')

# Функция для обработки файлов
async def handle_document(update: Update, context):
    # Получаем файл
    file = await update.message.document.get_file()
    
    # Создаем папку для сохранения файлов, если её нет
    save_folder = 'saved_files'
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    
    # Получаем имя файла
    file_name = update.message.document.file_name
    
    # Сохраняем файл
    file_path = os.path.join(save_folder, file_name)
    await file.download_to_drive(custom_path=file_path)
    
    await update.message.reply_text(f'Файл {file_name} успешно сохранен!')

# Функция для обработки всех остальных сообщений
async def unknown(update: Update, context):
    await update.message.reply_text('Отправь мне файл, пожалуйста.')

def main():
    # Вставьте токен вашего бота здесь
    token = ''
    
    # Создаем приложение
    application = Application.builder().token(token).build()
    
    # Добавляем обработчики команд
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.PHOTO, handle_document))
    application.add_handler(MessageHandler(filters.ALL, unknown))
    
    # Запускаем бота
    application.run_polling(poll_interval=1.0)

if __name__ == '__main__':
    main()
