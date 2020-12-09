import os

def main():
    sourpath = 'D:/迅雷下载/灯泡小剧场/P1/'
    scpath = 'D:/迅雷下载/灯泡小剧场/P1/sc/'
    if os.path.exists(sourpath + 'hvc') or os.path.exists(sourpath + 'heic'):
        raise FileExistsError('Folder is exist.')
    os.makedirs(sourpath + 'hvc')
    os.makedirs(sourpath + 'heic')
    for path, dirs, filelist in os.walk(scpath):
            for f in filelist:
                fn = f.split('.')[0]
                os.system('ffmpeg -i "%s" -crf 10 -pix_fmt yuv420p -sws_flags spline+accurate_rnd+full_chroma_int \
                            -color_range 1 -colorspace 5 -color_primaries 5 -color_trc 6 -f hevc "%s"'
                            % (scpath + f,  '%shvc/%s.hvc' % (sourpath, fn)))
                os.system('D:/Program Files (x86)/mp4box/mp4box.exe -add-image "%s:primary" -ab heic -new "%s"'
                            % ('%shvc/%s.hvc' % (sourpath, fn), '%s/heic/%s.heic' % (sourpath, fn)))

if __name__ == "__main__":
    main()