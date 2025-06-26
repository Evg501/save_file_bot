import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.token import TokenValidationError
from aiogram import F
#from pack.file_lib import *
import filetype
from config import *
from config_hiden import *
from pack.date_lib import *
import logging
from pack.file_lib import *
from pack.async_lib import *
from pack.bot_lib import *
from rich import print

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("Бот запущен и готов к работе")

# Укажите токен вашего бота
#API_TOKEN = ''

# Укажите путь к папке, куда будут сохраняться файлы
#DOWNLOADS_DIR = './downloads'

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
        #print(message)
        if message.chat.type != "private":
            # Не отвечаем на сообщения из групп и каналов
            print('[grey53]'+"Не отвечаем на сообщения из групп и каналов")
            return
        is_file = True
        # В зависимости от типа файла получаем разные атрибуты
        if message.document:
        #    file = message.document        
            file_id = message.document.file_id
            file_size = message.document.file_size
            file_name = message.document.file_name or f"document_{file_id}"
            prefix='document_'
        elif message.photo:
            file_id = message.photo[-1].file_id  # Берем последнее (самое высокое) фото
            file_size = message.photo[-1].file_size
            file_name = f"photo_{file_id}.jpg"
            prefix='photo_'
        elif message.video:
            file_id = message.video.file_id
            file_size = message.video.file_size
            file_name = message.video.file_name or f"video_{file_id}.mp4"
            prefix='video_'
        elif message.audio:
            file_id = message.audio.file_id
            file_size = message.audio.file_size
            file_name = message.audio.file_name or f"audio_{file_id}.mp3"
            prefix='audio_'
        elif message.voice:
            file_id = message.voice.file_id
            file_size = message.voice.file_size
            file_name = f"voice_{file_id}.ogg"
            prefix='voice_'
        elif message.video_note:
            file_id = message.video_note.file_id
            file_size = message.video_note.file_size
            file_name = f"video_note_{file_id}.mp4"
            prefix='video_note_'
        else:
            is_file = False

        # save text
        if message.text!=None or message.caption!=None:
            #print(message.text)
            # Расширение файла не известно
            file_name_txt = genfname(pref='txt_', postf='.txt')
            # Формируем путь для сохранения файла
            file_path_txt = os.path.join(DOWNLOADS_DIR, file_name_txt)         
            #write_file(fname=file_path_txt, text=str(message.text or '') + str(message.caption or ''), e='utf8')
            write_file(fname=file_path_txt, text=f"{message.text or ''}{message.caption or ''}", e='utf8')
            print('[deep_pink4]'+f"Текст сохранён в {file_name_txt}")
            print('[spring_green4]' + f"{message.text or ''}{message.caption or ''}")
            await message.reply( f"Текст сохранён в {file_name_txt}")
            #return  

        # save file  
        if is_file:
            ok_msg = await save_file(bot, prefix, file_id, file_size)
                
            if ok_msg['result']==True:
                # Отправляем подтверждение пользователю
                await message.answer(ok_msg['msg'])
            else:
                print('[green]'+ok_msg['msg'])
                await message.answer('Ошибка')

    except Exception as e:
        logger.error(f"Ошибка при обработке файла: {e}")
        await message.reply("Произошла ошибка при сохранении файла.")

# Запуск бота
async def main():
    try:
        await dp.start_polling(bot)
    except TokenValidationError:
        print('[red]' + "Ошибка: Неверный токен бота.")
    except Exception as e:
        print('[red]'+ f"Произошла ошибка: {e}")

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())