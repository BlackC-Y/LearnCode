# -*- coding: UTF-8 -*-
'''Roadmap:
'''
from PySide2 import QtCore, QtGui, QtWidgets
import shiboken2
from maya import cmds, mel
from maya import OpenMaya as Om, OpenMayaAnim as OmAni, OpenMayaUI as OmUI
from maya.api import OpenMaya as om, OpenMayaAnim as omAni
import decimal


class WeightTool_JellyBean():

    #__Verision = 0.85

    def ToolUi(self):
        ToolUi = 'WeightTool_JellyBean'
        if cmds.window(ToolUi, q=1, ex=1):
            cmds.deleteUI(ToolUi)
        cmds.window(ToolUi, t='WeightTool', rtf=1, mb=1, mxb=0, wh=(230, 500))
        cmds.menu(l='SkinT', to=1)
        cmds.menuItem(d=1, dl="S/L")
        cmds.menuItem(l='Save', c=lambda *args: self.vtxSave_api())
        cmds.menuItem(l='Load', c=lambda *args: self.vtxLoad_api())
        cmds.menuItem(d=1)
        cmds.menuItem(l='WeightCheck', c=lambda *args: WeightCheckTool_JellyBean().ToolUi())
        cmds.menuItem(l='reset SkinPose', c=lambda *args: self.resetSkinPose())
        cmds.menu(l='RigT', to=1)
        cmds.menuItem(l='Create', c=lambda *args: self.createSelect())
        cmds.menuItem(l='Get', c=lambda *args: self.getSelect())
        cmds.columnLayout('FiristcL_JellyBean', cat=('both', 2), rs=2, cw=220, adj=1)
        cmds.text('spJobchangeVtx_JellyBean', p='FiristcL_JellyBean', vis=0)
        cmds.scriptJob(e=['SelectTypeChanged', 'WeightTool_JellyBean().refreshBoxChange(None)'], p='spJobchangeVtx_JellyBean')
        cmds.rowLayout(nc=6, adj=2)
        cmds.iconTextCheckBox('refresh_JellyBean', i='refresh.png', w=20, h=20,
                              onc=lambda *args: self.spJobStart(), ofc=lambda *args: self.refreshBoxChange(9))
        cmds.popupMenu()
        cmds.menuItem('OFFmeunItem_JellyBean', l='OFF', cb=0)
        cmds.textField('searchText_JellyBean', h=22, tcc=lambda *args: self.refreshJointList(1, cmds.textField('searchText_JellyBean', q=1, tx=1)))
        cmds.popupMenu()
        cmds.radioMenuItemCollection()
        cmds.menuItem('HImeunItem_JellyBean', l='Hierarchy', rb=1, c=lambda *args: self.refreshJointList(1))
        cmds.menuItem('AImeunItem_JellyBean', l='Alphabetically', rb=0, c=lambda *args: self.refreshJointList(1))
        cmds.menuItem('FImeunItem_JellyBean', l='Filter Zero', cb=0, c=lambda *args: self.refreshJointList(1))
        # cmds.iconTextButton(i='expandInfluenceList.png', w=20, h=20,
        #    c=lambda *args: cmds.treeView('JointTV_JellyBean', e=1, h=cmds.treeView('JointTV_JellyBean', q=1, h=1) + 20))
        # cmds.iconTextButton(i='retractInfluenceList.png', w=20, h=20,
        #    c=lambda *args: cmds.treeView('JointTV_JellyBean', e=1, h=cmds.treeView('JointTV_JellyBean', q=1, h=1) - 20))
        # invertSelection.png
        cmds.iconTextButton(i='invertSelection.png', w=20, h=20, c=self.reSelect)
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.formLayout('JointTVLayout_JellyBean')
        cmds.treeView('JointTV_JellyBean', nb=1, h=100, scc=self._weightView, pc=(1, self.lock_unLock))
        cmds.text('saveData_JellyBean', l='', vis=0)
        cmds.popupMenu()
        #cmds.menuItem(l='Lock All')
        #cmds.menuItem(l='Unlock All')
        cmds.menuItem(l='Select Vtx', c=lambda *args: self.slVtx())
        cmds.formLayout('JointTVLayout_JellyBean', e=1, af=[('JointTV_JellyBean', 'top', 0), ('JointTV_JellyBean', 'bottom', 0),
                                                            ('JointTV_JellyBean', 'left', 3), ('JointTV_JellyBean', 'right', 3)])
        cmds.setParent('..')
        cmds.columnLayout(cat=('both', 2), rs=2, cw=225)
        cmds.rowLayout(nc=4, cw4=(50, 50, 50, 65))
        cmds.floatField('weighrfloat_JellyBean', w=52, h=26, pre=4, min=0, max=1,
                        ec=lambda *args: self.editVtxWeight(cmds.floatField('weighrfloat_JellyBean', q=1, v=1)))
        cmds.button(w=50, h=26, l='Copy', c=lambda *args: self.copyVtxWeight())
        cmds.button(w=50, h=26, l='Paste', c=lambda *args: self.pasteVtxWeight())
        cmds.popupMenu()
        cmds.menuItem(l='PasteAll', c=lambda *args: mel.eval("polyConvertToShell;artAttrSkinWeightPaste;"))
        cmds.button(w=65, h=26, l='Hammer', c=lambda *args: (mel.eval('weightHammerVerts'), self.refreshJointList(0)))
        cmds.setParent('..')
        cmds.rowLayout(nc=5, cw5=(43, 43, 43, 43, 43))
        cmds.button(w=43, h=26, l='Loop', c=lambda *args: cmds.polySelectSp(loop=1))
        cmds.button(w=43, h=26, l='Ring',
                    c=lambda *args: mel.eval("PolySelectConvert 2;PolySelectTraverse 2;polySelectEdges edgeRing;PolySelectConvert 3;"))
        cmds.button(w=43, h=26, l='Shell', c=lambda *args: mel.eval("polyConvertToShell"))
        cmds.button(w=43, h=26, l='Shrink', c=lambda *args: cmds.polySelectConstraint(pp=2))
        cmds.button(w=43, h=26, l='Grow', c=lambda *args: cmds.polySelectConstraint(pp=1))
        cmds.setParent('..')
        cmds.rowLayout(nc=7, cw=[(1, 30), (2, 30), (3, 30), (4, 30), (5, 30), (6, 30), (7, 30)])
        cmds.button(w=30, h=26, l='0', c=lambda *args: self.editVtxWeight(0))
        cmds.button(w=30, h=26, l='.1', c=lambda *args: self.editVtxWeight(.1))
        cmds.button(w=30, h=26, l='.25', c=lambda *args: self.editVtxWeight(.25))
        cmds.button(w=30, h=26, l='.5', c=lambda *args: self.editVtxWeight(.5))
        cmds.button(w=30, h=26, l='.75', c=lambda *args: self.editVtxWeight(.75))
        cmds.button(w=30, h=26, l='.9', c=lambda *args: self.editVtxWeight(.9))
        cmds.button(w=30, h=26, l='1', c=lambda *args: self.editVtxWeight(1))
        cmds.setParent('..')
        cmds.rowLayout(nc=4, cw4=(80, 60, 38, 38))
        cmds.text(l='A/S Weight', w=80)
        cmds.floatField('ASFloat_JellyBean', v=0.05, h=26, w=50, pre=3, min=0, max=1)
        cmds.button(w=38, h=26, l='+', c=lambda *args: self.editVtxWeight('+'))
        cmds.button(w=38, h=26, l='-', c=lambda *args: self.editVtxWeight('-'))
        cmds.setParent('..')
        cmds.rowLayout(nc=4, cw4=(80, 60, 38, 38))
        cmds.text(l='M/D Weight', w=80)
        cmds.floatField('MDFloat_JellyBean', v=0.95, h=26, w=50, pre=3, min=0, max=1)
        cmds.button(w=38, h=26, l='*', c=lambda *args: self.editVtxWeight('*'))
        cmds.button(w=38, h=26, l='/', c=lambda *args: self.editVtxWeight('/'))
        cmds.setParent('..')

        cmds.showWindow(ToolUi)

    def spJobStart(self):
        if cmds.text('spJobVtxParent_JellyBean', q=1, ex=1):
            return
        cmds.text('spJobVtxParent_JellyBean', p='FiristcL_JellyBean', vis=0)
        cmds.scriptJob(e=['Undo', 'WeightTool_JellyBean().refreshJointList(0)'], p='spJobVtxParent_JellyBean')
        cmds.scriptJob(e=['SelectionChanged', 'WeightTool_JellyBean().refreshJointList(0)'], p='spJobVtxParent_JellyBean')
        #cmds.scriptJob(e=['ToolChanger', '自毁'], p='spJobVtxParent_JellyBean')
        cmds.scriptJob(uid=['WeightTool_JellyBean', 'WeightTool_JellyBean().refreshBoxChange(9)'])

        PaintSkinCmd = '"ArtPaintSkinWeightsToolOptions;"'
        if int(cmds.about(v=1)) > 2017:
            edgeCmd = '("doMenuComponentSelectionExt(\\\"" + $object + "\\\", \\\"edge\\\", 0);")'
            vertexCmd = '("doMenuComponentSelectionExt(\\\"" + $object + "\\\", \\\"vertex\\\", 0);")'
            faceCmd = '("doMenuComponentSelectionExt(\\\"" + $object + "\\\", \\\"facet\\\", 0);")'
            objModeCmd = '"maintainActiveChangeSelectMode time1 0;"'  # python (\\\"WeightTool_JellyBean().refreshBoxChange(9)\\\");
        else:   #2017以下兼容
            edgeCmd = '("doMenuComponentSelection(\\\"" + $object + "\\\", \\\"edge\\\");")'
            vertexCmd = '("doMenuComponentSelection(\\\"" + $object + "\\\", \\\"vertex\\\");")'
            faceCmd = '("doMenuComponentSelection(\\\"" + $object + "\\\", \\\"facet\\\");")'
            objModeCmd = '"changeSelectMode -component;changeSelectMode -object;"'
        mel.eval('global proc dagMenuProc(string $parent, string $object){ \
                if(!size($object)){ \
                string $lsList[] = `ls -sl -o`; if(!size($lsList)){return;} else{$object = $lsList[0];}} \
                if(objectType($object) == "joint"){ \
                string $selCmd = "python(\\\"cmds.treeView(\'JointTV_JellyBean\', e=1, cs=1);cmds.treeView(\'JointTV_JellyBean\', e=1, si=(\'" + $object + "\', 1));WeightTool_JellyBean()._weightView()\\\")"; \
                menuItem -l "Select Influence" -ec true -c $selCmd -rp "N" -p $parent; \
                }else{ \
                menuItem -l "Paint Skin Weights Tool" -ec true -c %s -rp "NW" -p $parent; \
                menuItem -l "Vertex" -ec true -c %s -rp "W" -p $parent; \
                menuItem -l "Edge" -ec true -c %s -rp "N" -p $parent; \
                menuItem -l "Face" -ec true -c %s -rp "S" -p $parent; \
                menuItem -l "Object Mode" -ec true -c %s -rp "NE" -p $parent;}}'
                 % (PaintSkinCmd, vertexCmd, edgeCmd, faceCmd, objModeCmd))

    def refreshBoxChange(self, force):
        if force == 9 or cmds.menuItem('OFFmeunItem_JellyBean', q=1, cb=1):
            if cmds.text('spJobVtxParent_JellyBean', q=1, ex=1):
                cmds.deleteUI('spJobVtxParent_JellyBean', ctl=1)
            mel.eval('source "dagMenuProc.mel"')
            if cmds.window('WeightTool_JellyBean', q=1, ex=1):
                cmds.iconTextCheckBox('refresh_JellyBean', e=1, v=0)
        else:
            self.spJobStart()
            cmds.iconTextCheckBox('refresh_JellyBean', e=1, v=1)
            self.refreshJointList(0)

    def refreshJointList(self, refresh, search=''):
        seltyp = 0 if cmds.selectType(q=1, ocm=1, pv=1) or cmds.selectType(q=1, ocm=1, lp=1) or cmds.selectType(q=1, ocm=1, cv=1) else 1
        if seltyp:
            self.refreshBoxChange(9)
            return
        sel = cmds.ls(sl=1, fl=1)
        # ▽ copy权重后会触发刷新, 列表中的第一个可能是shape节点, 所以过滤一下mesh, 但是感觉可能会出现一些问题?
        #    点的Type也是mesh, 如果出问题可能在这.
        errorsel = cmds.ls(sl=1, typ=('transform', 'mesh'))
        if not sel or errorsel:
            return
        selobj = cmds.ls(sl=1, o=1)[0]
        clusterName = mel.eval('findRelatedSkinCluster("%s")' % selobj)
        if not clusterName:
            self.refreshBoxChange(9)
            return
        self.tempcluster = clusterName
        jointList = cmds.skinCluster(selobj, q=1, inf=1)  # cmds.skinCluster(selobj, q=1, wi=1)
        siItem = cmds.treeView('JointTV_JellyBean', q=1, si=1)
        _zero = cmds.menuItem('FImeunItem_JellyBean', q=1, cb=1)
        saveData = cmds.text('saveData_JellyBean', q=1, l=1).split('|')
        if refresh or _zero or saveData[0] != clusterName or saveData[1] != str(len(jointList)) or not cmds.treeView('JointTV_JellyBean', q=1, ch=''):
            cmds.treeView('JointTV_JellyBean', e=1, ra=1)
            if search:
                text = cmds.textField('searchText_JellyBean', q=1, tx=1)
                getList = [i for i in jointList if text in i]
                if getList:
                    jointList = getList
            jointList.sort()
            _jointList = []
            _valueList = []
            for i in jointList:
                Value = '%.3f' % cmds.skinPercent(clusterName, sel[0], ib=.000000001, q=1, t=i)
                if _zero:
                    if float(Value):
                        _jointList.append(i)
                        _valueList.append(Value)
                else:
                    _jointList.append(i)
                    _valueList.append(Value)
            for j, v in zip(_jointList, _valueList):
                if cmds.menuItem('HImeunItem_JellyBean', q=1, rb=1):
                    self.addHItoList(j, _jointList)
                else:
                    cmds.treeView('JointTV_JellyBean', e=1, ai=[j, ''])
                if cmds.getAttr(j + '.liw'):
                    cmds.treeView('JointTV_JellyBean', e=1, i=(j, 1, 'Lock_ON.png'))
                else:
                    cmds.treeView('JointTV_JellyBean', e=1, i=(j, 1, 'Lock_OFF_grey.png'))
                if not cmds.treeView('JointTV_JellyBean', q=1, dls=1):
                    cmds.treeView('JointTV_JellyBean', e=1, dls=(j, ''))
                if float(v):
                    cmds.treeView('JointTV_JellyBean', e=1, dls=(j, '   |   %s' % v))
            if siItem:
                allItem = cmds.treeView('JointTV_JellyBean', q=1, ch='')
                _Temp_ = list(set(siItem).intersection(set(allItem)))  # 求并集
                for i in _Temp_:
                    cmds.treeView('JointTV_JellyBean', e=1, si=(i, 1))
        else:
            allItem = cmds.treeView('JointTV_JellyBean', q=1, ch='')
            for j in allItem:
                if cmds.getAttr(j + '.liw'):
                    cmds.treeView('JointTV_JellyBean', e=1, i=(j, 1, 'Lock_ON.png'))
                else:
                    cmds.treeView('JointTV_JellyBean', e=1, i=(j, 1, 'Lock_OFF_grey.png'))
                Value = '%.3f' % cmds.skinPercent(clusterName, sel[0], ib=.000000001, q=1, t=j)
                if not cmds.treeView('JointTV_JellyBean', q=1, dls=1):
                    cmds.treeView('JointTV_JellyBean', e=1, dls=(j, ''))
                if not float(Value):
                    continue
                cmds.treeView('JointTV_JellyBean', e=1, dls=(j, '   |   %s' % Value))
        cmds.text('saveData_JellyBean', e=1, l='%s|%s' % (clusterName, len(jointList)))

    def addHItoList(self, i, jointList):
        jointP = cmds.listRelatives(i, p=1)
        if not jointP:
            if not cmds.treeView('JointTV_JellyBean', q=1, iex=i):
                cmds.treeView('JointTV_JellyBean', e=1, ai=[i, ''])
        elif cmds.treeView('JointTV_JellyBean', q=1, iex=jointP[0]):
            if not cmds.treeView('JointTV_JellyBean', q=1, iex=i):
                cmds.treeView('JointTV_JellyBean', e=1, ai=[i, jointP[0]])
        elif jointP[0] in jointList:
            self.addHItoList(jointP[0], jointList)
            if not cmds.treeView('JointTV_JellyBean', q=1, iex=i):
                cmds.treeView('JointTV_JellyBean', e=1, ai=[i, jointP[0]])
        else:
            if not cmds.treeView('JointTV_JellyBean', q=1, iex=i):
                cmds.treeView('JointTV_JellyBean', e=1, ai=[i, ''])

    def lock_unLock(self, jnt, but):
        slItem = cmds.treeView('JointTV_JellyBean', q=1, si=1)
        if not slItem or len(slItem) == 1:
            slItem = [jnt]
        if cmds.getAttr(jnt + '.liw'):
            for i in slItem:
                cmds.setAttr(i + '.liw', 0)
                cmds.treeView('JointTV_JellyBean', e=1, i=(i, 1, 'Lock_OFF_grey.png'))
        else:
            for i in slItem:
                cmds.setAttr(i + '.liw', 1)
                cmds.treeView('JointTV_JellyBean', e=1, i=(i, 1, 'Lock_ON.png'))

    def reSelect(self):
        allItem = cmds.treeView('JointTV_JellyBean', q=1, iv=1)
        slItem = cmds.treeView('JointTV_JellyBean', q=1, si=1)
        if not allItem or not slItem:
            return
        cmds.treeView('JointTV_JellyBean', e=1, cs=1)
        _Temp_ = list(set(allItem).difference(set(slItem)))  # 求差集 a有b没有
        for i in _Temp_:
            cmds.treeView('JointTV_JellyBean', e=1, si=(i, 1))

    def editVtxWeight(self, mode):
        sel = cmds.ls(sl=1, fl=1)
        if not sel:
            return
        selVtx = cmds.filterExpand(sel, sm=[28, 31, 36, 40, 46])
        if not selVtx:
            return
        selobj = cmds.ls(sl=1, o=1)[0]
        clusterName = mel.eval('findRelatedSkinCluster("%s")' % selobj)
        if not clusterName:
            return
        sljntList = cmds.treeView('JointTV_JellyBean', q=1, si=1)
        if not sljntList:
            om.MGlobal.displayError('Not Selected Joint')
            return
        if mode == '+' or mode == '-':
            for v in selVtx:
                tvList = []
                for j in sljntList:
                    Value = cmds.skinPercent(clusterName, v, ib=.000000001, q=1, t=j)
                    Value = Value + cmds.floatField('ASFloat_JellyBean', q=1, v=1)   \
                        if mode == '+' else Value - cmds.floatField('ASFloat_JellyBean', q=1, v=1)
                    tvList.append((j, Value))
                cmds.skinPercent(clusterName, v, tv=tvList)
        elif mode == '*' or mode == '/':
            for v in selVtx:
                tvList = []
                for j in sljntList:
                    Value = cmds.skinPercent(clusterName, v, ib=.000000001, q=1, t=j)
                    Value = Value * cmds.floatField('MDFloat_JellyBean', q=1, v=1)   \
                        if mode == '*' else Value / cmds.floatField('MDFloat_JellyBean', q=1, v=1)
                    tvList.append((j, Value))
                cmds.skinPercent(clusterName, v, tv=tvList)
        else:
            for v in selVtx:
                tvList = [(j, float(mode)) for j in sljntList]
                cmds.skinPercent(clusterName, v, tv=tvList)
        siItem = cmds.treeView('JointTV_JellyBean', q=1, si=1)
        self.refreshJointList(0)
        for i in siItem:
            cmds.treeView('JointTV_JellyBean', e=1, si=(i, 1))

    def slVtx(self):
        slJnt = cmds.treeView('JointTV_JellyBean', q=1, si=1)
        vtxList = []
        for i in slJnt:
            cmds.skinCluster(self.tempcluster, e=1, siv=i)
            vtxList.append(cmds.filterExpand(cmds.ls(sl=1, fl=1), sm=[28, 31, 36, 40, 46]))
        cmds.select(vtxList, r=1)

    def _weightView(self):
        if cmds.iconTextCheckBox('refresh_JellyBean', q=1, v=1):
            if cmds.currentCtx() == 'artAttrSkinContext':
                mel.eval('setSmoothSkinInfluence "%s";' % cmds.treeView('JointTV_JellyBean', q=1, si=1)[0])
            self._weightfloat()

    def _weightfloat(self):
        treesl = cmds.treeView('JointTV_JellyBean', q=1, si=1)
        sel = cmds.ls(sl=1, fl=1)
        if not treesl or not sel:
            return
        selobj = cmds.ls(sl=1, o=1)[0]
        clusterName = mel.eval('findRelatedSkinCluster("%s")' % selobj)
        cmds.floatField('weighrfloat_JellyBean', e=1, v=float('%.4f' % cmds.skinPercent(clusterName, sel[0], ib=.000000001, q=1, t=treesl[0])))

    # # # # # # # # # #
    def copyVtxWeight(self):
        selVtx = cmds.filterExpand(cmds.ls(sl=1)[0], sm=[28, 31, 36, 40, 46])
        if not selVtx:
            om.MGlobal.displayError('Not Selected Vtx')
            return
        selobj = cmds.ls(sl=1, o=1)[0]
        clusterName = mel.eval('findRelatedSkinCluster("%s")' % selobj)
        if not clusterName:
            om.MGlobal.displayError('Select No Skin')
            return
        mel.eval('artAttrSkinWeightCopy;')
        ValueList = cmds.skinPercent(clusterName, selVtx, q=1, ib=.000000001, v=1)
        TransList = cmds.skinPercent(clusterName, selVtx, q=1, ib=.000000001, t=None)
        '''   #倒序循环
        for i in range(len(ValueList)-1, -1, -1):
            if ValueList[i] < .0001:
                del ValueList[i], TransList[i]
        '''
        self.vtxWeightInfo = [clusterName, TransList, ValueList]
        # print(self.vtxWeightInfo)

    def pasteVtxWeight(self):
        selVtx = cmds.filterExpand(cmds.ls(sl=1, fl=1), sm=[28, 31, 36, 40, 46])
        if not selVtx:
            om.MGlobal.displayError('Not Selected Vtx')
            return
        selObj = cmds.ls(sl=1, o=1)[0]
        clusterName = mel.eval('findRelatedSkinCluster("%s")' % selObj)
        if not clusterName:
            om.MGlobal.displayError('Select No Skin')
            return
        if clusterName != self.vtxWeightInfo[0]:
            jointList = cmds.skinCluster(selObj, q=1, inf=1)
            for j in self.vtxWeightInfo[1]:
                if not j in jointList:
                    om.MGlobal.displayError('Joint are different !!!')
                    return
        tvList = [(self.vtxWeightInfo[1][i], self.vtxWeightInfo[2][i]) for i in range(len(self.vtxWeightInfo[1]))]
        # print(tvList)
        for i in selVtx:
            exec('cmds.skinPercent("%s", "%s", nrm=0, zri=1, tv=%s)' % (clusterName, i, tvList))
        self.refreshJointList(0)
    # # # # # # # # # #

    # # # # # Tool # # # # #
    def vtxSave_Mel(self):
        sel = cmds.ls(sl=1, fl=1)
        if not sel:
            om.MGlobal.displayError('Select Nothing')
            return
        selobj = cmds.ls(sl=1, o=1)[0]
        selVtx = cmds.filterExpand(sel, sm=[28, 31, 36, 40, 46])
        if not selVtx:
            seltyp = cmds.objectType(cmds.listRelatives(selobj, s=1, f=1)[0])
            if seltyp == 'mesh':
                suf = '.vtx'
            elif seltyp == 'nurbsCurve' or seltyp == 'nurbsSurface':
                suf = '.cv'
            elif seltyp == 'subdiv':
                suf = '.smp'
            elif seltyp == 'lattice':
                suf = '.pt'
            selVtx = cmds.ls('%s%s[*]' % (selobj, suf), fl=1)
        clusterName = mel.eval('findRelatedSkinCluster("%s")' % selobj)
        if not clusterName:
            om.MGlobal.displayError('Select No Skin')
            return
        filePath = cmds.fileDialog2(ff='WeightFile (*.vtxWeight *.sdd)', ds=2)  # vtxWeight (*.vtxWeight);;sdd (*.sdd)
        if not filePath:
            return
        with open(filePath[0], 'w') as vwfile:
            #gMainProgressBar = mel.eval('$tmp = $gMainProgressBar')
            #cmds.progressBar(gMainProgressBar, e=1, bp=1, ii=1, st='Save ...', max=len(selVtx))
            for i in selVtx:
                #cmds.progressBar(gMainProgressBar, e=1, s=1)
                valueList = cmds.skinPercent(clusterName, i, ib=.000000001, q=1, v=1)
                transList = cmds.skinPercent(clusterName, i, ib=.000000001, q=1, t=None)
                allWeight = 0
                for w in range(len(valueList)):
                    valueList[w] = round(valueList[w], 4)
                    allWeight += valueList[w]
                valueList[-1] += (1.0 - allWeight)
                tvList = [[transList[u], valueList[u]] for u in range(len(valueList))]
                wtStr = '%s--%s\r\n' % (i.split('.')[-1], tvList)
                vwfile.write(wtStr)
            #cmds.progressBar(gMainProgressBar, e=1, ep=1)
        DisplayYes().showMessage('Process Finish!')

    def vtxLoad_Mel(self):
        sel = cmds.ls(sl=1, fl=1)
        if not sel:
            om.MGlobal.displayError('Select Nothing')
            return
        selobj = cmds.ls(sl=1, o=1)[0]
        clusterName = mel.eval('findRelatedSkinCluster("%s")' % selobj)
        if not clusterName:
            om.MGlobal.displayError('Select No Skin')
            return
        filePath = cmds.fileDialog2(ff='WeightFile (*.vtxWeight *.sdd)', ds=2, fm=1)
        if not filePath:
            return
        allLine = []
        allLineapp = allLine.append
        with open(filePath[0], 'r') as vwfile:
            line = vwfile.readline()
            while line:
                allLineapp(line)
                line = vwfile.readline()

        jntList = cmds.skinCluster(selobj, q=1, inf=1)
        jntLock = []
        for j in jntList:
            jntLock.append(cmds.getAttr(j + '.liw'))
            cmds.setAttr(j + '.liw', 0)
        #gMainProgressBar = mel.eval('$tmp = $gMainProgressBar')
        #cmds.progressBar(gMainProgressBar, e=1, bp=1, ii=1, st='Load ...', max=len(allLine))
        for i in allLine:
            #cmds.progressBar(gMainProgressBar, e=1, s=1)
            strsplit = i.split('--')
            vtx = strsplit[0].strip()
            tvList = strsplit[-1].strip()
            exec('cmds.skinPercent("%s", "%s.%s", tv=%s)' % (clusterName, selobj, vtx, tvList))
        #cmds.progressBar(gMainProgressBar, e=1, ep=1)
        for j, l in zip(jntList, jntLock):
            cmds.setAttr(j + '.liw', l)
        DisplayYes().showMessage('Process Finish!')

    def vtxSave_Oapi(self):
        selList = Om.MSelectionList()
        Om.MGlobal.getActiveSelectionList(selList)
        #_prselList = []
        # selList.getSelectionStrings(_prselList)   #获取 MSelectionList 内容
        # print _prselList
        if selList.isEmpty():
            Om.MGlobal.displayError('Select Nothing')
            return
        MDagPath = Om.MDagPath()  # 存储所选物体的路径
        MObject = Om.MObject()  # 存储所选物体的组件的列表
        selList.getDagPath(0, MDagPath)
        selList.getDependNode(0, MObject)
        # MDagPath.fullPathName()   #获取 MDagPath 内容
        slMIt = Om.MItSelectionList(selList)
        MItDagPath = Om.MDagPath()
        MItcomponent = Om.MObject()
        slMIt.getDagPath(MItDagPath, MItcomponent)

        _selType = MDagPath.apiType()
        MDagPath.extendToShape()  # 获取当前物体的shape节点
        _selShapeType = MDagPath.apiType()
        if not _selType in set([110, 296, 267, 294, 279, ]):
            return
        elif _selShapeType == 296:
            suf = 'vtx'
        elif _selShapeType == 267 or _selShapeType == 294:
            suf = 'cv'
        elif _selShapeType == 279:
            suf = 'pt'

        skCluster = mel.eval('findRelatedSkinCluster("%s")' % MDagPath.partialPathName())
        if not skCluster:
            return
        #connectNode = cmds.listHistory(MDagPath.partialPathName(), il=1, pdo=1)
        # if not connectNode:
        #    Om.MGlobal.displayError('Select No Skin')
        #    return
        # for skCluster in connectNode:
        #    if cmds.nodeType(skCluster) == 'skinCluster':
        #        break
        #    if skCluster == connectNode[-1]:
        #        return
        Om.MGlobal.getSelectionListByName(skCluster, selList)
        skinObj = Om.MObject()
        selList.getDependNode(1, skinObj)
        skinNode = OmAni.MFnSkinCluster(skinObj)
        infs = Om.MDagPathArray()
        numInfs = skinNode.influenceObjects(infs)
        infNameList = []  # 骨骼列表
        for i in range(numInfs):
            infName = infs[i].partialPathName()
            infNameList.append(infName)
        # fn = Om.MFnDependencyNode(MDagPath.node())   #获取MDagPath的内容?
        # print fn.name()   #获取 MFnDependencyNode 内容

        filePath = cmds.fileDialog2(ff='WeightFile (*.vtxWeight *.sdd)', ds=2)  # vtxWeight (*.vtxWeight);;sdd (*.sdd)
        if not filePath:
            return
        fileLine = []
        Lineapp = fileLine.append
        if not MItcomponent.isNull():  # component组件不为空(点), 线和面会强制转为点
            vertIter = Om.MItGeometry(MItDagPath, MItcomponent)
        else:
            vertIter = Om.MItGeometry(MObject)
        while not vertIter.isDone():
            infCount = Om.MScriptUtil()
            infCountPtr = infCount.asUintPtr()
            Om.MScriptUtil.setUint(infCountPtr, 0)
            weights = Om.MDoubleArray()
            skinNode.getWeights(MDagPath, vertIter.currentItem(), weights, infCountPtr)

            tvList = self.zeroWeightData_Save(weights, infNameList)
            wtStr = '%s[%s]--%s\r\n' % (suf, vertIter.index(), tvList)
            Lineapp(wtStr)
            vertIter.next()
        with open(filePath[0], 'w') as vwfile:
            for i in fileLine:
                vwfile.write(i)
        DisplayYes().showMessage('Process Finish!')

    def vtxLoad_Oapi(self):
        selList = Om.MSelectionList()
        Om.MGlobal.getActiveSelectionList(selList)
        if selList.isEmpty():
            Om.MGlobal.displayError('Select Nothing')
            return
        elif selList.length() != 1:
            Om.MGlobal.displayError("Nothing selected")
        MDagPath = Om.MDagPath()  # 存储所选物体的路径
        MObject = Om.MObject()  # 存储所选物体的组件的列表
        selList.getDagPath(0, MDagPath)
        selList.getDependNode(0, MObject)
        # MDagPath.fullPathName()   #获取 MDagPath 内容

        _selType = MDagPath.apiType()
        if _selType != 110:
            Om.MGlobal.displayError('Please Select Object')
            return

        skCluster = mel.eval('findRelatedSkinCluster("%s")' % MDagPath.partialPathName())
        if not skCluster:
            return
        Om.MGlobal.getSelectionListByName(skCluster, selList)
        skinObj = Om.MObject()
        selList.getDependNode(1, skinObj)
        skinNode = OmAni.MFnSkinCluster(skinObj)
        infs = Om.MDagPathArray()
        numInfs = skinNode.influenceObjects(infs)
        infNameList = []  # 骨骼列表
        for i in range(numInfs):
            infName = infs[i].partialPathName()
            infNameList.append(infName)
        # fn = Om.MFnDependencyNode(MDagPath.node())   #获取MDagPath的内容?
        # print fn.name()   #获取 MFnDependencyNode 内容

        filePath = cmds.fileDialog2(ff='WeightFile (*.vtxWeight *.sdd)', ds=2, fm=1)
        if not filePath:
            return
        allLine = self.readWeightData_Load(filePath[0])
        if allLine == 'toMel':
            Om.MGlobal.displayWarning('Some Error. Please ReSelect')
            self.vtxLoad_Mel()
            return

        jntLock = []
        for j in infNameList:
            jntLock.append(cmds.getAttr(j + '.liw'))
            cmds.setAttr(j + '.liw', 0)
        vertIter = Om.MItGeometry(MObject)
        _Num = 0
        while not vertIter.isDone():
            if vertIter.index() != int(allLine[_Num][0]):
                vertIter.next()
                continue
            jntindex = Om.MIntArray()
            weights = Om.MDoubleArray()
            jntindexapp = jntindex.append
            weightsapp = weights.append
            for i in range(len(allLine[_Num][1])):
                jntindexapp(infNameList.index(allLine[_Num][1][i]))
                weightsapp(allLine[_Num][2][i])
            skinNode.setWeights(MDagPath, vertIter.currentItem(), jntindex, weights, False)  # False规格化开关默认为True
            _Num += 1
            vertIter.next()
        for j, l in zip(infNameList, jntLock):
            cmds.setAttr(j + '.liw', l)
        DisplayYes().showMessage('Process Finish!')

    def vtxSave_api(self):
        selList = om.MGlobal.getActiveSelectionList()
        if selList.isEmpty():
            om.MGlobal.displayError('Select Nothing')
            return
        MDagPath = selList.getDagPath(0)  # 存储所选物体的路径
        MObject = selList.getDependNode(0)  # 存储所选物体的组件的列表
        slMIt = om.MItSelectionList(selList)
        MItDagPath, MItcomponent = slMIt.getComponent()

        _selType = MDagPath.apiType()
        _selShapeType = MDagPath.extendToShape().apiType()
        if not _selType in set([110, 296, 267, 294, 279, ]):
            return
        elif _selShapeType == 296:
            suf = 'vtx'
        elif _selShapeType == 267 or _selShapeType == 294 or _selShapeType == 279:
            self.vtxSave_Oapi()
            return

        skCluster = mel.eval('findRelatedSkinCluster("%s")' % MDagPath.partialPathName())
        if not skCluster:
            return
        selList.add(skCluster)
        skinObj = selList.getDependNode(1)
        skinNode = omAni.MFnSkinCluster(skinObj)
        infs = skinNode.influenceObjects()
        infNameList = [infs[i].partialPathName() for i in range(len(infs))]  # 骨骼列表

        filePath = cmds.fileDialog2(ff='WeightFile (*.vtxWeight *.sdd)', ds=2)
        if not filePath:
            return
        fileLine = []
        Lineapp = fileLine.append
        if not MItcomponent.isNull():  # component组件不为空（点）,线和面会强制转为点
            vertIter = om.MItMeshVertex(MItDagPath, MItcomponent)
        else:
            vertIter = om.MItMeshVertex(MObject)
        while not vertIter.isDone():
            weights = skinNode.getWeights(MDagPath, vertIter.currentItem())[0]

            tvList = self.zeroWeightData_Save(weights, infNameList)
            wtStr = '%s[%s]--%s\r\n' % (suf, vertIter.index(), tvList)
            Lineapp(wtStr)
            vertIter.next()
        with open(filePath[0], 'w') as vwfile:
            for i in fileLine:
                vwfile.write(i)
        DisplayYes().showMessage('Process Finish!')

    def vtxLoad_api(self):
        selList = om.MGlobal.getActiveSelectionList()
        if selList.isEmpty():
            om.MGlobal.displayError('Select Nothing')
            return
        MDagPath = selList.getDagPath(0)  # 存储所选物体的路径
        MObject = selList.getDependNode(0)  # 存储所选物体的组件的列表

        _selType = MDagPath.apiType()
        _selShapeType = MDagPath.extendToShape().apiType()
        if _selType != 110:
            om.MGlobal.displayError('Please Select Object')
            return
        if _selShapeType != 296:
            self.vtxLoad_Oapi()
            return

        skCluster = mel.eval('findRelatedSkinCluster("%s")' % MDagPath.partialPathName())
        if not skCluster:
            return
        selList.add(skCluster)
        skinObj = selList.getDependNode(1)
        skinNode = omAni.MFnSkinCluster(skinObj)
        infs = skinNode.influenceObjects()
        infNameList = [infs[i].partialPathName() for i in range(len(infs))]  # 骨骼列表

        filePath = cmds.fileDialog2(ff='WeightFile (*.vtxWeight *.sdd)', ds=2, fm=1)
        if not filePath:
            return
        allLine = self.readWeightData_Load(filePath[0])
        if allLine == 'toMel':
            om.MGlobal.displayWarning('Some Error. Please ReSelect')
            self.vtxLoad_Mel()
            return

        jntLock = []
        for j in infNameList:
            jntLock.append(cmds.getAttr(j + '.liw'))
            cmds.setAttr(j + '.liw', 0)
        vertIter = om.MItMeshVertex(MObject)
        _Num = 0
        while not vertIter.isDone():
            if vertIter.index() != int(allLine[_Num][0]):
                vertIter.next()
                continue
            jntindex = om.MIntArray()
            weights = om.MDoubleArray()
            jntindexapp = jntindex.append
            weightsapp = weights.append
            for i in range(len(allLine[_Num][1])):
                jntindexapp(infNameList.index(allLine[_Num][1][i]))
                weightsapp(allLine[_Num][2][i])
            skinNode.setWeights(MDagPath, vertIter.currentItem(), jntindex, weights, False)  # False规格化开关默认为True
            _Num += 1
            vertIter.next()
        for j, l in zip(infNameList, jntLock):
            cmds.setAttr(j + '.liw', l)
        DisplayYes().showMessage('Process Finish!')

    def zeroWeightData_Save(self, weights, infNameList, source=0):
        #去除0权重数据, source为1则输出源数据
        if source:
            return [[infNameList[it], weights[it]] for it in range(len(weights))]
        allWeight = 0
        transList = []
        valueList = []
        _jLappend = transList.append
        _wLappend = valueList.append
        for i in range(len(weights)):
            _tempweight = round(weights[i], 4)
            if _tempweight:
                _jLappend(infNameList[i])
                _wLappend(_tempweight)
            allWeight += _tempweight
        valueList[0] += (1.0 - allWeight)
        return [[transList[it], valueList[it]] for it in range(len(valueList))]

    def readWeightData_Load(self, path):
        allLine = []
        _allappend = allLine.append
        with open(path, 'r') as vwfile:
            line = vwfile.readline()
            while line:
                strsplit = line.split('--')
                if '][' in strsplit[0]:
                    return 'toMel'
                vtx = strsplit[0].split('[')[-1].split(']')[0]
                _data = strsplit[-1].strip()
                if '], [' in _data:
                    jointList = []
                    _jointListapp = jointList.append
                    weightList = []
                    _weightListapp = weightList.append
                    for i in _data[2:-2].split('], ['):
                        _str = i.split(', ')
                        _jointListapp(_str[0][2:-1])
                        _weightListapp(float(_str[1]))
                    _allappend([vtx, jointList, weightList])
                else:
                    _str = _data[2:-2].split(', ')
                    _allappend([vtx, [_str[0][2:-1]], [float(_str[1])]])
                # for item in eval(_data):
                #    jointList.append(item[0])
                #    weightList.append(item[1])
                #_allappend([vtx, jointList, weightList])
                line = vwfile.readline()
            _allappend([-1, None, None])
        return allLine

    def resetSkinPose(self):
        for obj in cmds.ls(sl=1):
            clusterName = mel.eval('findRelatedSkinCluster("%s")' % obj)
            if not clusterName:
                return
            sk_matrix = clusterName + '.matrix'
            mx_num = cmds.getAttr(sk_matrix, mi=1)
            infs = cmds.listConnections(sk_matrix, s=1, d=0, scn=1)
            if not infs:
                return
            for n in mx_num:
                inf = cmds.listConnections('%s[%d]' % (sk_matrix, n), s=1, d=0, scn=1)
                if not inf:
                    continue
                matrix = cmds.getAttr('%s.worldInverseMatrix[0]' % inf[0])
                cmds.setAttr('%s.pm[%d]' % (clusterName, n), matrix, typ='matrix')
                cmds.dagPose(inf[0], rs=1, n=cmds.listConnections('%s.bp' % clusterName, s=1, d=0, scn=1)[0])

    def createSelect(self):
        selvtx = cmds.ls(sl=1)
        selobj = cmds.ls(sl=1, o=1)[0]
        cluWs = cmds.getAttr(cmds.cluster(n='_tempClu_')[1] + 'Shape.origin')[0]
        Curname = cmds.circle(n='_selectCur_')[0]
        cmds.setAttr(Curname + '.translate', cmds.polyEvaluate(selobj, b=1)[0][1] + 1, cluWs[1], cluWs[2])
        cmds.addAttr(Curname, ln='vtxinfo', dt='string')
        cmds.setAttr(Curname + '.vtxinfo', '', type='string')
        for i in selvtx:
            cmds.setAttr(Curname + '.vtxinfo', '%s%s,' % (cmds.getAttr(Curname + '.vtxinfo'), i), type='string')
        cmds.delete('_tempClu_Handle')
        cmds.setAttr(cmds.listRelatives(Curname, c=1, s=1)[0] + '.overrideEnabled', 1)
        cmds.setAttr(cmds.listRelatives(Curname, c=1, s=1)[0] + '.overrideColor', 16)

    def getSelect(self):
        _tempVtx = []
        for c in cmds.ls(sl=1):
            if not cmds.ls('%s.vtxinfo' % c):
                return
            vtxList = cmds.getAttr('%s.vtxinfo' % c).split(',')[0:-1]
            for i in vtxList:
                _tempVtx.append(i)
        cmds.select(_tempVtx, r=1)
    # # # # # Tool # # # # #


