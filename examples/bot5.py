import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.enums import ParseMode

# Токен вашего бота
BOT_TOKEN = ""
# Папка для сохранения файлов
DOWNLOAD_FOLDER = "downloads"

# Создаем папку, если она не существует
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# Обработчик команды /start
@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Привет! Отправь мне файл, и я сохраню его в папку.")

# Обработчик документов и файлов
@dp.message()
async def handle_files(message: Message):
    if message.document:
        file = message.document
    elif message.photo:
        file = message.photo[-1]  # Берем самое большое изображение
    elif message.audio:
        file = message.audio
    elif message.video:
        file = message.video
    elif message.voice:
        file = message.voice
    elif message.video_note:
        file = message.video_note
    else:
        await message.reply("Пожалуйста, отправьте файл.")
        return

    try:
        file_info = await bot.get_file(file.file_id)
        downloaded_file = await bot.download_file(file_info.file_path)
        
        # Создаем путь для сохранения файла
        file_path = os.path.join(DOWNLOAD_FOLDER, file.file_id + "_" + file.file_name if hasattr(file, 'file_name') else file.file_id)
        
        # Сохраняем файл
        with open(file_path, "wb") as new_file:
            new_file.write(downloaded_file.getvalue())
        
        await message.reply(f"Файл сохранен: {file_path}")
    except Exception as e:
        await message.reply(f"Произошла ошибка: {e}")

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())