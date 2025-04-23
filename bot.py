import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.token import TokenValidationError
from aiogram import F
#from pack.file_lib import *
import filetype
from config_hiden import API_TOKEN
from pack.date_lib import *
import logging
from pack.file_lib import *

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("Бот запущен и готов к работе")

# Укажите токен вашего бота
#API_TOKEN = ''

# Укажите путь к папке, куда будут сохраняться файлы
DOWNLOADS_DIR = './downloads'

# Создаем папку для загрузок, если она не существует
os.makedirs(DOWNLOADS_DIR, exist_ok=True)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Обработчик команды /start
@dp.message(Command("start"))
async def send_welcome(message: Message):
    await message.answer("Привет! Отправь мне файл, и я сохраню его.")

# Обработчик для других типов сообщений (опционально)
@dp.message()
async def handle_other_messages(message: Message):
    try:
        # В зависимости от типа файла получаем разные атрибуты
        if message.document:
        #    file = message.document        
            file_id = message.document.file_id
            file_name = message.document.file_name or f"document_{file_id}"
            prefix='document_'
        elif message.photo:
            file_id = message.photo[-1].file_id  # Берем последнее (самое высокое) фото
            file_name = f"photo_{file_id}.jpg"
            prefix='photo_'
        elif message.video:
            file_id = message.video.file_id
            file_name = message.video.file_name or f"video_{file_id}.mp4"
            prefix='video_'
        elif message.audio:
            file_id = message.audio.file_id
            file_name = message.audio.file_name or f"audio_{file_id}.mp3"
            prefix='audio_'
        elif message.voice:
            file_id = message.voice.file_id
            file_name = f"voice_{file_id}.ogg"
            prefix='voice_'
        elif message.video_note:
            file_id = message.video_note.file_id
            file_name = f"video_note_{file_id}.mp4"
            prefix='video_note_'
        else:
            if message.text!=None:
                #print(message.text)
                # Расширение файла не известно
                file_name_txt = genfname(pref='txt_', postf='.txt')
                # Формируем путь для сохранения файла
                file_path_txt = os.path.join(DOWNLOADS_DIR, file_name_txt)                
                write_file(fname=file_path_txt, text=message.text, e='utf8')
            await message.reply("Пожалуйста, отправьте файл.")
            return    
        
        # Расширение файла не известно
        file_name = genfname(pref=prefix, postf='.bin')
        
        # Формируем путь для сохранения файла
        file_path = os.path.join(DOWNLOADS_DIR, file_name)
        
        # Скачиваем файл
        await bot.download(file_id, destination=file_path)
        
        # Получаем расширение файла
        kind = filetype.guess(file_path)
        
        ok_msg = f"Файл '{file_name}' успешно сохранен!"
        if kind != None:
            file_path_new = file_path.replace('.bin', '.'+ kind.extension)
            os.rename(file_path, file_path_new)
            file_name = file_name.replace('.bin', '.'+ kind.extension)
            ok_msg = f"Файл '{file_name}' успешно сохранен!"
            print(ok_msg)
            
        # Отправляем подтверждение пользователю
        await message.answer(ok_msg)

    except Exception as e:
        logger.error(f"Ошибка при обработке файла: {e}")
        await message.reply("Произошла ошибка при сохранении файла.")

# Запуск бота
async def main():
    try:
        await dp.start_polling(bot)
    except TokenValidationError:
        print("Ошибка: Неверный токен бота.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())