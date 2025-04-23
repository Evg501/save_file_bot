import os
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Настройки бота
TOKEN = ""  # Замените на токен вашего бота
SAVE_FOLDER = "temp"   # Папка для сохранения файлов (создается в той же директории, что и скрипт)

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext) -> None:
    """Отправляет сообщение при команде /start"""
    user = update.effective_user
    update.message.reply_text(
        f"Привет {user.first_name}! Отправь мне любой файл, и я сохраню его в папку {SAVE_FOLDER}."
    )

def handle_file(update: Update, context: CallbackContext) -> None:
    """Обрабатывает полученные файлы и сохраняет их"""
    # Создаем папку, если она не существует
    if not os.path.exists(SAVE_FOLDER):
        os.makedirs(SAVE_FOLDER)
    
    # Получаем файл от пользователя
    file = update.message.effective_attachment
    
    # В зависимости от типа файла получаем разные атрибуты
    if update.message.document:
        file_id = update.message.document.file_id
        file_name = update.message.document.file_name or f"document_{file_id}"
    elif update.message.photo:
        file_id = update.message.photo[-1].file_id  # Берем последнее (самое высокое) фото
        file_name = f"photo_{file_id}.jpg"
    elif update.message.video:
        file_id = update.message.video.file_id
        file_name = update.message.video.file_name or f"video_{file_id}.mp4"
    elif update.message.audio:
        file_id = update.message.audio.file_id
        file_name = update.message.audio.file_name or f"audio_{file_id}.mp3"
    elif update.message.voice:
        file_id = update.message.voice.file_id
        file_name = f"voice_{file_id}.ogg"
    elif update.message.video_note:
        file_id = update.message.video_note.file_id
        file_name = f"video_note_{file_id}.mp4"
    else:
        update.message.reply_text("Извините, этот тип файла не поддерживается.")
        return
    
    # Скачиваем файл
    new_file = context.bot.get_file(file_id)
    file_path = os.path.join(SAVE_FOLDER, file_name)
    
    # Сохраняем файл
    new_file.download(file_path)
    
    # Отправляем подтверждение
    update.message.reply_text(f"Файл сохранен как: {file_name}")

def main() -> None:
    """Запуск бота"""
    # Создаем Updater и передаем ему токен бота
    updater = Updater(TOKEN)
    
    # Получаем диспетчер для регистрации обработчиков
    dispatcher = updater.dispatcher
    
    # Регистрируем обработчики команд
    dispatcher.add_handler(CommandHandler("start", start))
    
    # Регистрируем обработчик файлов
    dispatcher.add_handler(MessageHandler(
        Filters.document | Filters.photo | Filters.video | Filters.audio | Filters.voice | Filters.video_note,
        handle_file
    ))
    
    # Запускаем бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()