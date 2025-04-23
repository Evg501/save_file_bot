import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ContentTypes

# Инициализация бота
API_TOKEN = 'ВАШ_TOKEN_BOT'
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Создание директории для сохранения файлов
SAVE_PATH = 'saved_files/'

# Обработчик файлов
@dp.message_handler(content_types=ContentTypes.DOCUMENT | ContentTypes.PHOTO | ContentTypes.AUDIO | ContentTypes.VIDEO)
async def handle_file(message: types.Message):
    try:
        # Определяем тип контента
        if message.document:
            file_id = message.document.file_id
            file_name = message.document.file_name
        elif message.photo:
            file_id = message.photo[-1].file_id
            file_name = f"{message.chat.id}_photo.jpg"
        elif message.audio:
            file_id = message.audio.file_id
            file_name = message.audio.file_name
        elif message.video:
            file_id = message.video.file_id
            file_name = message.video.file_name
        
        # Загружаем файл
        file_info = await bot.get_file(file_id)
        file_path = file_info.file_path
        
        # Сохраняем файл
        await bot.download_file(file_path, SAVE_PATH + file_name)
        
        await message.answer(f"Файл {file_name} успешно сохранен!")
        
    except Exception as e:
        logging.error(f"Ошибка при сохранении файла: {e}")
        await message.answer("Произошла ошибка при сохранении файла")

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)
