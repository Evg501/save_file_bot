import os
import logging
from aiogram import Bot, Dispatcher, types
#from aiogram.utils import executor
from aiogram.types import InputFile
import asyncio

# Настройки бота
TOKEN = ""  # Замените на токен вашего бота
SAVE_FOLDER = "downloaded_files"   # Папка для сохранения файлов

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

async def on_startup(_):
    """Создаем папку для файлов при запуске бота"""
    if not os.path.exists(SAVE_FOLDER):
        os.makedirs(SAVE_FOLDER)
    logger.info("Бот запущен и готов к работе")

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """Обработчик команды /start"""
    await message.reply(f"Привет {message.from_user.first_name}!\nОтправь мне любой файл, и я сохраню его в папку {SAVE_FOLDER}.")

@dp.message_handler(content_types=[
    types.ContentType.DOCUMENT,
    types.ContentType.PHOTO,
    types.ContentType.VIDEO,
    types.ContentType.AUDIO,
    types.ContentType.VOICE,
    types.ContentType.VIDEO_NOTE
])
async def handle_file(message: types.Message):
    """Обработчик для всех типов файлов"""
    try:
        # Определяем тип файла и получаем информацию о нем
        if message.document:
            file_id = message.document.file_id
            file_name = message.document.file_name or f"document_{file_id}"
            file = await bot.get_file(file_id)
        elif message.photo:
            file_id = message.photo[-1].file_id  # Берем фото с самым высоким разрешением
            file_name = f"photo_{file_id}.jpg"
            file = await bot.get_file(file_id)
        elif message.video:
            file_id = message.video.file_id
            file_name = message.video.file_name or f"video_{file_id}.mp4"
            file = await bot.get_file(file_id)
        elif message.audio:
            file_id = message.audio.file_id
            file_name = message.audio.file_name or f"audio_{file_id}.mp3"
            file = await bot.get_file(file_id)
        elif message.voice:
            file_id = message.voice.file_id
            file_name = f"voice_{file_id}.ogg"
            file = await bot.get_file(file_id)
        elif message.video_note:
            file_id = message.video_note.file_id
            file_name = f"video_note_{file_id}.mp4"
            file = await bot.get_file(file_id)
        else:
            await message.reply("Извините, этот тип файла не поддерживается.")
            return

        # Формируем путь для сохранения
        file_path = os.path.join(SAVE_FOLDER, file_name)
        
        # Скачиваем и сохраняем файл
        await bot.download_file(file.file_path, file_path)
        
        # Отправляем подтверждение
        await message.reply(f"Файл успешно сохранен как: {file_name}")
        
    except Exception as e:
        logger.error(f"Ошибка при обработке файла: {e}")
        await message.reply("Произошла ошибка при сохранении файла.")

async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    #bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    bot = Bot(token=TOKEN)

    # And the run events dispatching
    await dp.start_polling(bot)
    
if __name__ == '__main__':
    #executor.start_polling(dp, on_startup=on_startup)
    asyncio.run(main())