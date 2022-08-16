# -*- coding: UTF-8 -*-
from maya import cmds, mel


class DataSaveUi():

    def ToolUi(self):
        Ver = 1.24
        self.UiN = 'DataSaveUi'
        UiN = self.UiN
        if cmds.window(UiN, q=1, ex=1):
            cmds.deleteUI(UiN)
        cmds.window(UiN, t='%s %s' %(UiN, Ver), rtf=1, mb=1, tlb=1, wh=(250, 150))
        cmds.columnLayout('%s_MaincL' % UiN, cat=('both', 2), rs=2, cw=250, adj=1)
        cmds.rowLayout(nc=2, adj=1)
        cmds.text(l='', w=225)
        cmds.iconTextButton(i='addClip.png', w=20, h=20, c=lambda *args: self.addUiComponent())
        cmds.setParent('..')
        cmds.showWindow(UiN)
        self.ComponentData = {}
        self.addUiComponent()

    def addUiComponent(self):
        UiN = self.UiN
        uiNum = len(cmds.columnLayout('%s_MaincL' % UiN, q=1, ca=1))
        cmds.columnLayout('%s_ComponentcL%s' % (UiN, uiNum), p='%s_MaincL' % UiN, cat=('both', 2), rs=2, cw=240, adj=1)
        cmds.rowLayout(nc=2)
        cmds.button(l='Save', w=120)
        cmds.popupMenu(b=1)
        cmds.menuItem(l=u'名称(用于再次选择)', c=lambda *args: self.saveData('Name', uiNum))
        cmds.menuItem(l=u'位移和旋转(用于选择物体对位)', c=lambda *args: self.saveData('Position', uiNum))
        cmds.menuItem(l=u'中心位置(用于选择物体对位)', c=lambda *args: self.saveData('CenterPosition', uiNum))
        cmds.menuItem(l=u'物体蒙皮骨骼(用于再次选择)', c=lambda *args: self.saveData('SkinJoint', uiNum))
        cmds.menuItem(l=u'物体颜色(用于给其他物体上色)', c=lambda *args: self.saveData('ShapeColor', uiNum))
        cmds.button(l='Get', w=120, c=lambda *args: self.getData(uiNum))
        cmds.setParent('..')
        cmds.text('%s_ComponentText%s' % (UiN, uiNum), l='')
        cmds.popupMenu()
        cmds.menuItem(l=u'删除槽位', c=lambda *args: cmds.columnLayout('%s_ComponentcL%s' % (UiN, uiNum), e=1, vis=0))
        #cmds.menuItem(l=u'删除槽位', c=lambda *args: cmds.deleteUI('%s_ComponentcL%s' %(UiN, uiNum), lay=1))
        # 直接deleteUI时，导致数量和序号不匹配。再次添加时如果报错，Maya可能直接崩。

    def saveData(self, Type, uiNum):
        UiN = self.UiN
        if Type == 'Name':
            slList = cmds.ls(sl=1)
            if not slList:
                return
            self.ComponentData['Data%s' % uiNum] = slList
            cmds.text('%s_ComponentText%s' % (UiN, uiNum), e=1, l=u'已储存 名称')

        elif Type == 'Position':
            slList = cmds.ls(sl=1)
            if len(slList) != 1:
                cmds.warning(u'只能选择一个物体')
                return
            _temploc_ = cmds.spaceLocator()
            cmds.delete(cmds.parentConstraint(slList[0], _temploc_, w=1))
            self.ComponentData['Data%s' % uiNum] = [cmds.xform(_temploc_, q=1, ws=1, t=1), cmds.xform(_temploc_, q=1, ws=1, ro=1)]
            cmds.delete(_temploc_)
            cmds.text('%s_ComponentText%s' % (UiN, uiNum), e=1, l=u'已储存 位移和旋转')

        elif Type == 'CenterPosition':
            slList = cmds.ls(sl=1, fl=1)
            if not slList:
                return
            _tempobj_ = []
            if len(cmds.ls(slList, typ='transform')) == len(slList):   #簇点对Locator无效
                for i in slList:
                    _temp_ = cmds.polyCube(ch=0)[0]
                    _tempobj_.append(_temp_)
                    cmds.delete(cmds.parentConstraint(i, _temp_, w=1))
                _tempclu_ = cmds.cluster(_tempobj_)[1]
            else:
                _tempclu_ = cmds.cluster()[1]
            self.ComponentData['Data%s' % uiNum] = cmds.getAttr('%sShape.origin' %_tempclu_)[0]
            cmds.delete(_tempclu_, _tempobj_)
            cmds.text('%s_ComponentText%s' % (UiN, uiNum), e=1, l=u'已储存 中心位置')

        elif Type == 'SkinJoint':
            slList = cmds.ls(sl=1, o=1)
            if len(slList) != 1:
                cmds.warning(u'只能选择一个物体')
                return
            jointlist = cmds.skinCluster(slList, q=1, inf=1)
            self.ComponentData['Data%s' % uiNum] = jointlist
            cmds.text('%s_ComponentText%s' % (UiN, uiNum), e=1, l=u'已储存 蒙皮骨骼')

        elif Type == "ShapeColor":
            slList = cmds.ls(sl=1, o=1)
            if len(slList) != 1:
                cmds.warning(u'只能选择一个物体')
                return
            objShape = cmds.listRelatives(slList, c=1, s=1)
            if not objShape:
                if not cmds.ls(slList, typ='joint'):
                    return
                objShape = slList
            self.ComponentData['Data%s' % uiNum] = [cmds.getAttr("%s.overrideEnabled" %objShape[0]),
                                                    cmds.getAttr("%s.overrideRGBColors" %objShape[0]),
                                                    cmds.getAttr("%s.overrideColor" %objShape[0]),
                                                    cmds.getAttr("%s.overrideColorRGB" %objShape[0])[0]]
            cmds.text('%s_ComponentText%s' % (UiN, uiNum), e=1, l=u'已储存 物体颜色')

    def getData(self, uiNum):
        UiN = self.UiN
        typString = cmds.text('%s_ComponentText%s' %(UiN, uiNum), q=1, l=1)
        data = self.ComponentData['Data%s' % uiNum]
        lsList = cmds.ls(sl=1)
        if not data or not typString:
            return
        
        if typString == u'已储存 名称':
            cmds.select(data, add=1)

        elif typString == u'已储存 位移和旋转':
            if not lsList:
                return
            _temploc_ = cmds.spaceLocator()[0]
            cmds.xform(_temploc_, ws=1, t=data[0])
            cmds.xform(_temploc_, ws=1, ro=data[1])
            for i in lsList:
                cmds.delete(cmds.parentConstraint(_temploc_, i, w=1))
            cmds.delete(_temploc_)

        elif typString == u'已储存 中心位置':
            if not lsList:
                return
            _temploc_ = cmds.spaceLocator()[0]
            cmds.setAttr(_temploc_ + '.t', data[0], data[1], data[2])
            for i in lsList:
                cmds.delete(cmds.pointConstraint(_temploc_, i, w=1))
            cmds.delete(_temploc_)

        elif typString == u'已储存 蒙皮骨骼':
            cmds.select(data, r=1)

        elif typString == u'已储存 物体颜色':
            slList = cmds.ls(sl=1, o=1)
            if len(slList) != 1:
                cmds.warning(u'只能选择一个物体')
                return
            objShape = cmds.listRelatives(slList, c=1, s=1)
            if not objShape:
                if not cmds.ls(slList, typ='joint'):
                    return
                objShape = slList
            cmds.setAttr("%s.overrideEnabled" %objShape[0], data[0])
            cmds.setAttr("%s.overrideRGBColors" %objShape[0], data[1])
            if data[1]:
                cmds.setAttr("%s.overrideColorRGB" %objShape[0], data[3][0], data[3][1], data[3][2])
            else:
                cmds.setAttr("%s.overrideColor" %objShape[0], data[2])

#DataSaveUi().ToolUi()