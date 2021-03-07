import os

def main():
    spath = 'D:/下载/明日方舟1'
    topath = 'D:/下载/明日方舟'
    for root, dirs, files in os.walk(spath):
        for f in files:
            with open(f'{topath}/{f}', 'w') as of:
                of.write('Null')
                print(f)

if __name__ == "__main__":
    main()