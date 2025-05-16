import os
from pack.date_lib import *
from config import *
from config_hiden import *
import filetype
import traceback
from pack.async_lib import *

async def save_file(bot, prefix, file_id, file_size):
    try:
        # Расширение файла не известно
        file_name = genfname(pref=prefix, postf='.bin')
        
        # Формируем путь для сохранения файла
        file_path = os.path.join(DOWNLOADS_DIR, file_name)
        
        # Скачиваем файл
        await bot.download(file=file_id, destination=file_path, timeout = 3600)
        #await download_(bot=bot, file_id=file_id, src_path=file_path)
        wffs = await wait_for_file_size(file_path=file_path, expected_size=file_size)
        if not wffs:
            return {'result':False, 'msg':'Таймаут: не удалось дождаться нужного размера файла'}
        
        # Получаем расширение файла
        kind = filetype.guess(file_path)
        
        ok_msg = f"Файл '{file_name}' успешно сохранен!"
        if kind != None:
            file_path_new = file_path.replace('.bin', '.'+ kind.extension)
            os.rename(file_path, file_path_new)
            #await wait_rename(file_path, file_path_new)
            file_name = file_name.replace('.bin', '.'+ kind.extension)
            ok_msg = f"Файл '{file_name}' успешно сохранен!"
            print(ok_msg)
        return {'result':True, 'msg':ok_msg}
    except Exception as e:
        #return str(e) + traceback.format_exc()
        return {'result':False, 'msg':str(e) + traceback.format_exc()}
