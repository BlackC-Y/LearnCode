import zipfile, os

def main():
    spath = 'E:/F/Evermotion Archmodels/'
    for path, dirs, filelist in os.walk(spath):
        for f in filelist:
            with zipfile.ZipFile(spath + f, mode='r') as onezip:
                fn = f.split('.', 1)[0]
                onezip.extract(f'{fn}/previews/{fn}.pdf', 'E:/F/export')

if __name__ == "__main__":
    main()