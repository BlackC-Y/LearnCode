allline = [
'https://y.qq.com/n/yqq/song/000PFqzi38hAOf.html',



	]

import sys
import you_get
 
 
def download():
    for i in allline:
        if not i: continue
        sys.argv = ['you-get', '-o', 'D:/迅雷下载/', '--playlist', i]
        you_get.main()
 
if __name__ == '__main__':
    download()

#PowerShell Code
#you-get -o D:/迅雷下载/动态背景/明日方舟 --playlist https://www.bilibili.com/video/BV1ux41147Eh
#--format=dash-flv