import filetype

def main():
    #kind = filetype.guess('tests/fixtures/sample.jpg')
    kind = filetype.guess('downloads/photo_20250423-102126.bin')
    if kind is None:
        print('Cannot guess file type!')
        return

    print('File extension: %s' % kind.extension)
    print('File MIME type: %s' % kind.mime)

if __name__ == '__main__':
    main()