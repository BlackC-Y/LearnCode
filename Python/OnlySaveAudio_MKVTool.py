import os

def main():
    spath = 'D:/下载/明日方舟1'
    topath = 'D:/下载/明日方舟2'
    audioType = 'aac'
    for root, dirs, files in os.walk(spath):
            for f in files:
                os.system(f'D:/下载/STEAMM/mkvtoolnix/mkvmerge.exe --ui-language zh_CN --output "{topath}/{f.split('.flv')[0]}.{audioType}" --no-video 
                            --language 1:und "{spath}/{f}"')

if __name__ == "__main__":
    main()