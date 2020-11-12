# -*- coding: UTF-8 -*-
from maya import cmds, mel

class DataSaveUi():

    __Verision = 1.12

    def Ui(self):
        self.UiN = 'DataSaveUi'
        UiN = self.UiN
        if cmds.window(UiN, q=1, ex=1):
            cmds.deleteUI(UiN)
        cmds.window(UiN, t=UiN, rtf=1, mb=1, mxb=0, wh=(250, 150))
        cmds.columnLayout('%s_MaincL' %UiN, cat=('both', 2), rs=2, cw=250, adj=1)
        cmds.rowLayout(nc=2, adj=1)
        cmds.text(l='', w=225)
        cmds.iconTextButton(i='addClip.png', w=20, h=20, c=lambda *args: self.addUiComponent())
        cmds.setParent('..')
        cmds.showWindow(UiN)
        self.addUiComponent()

    def addUiComponent(self):
        UiN = self.UiN
        #uiNum = 1 if mode == 'First' else int(cmds.columnLayout('%s_MaincL' %UiN, q=1, ca=1)[-1][-1]) + 1
        uiNum = len(cmds.columnLayout('%s_MaincL' %UiN, q=1, ca=1))
        cmds.columnLayout('%s_ComponentcL%s' %(UiN, uiNum), p='%s_MaincL' %UiN, cat=('both', 2), rs=2, cw=240, adj=1)
        cmds.rowLayout(nc=2)
        cmds.button(l='Save', w=120)
        cmds.popupMenu(b=1)
        cmds.menuItem(l=u'名称(用于再次选择)', c=lambda *args: self.saveData('Name', uiNum))
        cmds.menuItem(l=u'位置(用于选择物体对位)', c=lambda *args: self.saveData('Position', uiNum))
        cmds.menuItem(l=u'中心位置(用于选择物体对位)', c=lambda *args: self.saveData('CenterPosition', uiNum))
        cmds.button(l='Get', w=120, c=lambda *args: self.getData(uiNum))
        cmds.setParent('..')
        cmds.text('%s_ComponentText%s' %(UiN, uiNum), l='')
        cmds.popupMenu()
        cmds.menuItem(l=u'删除槽位', c=lambda *args: cmds.columnLayout('%s_ComponentcL%s' %(UiN, uiNum), e=1, vis=0))
        #cmds.menuItem(l=u'删除槽位', c=lambda *args: cmds.deleteUI('%s_ComponentcL%s' %(UiN, uiNum), lay=1))
        #直接deleteUI时，导致数量和序号不匹配。再次添加时如果报错，Maya可能直接崩。
        cmds.text('%s_ComponentData%s' %(UiN, uiNum), l='', vis=0)

    def saveData(self, Type, uiNum):
        UiN = self.UiN
        if Type == 'Name':
            slList = cmds.ls(sl=1)
            if not slList:
                return
            cmds.text('%s_ComponentData%s' %(UiN, uiNum), e=1, l=str(slList))
            cmds.text('%s_ComponentText%s' %(UiN, uiNum), e=1, l=u'已储存 名称')
        elif Type == 'Position':
            slList = cmds.ls(sl=1)
            if len(slList) != 1:
                cmds.warning(u'只能选择一个物体')
                return
            _temploc_ = cmds.spaceLocator()
            cmds.delete(cmds.parentConstraint(slList[0], _temploc_, w=1))
            _data = '[%s, %s]' %(cmds.xform(_temploc_, q=1, ws=1, t=1), cmds.xform(_temploc_, q=1, ws=1, ro=1))
            cmds.delete(_temploc_)
            cmds.text('%s_ComponentData%s' %(UiN, uiNum), e=1, l=_data)
            cmds.text('%s_ComponentText%s' %(UiN, uiNum), e=1, l=u'已储存 位置')
        elif Type == 'CenterPosition':
            slList = cmds.ls(sl=1)
            if not slList:
                return
            _tempclu_ = cmds.cluster()[1]
            cmds.text('%s_ComponentData%s' %(UiN, uiNum), e=1, l=str(cmds.getAttr(_tempclu_ + 'Shape.origin')[0]))
            cmds.text('%s_ComponentText%s' %(UiN, uiNum), e=1, l=u'已储存 中心位置')
            cmds.delete(_tempclu_)

    def getData(self, uiNum):
        UiN = self.UiN
        typString = cmds.text('%s_ComponentText%s' %(UiN, uiNum), q=1, l=1)
        data = cmds.text('%s_ComponentData%s' %(UiN, uiNum), q=1, l=1)
        if not data or not typString:
            return
        data = eval(data)
        print(data)
        if typString == u'已储存 名称':
            cmds.select(data, add=1)
        elif typString == u'已储存 位置':
            lsList = cmds.ls(sl=1)
            _temploc_ = cmds.spaceLocator()[0]
            cmds.xform(_temploc_, ws=1, t=data[0])
            cmds.xform(_temploc_, ws=1, ro=data[1])
            for i in lsList:
                cmds.delete(cmds.pointConstraint(_temploc_, i, w=1))
            cmds.delete(_temploc_)
        elif typString == u'已储存 中心位置':
            lsList = cmds.ls(sl=1)
            _temploc_ = cmds.spaceLocator()[0]
            cmds.setAttr(_temploc_ + '.t', data[0], data[1], data[2])
            for i in lsList:
                cmds.delete(cmds.pointConstraint(_temploc_, i, w=1))
            cmds.delete(_temploc_)

DataSaveUi().Ui()
