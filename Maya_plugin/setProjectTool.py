from maya import cmds, mel
import maya.OpenMaya as Om
import os, re

class setProjectTool():

    def __init__(self):
        self.filePath = os.path.expanduser("~") + '/maya/ProjectList'

    def setProjectUi(self):
        Ui = 'setProject'
        if cmds.window(Ui, q=1, ex=1):
            cmds.deleteUI(Ui)
        cmds.window(Ui, t=Ui, rtf=1, mb=1, mxb=0, wh=(230, 50))
        cmds.columnLayout(cat=('both', 2), rs=3, cw=230)
        cmds.optionMenu('ProjectList', l='ProjectPath')
        cmds.button(h=24, l='Set', c=lambda *args: mel.eval('setProject \"%s\";print "Finish!"' %cmds.optionMenu('ProjectList', q=1, v=1).strip()))
        cmds.popupMenu('rightC')
        cmds.menuItem(p='rightC', l='Add Project', c=lambda *args: self.refreshList('add'))
        cmds.menuItem(p='rightC', l='Delete Path', c=lambda *args: self.refreshList('delete'))
        cmds.showWindow(Ui)
        self.refreshList(None)
    
    def refreshList(self, mode):
        if mode == 'add':
            if cmds.promptDialog(t='PojectPath', m='eg: C:/xxx/xxx', b=['OK', 'Cancel'], db='OK', cb='Cancel', ds='Cancel') == 'OK':
                newPath = cmds.promptDialog(q=1, t=1)
                if not newPath:
                    return
                elif '\\' in newPath:
                    Om.MGlobal.displayError('The "\\" is wrong!')
                    return
                elif not os.path.exists(newPath):
                    Om.MGlobal.displayError('Path not exist!')
                    return
                elif not re.match('.:/\S', newPath) and not re.match('\\\\\S', newPath):
                    Om.MGlobal.displayError('Path is wrong!')
                    return
                with open(self.filePath, 'a') as listFile:
                    listFile.write(newPath + ';')
            self.refreshList(None)
        elif mode == 'delete':
            dPath = cmds.optionMenu('ProjectList', q=1, v=1)
            with open(self.filePath, 'r') as listFile:
                allPath = listFile.readline().split(';')
            with open(self.filePath, 'w') as listFile:
                for i in allPath:
                    if i and i != dPath:
                        listFile.write(i + ';')
            self.refreshList(None)
        else:
            oldList = cmds.optionMenu('ProjectList', q=1, ill=1)
            if oldList:
                for i in oldList:
                    cmds.deleteUI(i)
            with open(self.filePath, 'r') as listFile:
                allPath = listFile.readline().split(';')
                for i in allPath:
                    if i:
                        cmds.menuItem(p='ProjectList', l=i)

setProjectTool().setProjectUi()