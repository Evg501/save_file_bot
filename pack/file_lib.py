import os.path
from pathlib import Path
from os import listdir
from os.path import isfile, join
import requests
import math
import shutil

# 'cp1251'  'utf-8'
def read_file(fname, e=''):
    if e=='':
        with open(fname, 'r') as file:
            data = file.read().rstrip()
    else:
        with open(fname, mode='r', encoding=e) as file:
            data = file.read().rstrip()
    return data

def write_file(fname, text, e='', mode='w'):
    if e=='':
        f = open( file=fname, mode=mode )
    else:
        f = open( file=fname, mode=mode, encoding='utf-8' )
    f.write( text )
    f.close()

#def write_file_old2(fname, text):
#    f = open( fname, 'w', encoding='utf-8' )
#    f.write( text )
#    f.close()

def get_curr_dir(arg1=__file__):
    return os.path.dirname(arg1)

def get_parent_dir(arg1):
    return str(Path(arg1).parent.parent)

def mkdir_if_no_exist(d):
    if not os.path.exists(d):
        os.makedirs(d)

def file_exists(f):
    return os.path.exists(f)

#def write_file_old(fname, text):
#    f = codecs.open( fname, 'w', "utf-8" )
#    f.write( text )
#    f.close()

def num_lines(in_file):
    num_lines = sum(1 for line in open(in_file))
    return num_lines

def num_files(tmp_dir):
    onlyfiles = [f for f in listdir(tmp_dir) if isfile(join(tmp_dir, f))]
    return len(onlyfiles)

"""
def find_files(tmp_dir):
    onlyfiles = [join(tmp_dir, f) for f in listdir(tmp_dir) if isfile(join(tmp_dir, f))]
    return onlyfiles

def delete_old_files(fold, save_count=10):
    l = find_files(fold)
    #l.sort(key=lambda x: os.path.getmtime(x))
    l.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    i=0
    for f in l:
        if i>save_count:
            os.remove(f)
#            print("delete" , f  )
        else:
            pass
#            print("ok" , f  )
        i = i + 1
"""

def check_extention(f, ext=[]):
    #filename, file_extension = os.path.splitext('/path/to/somefile.ext')
    filename, file_extension = os.path.splitext( f )
    #print(file_extension)
    if file_extension in ext:
        return True
    else:
        return False

def find_files(tmp_dir, ext=[]):
    #print(len(ext))
    if len(ext)>0:
        onlyfiles = [join(tmp_dir, f) for f in listdir(tmp_dir) if isfile(join(tmp_dir, f)) and check_extention(join(tmp_dir, f), ext)]
    else:
        onlyfiles = [join(tmp_dir, f) for f in listdir(tmp_dir) if isfile(join(tmp_dir, f))]
    return onlyfiles

def delete_old_files(fold, save_count=10, ext=[]):
    l = find_files(fold, ext)
    #l.sort(key=lambda x: os.path.getmtime(x))
    l.sort(key=lambda x: os.path.getmtime(x), reverse=True) # сортировка по дате файла
    i=0
    for f in l:
        if i>save_count:
#            os.remove(f)
            print("delete" , f  )
        else:
            pass
#            print("ok" , f  )
        i = i + 1

def find_folders(tmp_dir):
    #print(len(ext))
    data = [join(tmp_dir, f) for f in listdir(tmp_dir) if not isfile(join(tmp_dir, f))]
    return data

# Здесь происходит удаление папки
#shutil.rmtree(file_location, ignore_errors=False)
def delete_old_folders(fold, save_count=10):
    l = find_folders(fold)
    #l.sort(key=lambda x: os.path.getmtime(x))
    l.sort(key=lambda x: os.path.getmtime(x), reverse=True) # сортировка по дате файла
    i=0
    for f in l:
        if i>=save_count:
            #os.remove(f)
            #shutil.rmtree(f, ignore_errors=False)
            print("delete" , f  )
        else:
            pass
#            print("ok" , f  )
        i = i + 1

def download_file(urlfile, path, check_exist=False, schema=''):
    if 'https' not in urlfile and 'http' not in urlfile:
        urlfile = schema + urlfile
    fname = os.path.basename(urlfile)
    myfile = requests.get(urlfile)
    full_name = os.path.join(path, fname)
    if check_exist:
        if not os.path.exists(full_name):
            print( 'download: ' + fname )        
            return open( full_name, 'wb').write(myfile.content)
        else:
            print('file exists: ' + fname)
    else:
        print( 'rewrite: ' + fname )
        return open(full_name, 'wb').write(myfile.content)

# val b - byte , mb - megabytes
# 1 MB = 1 048 576 B
def fsize(f, val='mb'):
    #num = 3.458
    #res = math.ceil(num)
    if val=='b':
        return os.path.getsize(f)
    if val=='mb':
        #return math.ceil(os.path.getsize(f)/1048576)
        return os.path.getsize(f)/1048576
    #os.path.getsize("/path/to/file.mp3")
    
def file_sz_msg1(fn):
    sfn = fsize(fn)
    print("размер файла: ", sfn, " ", fn)
    if sfn>50:
        print("размер файла превышает 50 мегабайт!")