#import maya.cmds as cmds
import re

a_file = open('C:/Users/donghua/Desktop/tes1t.ma')
fileNode = []
fileNodeadd = []
audioNode = []
audioNodeadd = []
referenceNode = []
referenceNodeadd = []
try:
    y = 0
    rlines = a_file.readlines()
    for line in rlines:
        if 'createNode file' in line:
            fileNode.append(re.findall(r"\"(.+?)\"",line))
            while True:
                if 'setAttr ".ftn" -type' in rlines[y]:
                    fileNodeadd.append(re.findall(r"\"(.+?)\"",rlines[y])[2])
                    break
                y += 1
        elif 'createNode audio' in line:
            audioNode.append(re.findall(r"\"(.+?)\"",line))
            while True:
                if 'setAttr ".f" -type' in rlines[y]:
                    audioNodeadd.append(re.findall(r"\"(.+?)\"",rlines[y])[2])
                    break
                y += 1
        elif 'createNode reference' in line:
            referenceNode.append(re.findall(r"\"(.+?)\"",line))
            while True:
                for r in referenceNode:
                    print r[0]
                    if 'file -rdi 1 -ns "*" -rfn "'+r[0]+'"' in line:
                        print ('aa')
                        referenceNodeadd.append(re.findall(r"\"(.+?)\"",line)[4])
                break
        y += 1
finally:
    a_file.close()

print (fileNode)
print (fileNodeadd)
print (audioNode)
print (audioNodeadd)
print (referenceNode)
print (referenceNodeadd)

