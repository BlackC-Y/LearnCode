allline = [
'https://www.bilibili.com/video/BV1QZ4y1T7mH',
'',




	]

import sys
import you_get
 
 
def download():
    for i in allline:
        if not i: continue
        sys.argv = ['you-get', '-o', 'D:/下载/方舟OST', '--playlist', i]
        you_get.main()
 
if __name__ == '__main__':
    download()


#https://www.bilibili.com/video/BV1QZ4y1T7mH
#'D:/下载/明日方舟'   



#PowerShell Code
#you-get -o D:/迅雷下载/动态背景/明日方舟 --playlist https://www.bilibili.com/video/BV1ux41147Eh