class DisplayYes():  # 报绿

    def __init__(self):
        self.gCommandLine = mel.eval('$tmp = $gCommandLine')

    def showMessage(self, message):
        widget = shiboken2.wrapInstance(long(OmUI.MQtUtil.findControl(self.gCommandLine)), QtWidgets.QWidget)
        widget.findChild(QtWidgets.QLineEdit).setStyleSheet('background-color:rgb(10,200,15);' + 'color:black;')
        cmds.select('time1', r=1)
        WeightTool_JellyBean().refreshBoxChange(9)
        cmds.text('spJobReLine_DisplayYes', p='FiristcL_JellyBean', vis=0)   # p = Layout
        cmds.scriptJob(e=['SelectionChanged', 'DisplayYes().resetLine()'], p='spJobReLine_DisplayYes')
        Om.MGlobal.displayInfo(message)

    def resetLine(self):
        cmds.deleteUI('spJobReLine_DisplayYes', ctl=1)
        cmds.deleteUI(self.gCommandLine.rsplit('|', 1)[0])
        mel.eval('source "initCommandLine.mel"')


class WeightCheckTool_JellyBean():

    def ToolUi(self):
        ToolUi = 'WeightCheckTool_JellyBean'
        if cmds.window(ToolUi, q=1, ex=1):
            cmds.deleteUI(ToolUi)
        cmds.window(ToolUi, t='WeightCheckTool', rtf=1, mb=1, wh=(500, 300))
        cmds.formLayout('MainformLayout_JellyBean')
        cmds.paneLayout('ListLayout_JellyBean', cn='vertical3', ps=(1, 1, 1))
        cmds.textScrollList('vtxList_JellyBean', ams=1, sc=lambda *args:
                            cmds.textScrollList('weightList_JellyBean', e=1, da=1, sii=cmds.textScrollList('vtxList_JellyBean', q=1, sii=1)))
        cmds.popupMenu()
        cmds.menuItem('SNmenuItem_JellyBean', l='View Object Name', cb=0, c=lambda *args: self.Load())
        cmds.textScrollList('weightList_JellyBean', ams=1, sc=lambda *args:
                            cmds.textScrollList('vtxList_JellyBean', e=1, da=1, sii=cmds.textScrollList('weightList_JellyBean', q=1, sii=1)))
        cmds.setParent('..')
        cmds.columnLayout('cLayout_JellyBean', cat=('right', 5), cw=100)
        cmds.text(l='', h=3)
        cmds.button(l='Load', w=80, h=26, c=lambda *args: self.Load())
        cmds.button(l='Clean', w=80, h=26, c=lambda *args: self.Clean())
        cmds.button(l='Remove Min', w=80, h=26, c=lambda *args: self.RemoveMin())
        cmds.popupMenu()
        cmds.menuItem(l='Remove as Value', c=lambda *args: self.RemoveValue())
        cmds.button(l='Select', w=80, h=26, c=lambda *args: self.selectVtx())
        cmds.text(l='Decimal', h=20)
        cmds.intField('DecimalInt_JellyBean', v=3)
        cmds.text(l='Influence', h=20)
        cmds.intField('InfluenceInt_JellyBean', v=3)
        cmds.text('ViewNum_JellyBean', vis=0, h=20)
        cmds.text('shapeInfo_JellyBean', vis=0)

        cmds.formLayout('MainformLayout_JellyBean', e=1, af=[('ListLayout_JellyBean', 'top', 0), ('ListLayout_JellyBean', 'bottom', 0),
                                                             ('ListLayout_JellyBean', 'left', 3), ('cLayout_JellyBean', 'right', 3)])
        cmds.formLayout('MainformLayout_JellyBean', e=1, ac=('ListLayout_JellyBean', 'right', 3, 'cLayout_JellyBean'))
        cmds.showWindow(ToolUi)

    def getSel(self):
        sel = cmds.ls(sl=1, fl=1)
        if not sel:
            om.MGlobal.displayError('Select Nothing')
            return None, None
        selVtx = cmds.filterExpand(sel, sm=[28, 31, 36, 40, 46])
        selobj = cmds.ls(sl=1, o=1)[0]
        self.saveShape = selobj
        if not selVtx:
            if not selobj:
                return None, None
            seltyp = cmds.objectType(cmds.listRelatives(selobj, s=1, f=1)[0])
            if seltyp == 'mesh':
                suf = '.vtx'
            elif seltyp == 'nurbsCurve' or seltyp == 'nurbsSurface':
                suf = '.cv'
            elif seltyp == 'subdiv':
                suf = '.smp'
            elif seltyp == 'lattice':
                suf = '.pt'
            selVtx = cmds.ls('%s%s[*]' % (selobj, suf), fl=1)
        clusterName = mel.eval('findRelatedSkinCluster("%s")' % selobj)
        if not clusterName:
            om.MGlobal.displayError('Select No Skin')
            return None, None
        return selVtx, clusterName

    def Load(self):
        cmds.text('ViewNum_JellyBean', e=1, vis=0)
        selVtx, clusterName = self.getSel()
        if not selVtx or not clusterName:
            return
        cmds.textScrollList('vtxList_JellyBean', e=1, ra=1)
        cmds.textScrollList('weightList_JellyBean', e=1, ra=1)
        self.Number = []
        for i in selVtx:
            valueList = cmds.skinPercent(clusterName, i, ib=.000000001, q=1, v=1)
            transList = cmds.skinPercent(clusterName, i, ib=.000000001, q=1, t=None)
            tvStr = ''
            if len(valueList) > cmds.intField('InfluenceInt_JellyBean', q=1, v=1):
                self.Number.append(i)
            for w, j in zip(valueList, transList):
                Value = str(w).rstrip('0').rstrip('.')
                tvStr += '%s ~ %s @ ' % (j, Value)
            if not cmds.menuItem('SNmenuItem_JellyBean', q=1, cb=1):
                i = i.split('.')[1]
            cmds.textScrollList('vtxList_JellyBean', e=1, a=i)
            cmds.textScrollList('weightList_JellyBean', e=1, a=tvStr)
        if self.Number:
            cmds.text('ViewNum_JellyBean', e=1, vis=1, l='Number: %s' % len(self.Number))
            if not cmds.menuItem('SNmenuItem_JellyBean', q=1, cb=1):
                _tempSl = [i.split('.')[1] for i in self.Number]
                cmds.textScrollList('vtxList_JellyBean', e=1, si=_tempSl)
            else:
                cmds.textScrollList('vtxList_JellyBean', e=1, si=self.Number)
            cmds.textScrollList('weightList_JellyBean', e=1, sii=cmds.textScrollList('vtxList_JellyBean', q=1, sii=1))
        cmds.text('shapeInfo_JellyBean', e=1, l=self.saveShape)

    def selectVtx(self):
        vtxList = cmds.textScrollList('vtxList_JellyBean', q=1, si=1)
        if not vtxList:
            cmds.select(cmds.polyListComponentConversion(self.saveShape, ff=1, fe=1, fuv=1, fvf=1, tv=1), r=1)
            cmds.hilite(self.saveShape)
            return
        if not '.' in vtxList[0]:
            _shapeN = cmds.text('shapeInfo_JellyBean', q=1, l=1)
            vtxList = ['%s.%s' % (_shapeN, i) for i in vtxList]
        else:
            _shapeN = cmds.ls(vtxList[0], o=1)
        cmds.hilite(_shapeN)
        cmds.select(vtxList, r=1)

    def Clean(self):
        selVtx, clusterName = self.getSel()
        if not selVtx or not clusterName:
            return
        jntList = cmds.skinCluster(cmds.ls(selVtx[0], o=1)[0], q=1, inf=1)
        jntLock = []
        for j in jntList:
            jntLock.append(cmds.getAttr(j + '.liw'))
            cmds.setAttr(j + '.liw', 0)
        decimal.getcontext().rounding = 'ROUND_HALF_UP'
        _decimal = '%.'+ str(cmds.intField('DecimalInt_JellyBean', q=1, v=1)) +'f'
        for i in selVtx:
            transList = cmds.skinPercent(clusterName, i, ib=.000000001, q=1, t=None)
            _tv = []
            for j in transList:
                # mel.eval('global proc float _rounding(float $f, int $n){float $N = pow(10, ($n));float $a = $f%(1/$N)*$N;float $B;     \
                #            if($a>0.5)$B = ceil($f*$N)/$N;else$B = floor($f*$N/$N);return $B;}')     #精度问题?
                #Value = mel.eval('_rounding(%s, %s)' %(cmds.skinPercent(clusterName, i, ib=.000000001, q=1, t=j), cmds.intField('DecimalInt', q=1, v=1)))
                Value = float(str(decimal.Decimal(str(cmds.skinPercent(clusterName, i, ib=.000000001, q=1, t=j))).
                                  quantize(decimal.Decimal(_decimal % 1))).rstrip('0').rstrip('.'))
                # if Value == 0:
                #    continue
                _tv.append([j, Value])
            num = 0
            for n in _tv:
                num += n[1]
            _tv[-1][1] = float(str(decimal.Decimal(str(_tv[-1][1] + 1 - num)).quantize(decimal.Decimal(_decimal % 1))).rstrip('0').rstrip('.'))
            cmds.skinPercent(clusterName, i, tv=_tv)
        for j, l in zip(jntList, jntLock):
            cmds.setAttr(j + '.liw', l)
        self.Load()

    def RemoveMin(self):
        selVtx, clusterName = self.getSel()
        if not selVtx or not clusterName:
            return
        jntList = cmds.skinCluster(cmds.ls(selVtx[0], o=1)[0], q=1, inf=1)
        jntLock = []
        for j in jntList:
            jntLock.append(cmds.getAttr(j + '.liw'))
            cmds.setAttr(j + '.liw', 0)
        Influence = cmds.intField('InfluenceInt_JellyBean', q=1, v=1)
        for v in selVtx:
            transList = cmds.skinPercent(clusterName, v, ib=.000000001, q=1, t=None)
            while len(transList) > Influence:
                valueList = cmds.skinPercent(clusterName, v, ib=.000000001, q=1, v=1)
                tvdic = {}
                for w, j in zip(valueList, transList):
                    tvdic[j] = w
                tvList = sorted(tvdic.items(), key=lambda item: item[1])
                cmds.skinPercent(clusterName, v, tv=(tvList[0][0], 0))
                transList = cmds.skinPercent(clusterName, v, ib=.000000001, q=1, t=None)
        for j, l in zip(transList, jntLock):
            cmds.setAttr(j + '.liw', l)
        self.Load()

    def RemoveValue(self):
        if cmds.promptDialog(t='RemoveValue', m='Value', tx='0.001', b=['OK', 'Cancel'], db='OK', cb='Cancel', ds='Cancel') == 'OK':
            reValue = float(cmds.promptDialog(q=1, tx=1))
            selVtx, clusterName = self.getSel()
            if not selVtx or not clusterName:
                return
            jntList = cmds.skinCluster(cmds.ls(selVtx[0], o=1)[0], q=1, inf=1)
            jntLock = []
            for j in jntList:
                jntLock.append(cmds.getAttr(j + '.liw'))
                cmds.setAttr(j + '.liw', 0)
            for i in selVtx:
                valueList = cmds.skinPercent(clusterName, i, ib=.000000001, q=1, v=1)
                transList = cmds.skinPercent(clusterName, i, ib=.000000001, q=1, t=None)
                reTvList = [(j, 0) for w, j in zip(valueList, transList) if w <= reValue]
                cmds.skinPercent(clusterName, i, tv=reTvList)
            for j, l in zip(jntList, jntLock):
                cmds.setAttr(j + '.liw', l)
            self.Load()


WeightTool_JellyBean().ToolUi()
#WeightCheckTool_JellyBean().ToolUi()
