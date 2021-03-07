import os, shutil

def main():
    oldpath = 'X:/'
    namedate = str(input('xxx'))
    newpath = 'X:/'
    os.mkdir(newpath)  #创建文件夹
    for path, dirs, filelist in os.walk(oldpath):
        for f in filelist:
            shutil.move(f'{oldpath}/{f}', newpath)