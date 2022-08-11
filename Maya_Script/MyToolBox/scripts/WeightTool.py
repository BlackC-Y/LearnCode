# -*- coding: UTF-8 -*-
'''Roadmap:
'''
from maya import cmds, mel
from maya import OpenMaya as Om, OpenMayaAnim as OmAni
from maya.api import OpenMaya as om, OpenMayaAnim as omAni
import decimal
import time
from .DisplayYes import *

class WeightTool_BbBB():

    def ToolUi(self):
        Ver = '1.01'
        self.ToolUi = 'WeightTool_BbBB'
        if cmds.window(self.ToolUi, q=1, ex=1):
            cmds.deleteUI(self.ToolUi)
        cmds.window(self.ToolUi, t='WeightTool %s' %Ver, rtf=1, mb=1, tlb=1, wh=(230, 500))
        cmds.menu(l='SkinT', to=1)
        cmds.menuItem(d=1, dl="S/L")
        cmds.menuItem(l='Save', c=lambda *args: WeightSL_BbBB().SLcheck('Save'))
        cmds.menuItem(l='Load', c=lambda *args: WeightSL_BbBB().SLcheck('Load'))
        cmds.menuItem(d=1)
        cmds.menuItem(l='WeightCheck', c=lambda *args: WeightCheckTool_BbBB().ToolUi())
        cmds.menuItem(l='reset SkinPose', c=lambda *args: self.resetSkinPose())
        cmds.menu(l='RigT', to=1)
        cmds.menuItem(l='Create', c=lambda *args: self.createSelect())
        cmds.menuItem(l='Get', c=lambda *args: self.getSelect())
        cmds.columnLayout('FiristcL_BbBB', cat=('both', 2), rs=2, cw=220, adj=1)
        cmds.text('spJobchangeVtx_BbBB', p='FiristcL_BbBB', vis=0)
        cmds.scriptJob(e=['SelectTypeChanged', 'WeightTool_BbBB().refreshBoxChange(None)'], p='spJobchangeVtx_BbBB')
        cmds.rowLayout(nc=6, adj=2)
        cmds.iconTextCheckBox('refresh_BbBB', i='refresh.png', w=20, h=20,
                              onc=lambda *args: self.spJobStart(), ofc=lambda *args: self.refreshBoxChange(9))
        cmds.popupMenu()
        cmds.menuItem('OFFmeunItem_BbBB', l='OFF', cb=0)
        cmds.textField('searchText_BbBB', h=22, tcc=lambda *args: self.refreshJointList(1, cmds.textField('searchText_BbBB', q=1, tx=1)))
        # cmds.iconTextButton(i='expandInfluenceList.png', w=20, h=20,
        #    c=lambda *args: cmds.treeView('JointTV_BbBB', e=1, h=cmds.treeView('JointTV_BbBB', q=1, h=1) + 20))
        # cmds.iconTextButton(i='retractInfluenceList.png', w=20, h=20,
        #    c=lambda *args: cmds.treeView('JointTV_BbBB', e=1, h=cmds.treeView('JointTV_BbBB', q=1, h=1) - 20))
        # invertSelection.png
        cmds.iconTextButton(i='invertSelection.png', w=20, h=20, c=self.reSelect)
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.formLayout('JointTVLayout_BbBB')
        cmds.treeView('JointTV_BbBB', nb=1, h=100, scc=self._weightView, pc=(1, self.lock_unLock))
        cmds.popupMenu()
        cmds.radioMenuItemCollection()
        cmds.menuItem('HImeunItem_BbBB', l='Hierarchy', rb=1, c=lambda *args: self.refreshJointList(1))
        cmds.menuItem('AImeunItem_BbBB', l='Alphabetically', rb=0, c=lambda *args: self.refreshJointList(1))
        cmds.menuItem('FImeunItem_BbBB', l='Filter Zero', cb=0, c=lambda *args: self.refreshJointList(1))
        cmds.text('saveData_BbBB', l='', vis=0)
        cmds.popupMenu()
        #cmds.menuItem(l='Lock All')
        #cmds.menuItem(l='Unlock All')
        cmds.menuItem(l='Select Vtx', c=lambda *args: self.slVtx())
        cmds.formLayout('JointTVLayout_BbBB', e=1, af=[('JointTV_BbBB', 'top', 0), ('JointTV_BbBB', 'bottom', 0),
                                                            ('JointTV_BbBB', 'left', 3), ('JointTV_BbBB', 'right', 3)])
        cmds.setParent('..')
        cmds.columnLayout(cat=('both', 2), rs=2, cw=225)
        cmds.rowLayout(nc=4, cw4=(50, 50, 50, 65))
        cmds.floatField('weighrfloat_BbBB', w=52, h=26, pre=4, min=0, max=1,
                        ec=lambda *args: self.editVtxWeight(cmds.floatField('weighrfloat_BbBB', q=1, v=1)))
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
        cmds.floatField('ASFloat_BbBB', v=0.05, h=26, w=50, pre=3, min=0, max=1)
        cmds.button(w=38, h=26, l='+', c=lambda *args: self.editVtxWeight('+'))
        cmds.button(w=38, h=26, l='-', c=lambda *args: self.editVtxWeight('-'))
        cmds.setParent('..')
        cmds.rowLayout(nc=4, cw4=(80, 60, 38, 38))
        cmds.text(l='M/D Weight', w=80)
        cmds.floatField('MDFloat_BbBB', v=0.95, h=26, w=50, pre=3, min=0, max=1)
        cmds.button(w=38, h=26, l='*', c=lambda *args: self.editVtxWeight('*'))
        cmds.button(w=38, h=26, l='/', c=lambda *args: self.editVtxWeight('/'))
        cmds.setParent('..')

        cmds.showWindow(self.ToolUi)

    def spJobStart(self):
        if cmds.text('spJobVtxParent_BbBB', q=1, ex=1):
            return
        cmds.text('spJobVtxParent_BbBB', p='FiristcL_BbBB', vis=0)
        cmds.scriptJob(e=['Undo', 'WeightTool_BbBB().refreshJointList(0)'], p='spJobVtxParent_BbBB')
        cmds.scriptJob(e=['SelectionChanged', 'WeightTool_BbBB().refreshJointList(0)'], p='spJobVtxParent_BbBB')
        #cmds.scriptJob(e=['ToolChanger', '自毁'], p='spJobVtxParent_BbBB')
        cmds.scriptJob(uid=['WeightTool_BbBB', 'WeightTool_BbBB().refreshBoxChange(9)'])

        PaintSkinCmd = '"ArtPaintSkinWeightsToolOptions;"'
        if int(cmds.about(v=1)) > 2017:
            edgeCmd = '("doMenuComponentSelectionExt(\\\"" + $object + "\\\", \\\"edge\\\", 0);")'
            vertexCmd = '("doMenuComponentSelectionExt(\\\"" + $object + "\\\", \\\"vertex\\\", 0);")'
            faceCmd = '("doMenuComponentSelectionExt(\\\"" + $object + "\\\", \\\"facet\\\", 0);")'
            objModeCmd = '"maintainActiveChangeSelectMode time1 0;"'  # python (\\\"WeightTool_BbBB().refreshBoxChange(9)\\\");
        else:
            #2017以下兼容
            edgeCmd = '("doMenuComponentSelection(\\\"" + $object + "\\\", \\\"edge\\\");")'
            vertexCmd = '("doMenuComponentSelection(\\\"" + $object + "\\\", \\\"vertex\\\");")'
            faceCmd = '("doMenuComponentSelection(\\\"" + $object + "\\\", \\\"facet\\\");")'
            objModeCmd = '"changeSelectMode -component;changeSelectMode -object;"'
        mel.eval(
            'global proc dagMenuProc(string $parent, string $object){ \
            if(!size($object)){ \
            string $lsList[] = `ls -sl -o`; if(!size($lsList)){return;} else{$object = $lsList[0];}} \
            if(objectType($object) == "joint"){ \
            string $selCmd = "python(\\\"cmds.treeView(\'JointTV_BbBB\', e=1, cs=1);cmds.treeView(\'JointTV_BbBB\', e=1, si=(\'" + $object + "\', 1));WeightTool_BbBB()._weightView()\\\")"; \
            menuItem -l "Select Influence" -ec true -c $selCmd -rp "N" -p $parent; \
            }else{ \
            menuItem -l "Paint Skin Weights Tool" -ec true -c %s -rp "NW" -p $parent; \
            menuItem -l "Vertex" -ec true -c %s -rp "W" -p $parent; \
            menuItem -l "Edge" -ec true -c %s -rp "N" -p $parent; \
            menuItem -l "Face" -ec true -c %s -rp "S" -p $parent; \
            menuItem -l "Object Mode" -ec true -c %s -rp "NE" -p $parent;}}'
            %(PaintSkinCmd, vertexCmd, edgeCmd, faceCmd, objModeCmd)
        )

    def refreshBoxChange(self, force):
        if force == 9 or cmds.menuItem('OFFmeunItem_BbBB', q=1, cb=1):
            if cmds.text('spJobVtxParent_BbBB', q=1, ex=1):
                cmds.deleteUI('spJobVtxParent_BbBB', ctl=1)
            mel.eval('source "dagMenuProc.mel"')
            if cmds.window('WeightTool_BbBB', q=1, ex=1):
                cmds.iconTextCheckBox('refresh_BbBB', e=1, v=0)
        else:
            self.spJobStart()
            cmds.iconTextCheckBox('refresh_BbBB', e=1, v=1)
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
        siItem = cmds.treeView('JointTV_BbBB', q=1, si=1)
        _zero = cmds.menuItem('FImeunItem_BbBB', q=1, cb=1)
        saveData = cmds.text('saveData_BbBB', q=1, l=1).split('|')
        if refresh or _zero or saveData[0] != clusterName or saveData[1] != str(len(jointList)) or not cmds.treeView('JointTV_BbBB', q=1, ch=''):
            cmds.treeView('JointTV_BbBB', e=1, ra=1)
            if search:
                text = cmds.textField('searchText_BbBB', q=1, tx=1)
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
                if cmds.menuItem('HImeunItem_BbBB', q=1, rb=1):
                    self.addHItoList(j, _jointList)
                else:
                    cmds.treeView('JointTV_BbBB', e=1, ai=[j, ''])
                if cmds.getAttr(j + '.liw'):
                    cmds.treeView('JointTV_BbBB', e=1, i=(j, 1, 'Lock_ON.png'))
                else:
                    cmds.treeView('JointTV_BbBB', e=1, i=(j, 1, 'Lock_OFF_grey.png'))
                if not cmds.treeView('JointTV_BbBB', q=1, dls=1):
                    cmds.treeView('JointTV_BbBB', e=1, dls=(j, ''))
                if float(v):
                    cmds.treeView('JointTV_BbBB', e=1, dls=(j, '   |   %s' % v))
            if siItem:
                allItem = cmds.treeView('JointTV_BbBB', q=1, ch='')
                _Temp_ = list(set(siItem).intersection(set(allItem)))  # 求并集
                for i in _Temp_:
                    cmds.treeView('JointTV_BbBB', e=1, si=(i, 1))
        else:
            allItem = cmds.treeView('JointTV_BbBB', q=1, ch='')
            for j in allItem:
                if cmds.getAttr(j + '.liw'):
                    cmds.treeView('JointTV_BbBB', e=1, i=(j, 1, 'Lock_ON.png'))
                else:
                    cmds.treeView('JointTV_BbBB', e=1, i=(j, 1, 'Lock_OFF_grey.png'))
                Value = '%.3f' % cmds.skinPercent(clusterName, sel[0], ib=.000000001, q=1, t=j)
                if not cmds.treeView('JointTV_BbBB', q=1, dls=1):
                    cmds.treeView('JointTV_BbBB', e=1, dls=(j, ''))
                if not float(Value):
                    continue
                cmds.treeView('JointTV_BbBB', e=1, dls=(j, '   |   %s' % Value))
        cmds.text('saveData_BbBB', e=1, l='%s|%s' % (clusterName, len(jointList)))

    def addHItoList(self, i, jointList):
        jointP = cmds.listRelatives(i, p=1)
        if not jointP:
            if not cmds.treeView('JointTV_BbBB', q=1, iex=i):
                cmds.treeView('JointTV_BbBB', e=1, ai=[i, ''])
        elif cmds.treeView('JointTV_BbBB', q=1, iex=jointP[0]):
            if not cmds.treeView('JointTV_BbBB', q=1, iex=i):
                cmds.treeView('JointTV_BbBB', e=1, ai=[i, jointP[0]])
        elif jointP[0] in jointList:
            self.addHItoList(jointP[0], jointList)
            if not cmds.treeView('JointTV_BbBB', q=1, iex=i):
                cmds.treeView('JointTV_BbBB', e=1, ai=[i, jointP[0]])
        else:
            if not cmds.treeView('JointTV_BbBB', q=1, iex=i):
                cmds.treeView('JointTV_BbBB', e=1, ai=[i, ''])

    def lock_unLock(self, jnt, but):
        slItem = cmds.treeView('JointTV_BbBB', q=1, si=1)
        if not slItem or len(slItem) == 1:
            slItem = [jnt]
        if cmds.getAttr(jnt + '.liw'):
            for i in slItem:
                cmds.setAttr(i + '.liw', 0)
                cmds.treeView('JointTV_BbBB', e=1, i=(i, 1, 'Lock_OFF_grey.png'))
        else:
            for i in slItem:
                cmds.setAttr(i + '.liw', 1)
                cmds.treeView('JointTV_BbBB', e=1, i=(i, 1, 'Lock_ON.png'))

    def reSelect(self):
        allItem = cmds.treeView('JointTV_BbBB', q=1, iv=1)
        slItem = cmds.treeView('JointTV_BbBB', q=1, si=1)
        if not allItem or not slItem:
            return
        cmds.treeView('JointTV_BbBB', e=1, cs=1)
        _Temp_ = list(set(allItem).difference(set(slItem)))  # 求差集 a有b没有
        for i in _Temp_:
            cmds.treeView('JointTV_BbBB', e=1, si=(i, 1))

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
        sljntList = cmds.treeView('JointTV_BbBB', q=1, si=1)
        if not sljntList:
            om.MGlobal.displayError(u'未选择骨骼')
            return
        if mode == '+' or mode == '-':
            for v in selVtx:
                tvList = []
                for j in sljntList:
                    Value = cmds.skinPercent(clusterName, v, ib=.000000001, q=1, t=j)
                    Value = Value + cmds.floatField('ASFloat_BbBB', q=1, v=1)   \
                        if mode == '+' else Value - cmds.floatField('ASFloat_BbBB', q=1, v=1)
                    tvList.append((j, Value))
                cmds.skinPercent(clusterName, v, tv=tvList)
        elif mode == '*' or mode == '/':
            for v in selVtx:
                tvList = []
                for j in sljntList:
                    Value = cmds.skinPercent(clusterName, v, ib=.000000001, q=1, t=j)
                    Value = Value * cmds.floatField('MDFloat_BbBB', q=1, v=1)   \
                        if mode == '*' else Value / cmds.floatField('MDFloat_BbBB', q=1, v=1)
                    tvList.append((j, Value))
                cmds.skinPercent(clusterName, v, tv=tvList)
        else:
            for v in selVtx:
                tvList = [(j, float(mode)) for j in sljntList]
                cmds.skinPercent(clusterName, v, tv=tvList)
        siItem = cmds.treeView('JointTV_BbBB', q=1, si=1)
        self.refreshJointList(0)
        for i in siItem:
            cmds.treeView('JointTV_BbBB', e=1, si=(i, 1))

    def slVtx(self):
        slJnt = cmds.treeView('JointTV_BbBB', q=1, si=1)
        vtxList = []
        for i in slJnt:
            cmds.skinCluster(self.tempcluster, e=1, siv=i)
            vtxList.append(cmds.filterExpand(cmds.ls(sl=1, fl=1), sm=[28, 31, 36, 40, 46]))
        cmds.select(vtxList, r=1)

    def _weightView(self):
        if cmds.iconTextCheckBox('refresh_BbBB', q=1, v=1):
            if cmds.currentCtx() == 'artAttrSkinContext':
                mel.eval('setSmoothSkinInfluence "%s";' % cmds.treeView('JointTV_BbBB', q=1, si=1)[0])
            self._weightfloat()

    def _weightfloat(self):
        treesl = cmds.treeView('JointTV_BbBB', q=1, si=1)
        sel = cmds.ls(sl=1, fl=1)
        if not treesl or not sel:
            return
        selobj = cmds.ls(sl=1, o=1)[0]
        clusterName = mel.eval('findRelatedSkinCluster("%s")' % selobj)
        cmds.floatField('weighrfloat_BbBB', e=1, v=float('%.4f' % cmds.skinPercent(clusterName, sel[0], ib=.000000001, q=1, t=treesl[0])))

    # # # # # # # # # #
    def copyVtxWeight(self):
        selVtx = cmds.filterExpand(cmds.ls(sl=1)[0], sm=[28, 31, 36, 40, 46])
        if not selVtx:
            om.MGlobal.displayError(u'未选择点')
            return
        selobj = cmds.ls(sl=1, o=1)[0]
        clusterName = mel.eval('findRelatedSkinCluster("%s")' % selobj)
        if not clusterName:
            om.MGlobal.displayError(u'选择的物体没有蒙皮')
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
            om.MGlobal.displayError(u'未选择点')
            return
        selObj = cmds.ls(sl=1, o=1)[0]
        clusterName = mel.eval('findRelatedSkinCluster("%s")' % selObj)
        if not clusterName:
            om.MGlobal.displayError(u'选择的物体没有蒙皮')
            return
        if clusterName != self.vtxWeightInfo[0]:
            jointList = cmds.skinCluster(selObj, q=1, inf=1)
            for j in self.vtxWeightInfo[1]:
                if not j in jointList:
                    om.MGlobal.displayError(u'两个物体的蒙皮骨骼不一样！')
                    return
        tvList = [(self.vtxWeightInfo[1][i], self.vtxWeightInfo[2][i]) for i in range(len(self.vtxWeightInfo[1]))]
        # print(tvList)
        for i in selVtx:
            exec('cmds.skinPercent("%s", "%s", nrm=0, zri=1, tv=%s)' % (clusterName, i, tvList))
        self.refreshJointList(0)

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
    # # # # # # # # # #


class WeightSL_BbBB():

    def SLcheck(self, mode):   #单独调用时filePath为列表
        sel = cmds.ls(sl=1, fl=1)
        if not sel:
            om.MGlobal.displayError(u'什么都没选诶 这我很难办啊')
            return
        selobj = cmds.ls(sl=1, o=1)
        if mode == 'Load' and len(selobj) > 1:
            om.MGlobal.displayError(u'只能选择一个物体')
            return
        selVtx = cmds.filterExpand(sel, sm=[28, 31, 36, 40, 46])
        skCluster = mel.eval('findRelatedSkinCluster("%s")' %selobj[0])
        if not skCluster:
            om.MGlobal.displayError(u'选择的物体没有蒙皮')
            return
        if not selVtx:   #选的是整个物体
            seltyp = cmds.objectType(cmds.listRelatives(selobj[0], s=1, f=1)[0])
            if seltyp == 'mesh':                                                                                    #整个mesh
                if mode == 'Save':
                    filePath = cmds.fileDialog2(ff='Xml (*.xml)', ds=2) #['%s/%s.xml' %(allInPath, selobj[0])]
                    if filePath:
                        self.vtxSave_dW(filePath)
                else:
                    filePath = cmds.fileDialog2(ff='File (*.xml *.Weight)', ds=2, fm=1)
                    if filePath:
                        if filePath[0].rsplit('.', 1)[1] == 'xml':
                            self.vtxLoad_dW(filePath)
                        elif filePath[0].rsplit('.', 1)[1] == 'Weight':
                            self.vtxLoad_api(filePath)
            elif seltyp == 'nurbsCurve' or seltyp == 'nurbsSurface' or seltyp == 'subdiv' or seltyp == 'lattice':   #整个其他
                if mode == 'Save':
                    filePath = cmds.fileDialog2(ff='File (*.Weight)', ds=2)
                    if filePath:
                        self.vtxSave_Mel(filePath)
                else:
                    filePath = cmds.fileDialog2(ff='File (*.Weight)', ds=2, fm=1)
                    if filePath:
                        self.vtxLoad_Mel(filePath)
            else:
                om.MGlobal.displayError(u'选择的物体不支持')
                return
        elif cmds.filterExpand(sel, sm=[31]):                                                                        #mesh点
            if mode == 'Save':
                filePath = cmds.fileDialog2(ff='File (*.Weight)', ds=2)
                if filePath:
                    self.vtxSave_api(filePath)
            else:
                filePath = cmds.fileDialog2(ff='File (*.Weight)', ds=2, fm=1)
                if filePath:
                    self.vtxLoad_api(filePath)
        elif cmds.filterExpand(sel, sm=[28, 36, 40, 46]):                                                            #其他点
            if mode == 'Save':
                filePath = cmds.fileDialog2(ff='File (*.Weight)', ds=2)
                if filePath:
                    self.vtxSave_Mel(filePath)
            else:
                filePath = cmds.fileDialog2(ff='File (*.Weight)', ds=2, fm=1)
                if filePath:
                    self.vtxLoad_Mel(filePath)
        else:
            om.MGlobal.displayError(u'选择的点不支持')
            return

    def vtxSave_Mel(self, filePath):
        st = time.time()
        selobj = cmds.ls(sl=1, o=1)[0]
        selVtx = cmds.filterExpand(cmds.ls(sl=1, fl=1), sm=[28, 31, 36, 40, 46])
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
        skCluster = mel.eval('findRelatedSkinCluster("%s")' % selobj)
        
        with open(filePath[0], 'w') as vwfile:
            #gMainProgressBar = mel.eval('$tmp = $gMainProgressBar')
            #cmds.progressBar(gMainProgressBar, e=1, bp=1, ii=1, st='Save ...', max=len(selVtx))
            for i in selVtx:
                #cmds.progressBar(gMainProgressBar, e=1, s=1)
                valueList = cmds.skinPercent(skCluster, i, ib=.000000001, q=1, v=1)
                transList = cmds.skinPercent(skCluster, i, ib=.000000001, q=1, t=None)
                allWeight = 0
                for w in range(len(valueList)):
                    valueList[w] = round(valueList[w], 4)
                    allWeight += valueList[w]
                valueList[-1] += (1.0 - allWeight)
                tvList = [[transList[u], valueList[u]] for u in range(len(valueList))]
                wtStr = '%s--%s\n' % (i.split('.')[-1], tvList)
                vwfile.write(wtStr)
            #cmds.progressBar(gMainProgressBar, e=1, ep=1)
        print(u'处理时间: %s' %(time.time()-st))
        DisplayYes().showMessage(u'处理完成!')

    def vtxLoad_Mel(self, filePath, selectpoint=0):
        st = time.time()
        selobj = cmds.ls(sl=1, o=1)[0]
        skCluster = mel.eval('findRelatedSkinCluster("%s")' % selobj)
        jntList = cmds.skinCluster(selobj, q=1, inf=1)
        jntLock = []
        for j in jntList:
            jntLock.append(cmds.getAttr(j + '.liw'))
            cmds.setAttr(j + '.liw', 0)
        with open(filePath[0], 'r') as vwfile:
            if selectpoint:
                selVtx = [i.split('.', 1)[-1] for i in cmds.ls(sl=1, fl=1)]
            line = vwfile.readline()
            #gMainProgressBar = mel.eval('$tmp = $gMainProgressBar')
            #cmds.progressBar(gMainProgressBar, e=1, bp=1, ii=1, st='Load ...', max=len(allLine))
            num = 0
            while line:
                #cmds.progressBar(gMainProgressBar, e=1, s=1)
                strsplit = line.split('--')
                vtx = strsplit[0].strip()
                tvList = strsplit[-1].strip()
                if selectpoint:
                    if vtx == selVtx[num]:
                        num += 1
                        exec('cmds.skinPercent("%s", "%s.%s", tv=%s, nrm=1)' % (skCluster, selobj, vtx, tvList))
                    line = vwfile.readline()
                else:
                    exec('cmds.skinPercent("%s", "%s.%s", tv=%s, nrm=1)' % (skCluster, selobj, vtx, tvList))
                    line = vwfile.readline()
        #cmds.progressBar(gMainProgressBar, e=1, ep=1)
        for j, l in zip(jntList, jntLock):
            cmds.setAttr(j + '.liw', l)
        print(u'处理时间: %s' %(time.time()-st))
        DisplayYes().showMessage(u'处理完成!')

    ''' 有报错 仅供参考
    def vtxSave_Oapi(self, filePath):
        st = time.time()
        selList = Om.MSelectionList()
        Om.MGlobal.getActiveSelectionList(selList)
        #_prselList = []
        # selList.getSelectionStrings(_prselList)   #获取 MSelectionList 内容
        # print _prselList
        MDagPath = Om.MDagPath()  # 存储所选物体的路径
        MObject = Om.MObject()  # 存储所选物体的组件的列表
        selList.getDagPath(0, MDagPath)
        selList.getDependNode(0, MObject)
        # MDagPath.fullPathName()   #获取 MDagPath 内容
        slMIt = Om.MItSelectionList(selList)
        MItDagPath = Om.MDagPath()
        MItcomponent = Om.MObject()
        slMIt.getDagPath(MItDagPath, MItcomponent)

        #_selType = MDagPath.apiType()
        MDagPath.extendToShape()  # 获取当前物体的shape节点
        _selShapeType = MDagPath.apiType()
        if _selShapeType == 296:
            suf = 'vtx'
        elif _selShapeType == 267 or _selShapeType == 294:
            suf = 'cv'
        elif _selShapeType == 279:
            suf = 'pt'

        skCluster = mel.eval('findRelatedSkinCluster("%s")' % MDagPath.partialPathName())
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

        # component组件不为空（点）,线和面会强制转为点
        if MItcomponent.isNull():   #有报错
            vertIter = om.MItMeshVertex(MObject)
        else:
            vertIter = om.MItMeshVertex(MItDagPath, MItcomponent)

        with open(filePath[0], 'w') as vwfile:
            while not vertIter.isDone():
                infCount = Om.MScriptUtil()
                infCountPtr = infCount.asUintPtr()
                Om.MScriptUtil.setUint(infCountPtr, 0)
                weights = Om.MDoubleArray()
                skinNode.getWeights(MDagPath, vertIter.currentItem(), weights, infCountPtr)

                tvList = self.zeroWeightData_Save(weights, infNameList)
                vwfile.write('%s[%s]--%s\n' % (suf, vertIter.index(), tvList))
                vertIter.next()
        print(u'处理时间: %s' %(time.time()-st))
        DisplayYes().showMessage(u'处理完成!')
    '''

    def vtxLoad_Oapi(self, filePath):
        st = time.time()
        selList = Om.MSelectionList()
        Om.MGlobal.getActiveSelectionList(selList)
        MDagPath = Om.MDagPath()  # 存储所选物体的路径
        MObject = Om.MObject()  # 存储所选物体的组件的列表
        selList.getDagPath(0, MDagPath)
        selList.getDependNode(0, MObject)
        # MDagPath.fullPathName()   #获取 MDagPath 内容

        skCluster = mel.eval('findRelatedSkinCluster("%s")' % MDagPath.partialPathName())
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

        allLine = self.readWeightData_Load(filePath[0])
        if allLine == 'toMel':
            self.vtxLoad_Mel(filePath)
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
            skinNode.setWeights(MDagPath, vertIter.currentItem(), jntindex, weights, True)  # False规格化开关默认为True
            _Num += 1
            vertIter.next()
        for j, l in zip(infNameList, jntLock):
            cmds.setAttr(j + '.liw', l)
        print(u'处理时间: %s' %(time.time()-st))
        DisplayYes().showMessage(u'处理完成!')

    def vtxSave_api(self, filePath):
        st = time.time()
        selList = om.MGlobal.getActiveSelectionList()
        MDagPath = selList.getDagPath(0)  # 存储所选物体的路径
        MObject = selList.getDependNode(0)  # 存储所选物体的组件的列表
        slMIt = om.MItSelectionList(selList)
        MItDagPath, MItcomponent = slMIt.getComponent()

        #_selType = MDagPath.apiType()
        #_selShapeType = MDagPath.extendToShape().apiType()
        #if not _selType in set([110, 296, 267, 294, 279, ]):
        #    return
		
        skCluster = mel.eval('findRelatedSkinCluster("%s")' % MDagPath.partialPathName())
        selList.add(skCluster)
        skinObj = selList.getDependNode(1)
        skinNode = omAni.MFnSkinCluster(skinObj)
        infs = skinNode.influenceObjects()
        infNameList = [infs[i].partialPathName() for i in range(len(infs))]  # 骨骼列表

        # component组件不为空（点）,线和面会强制转为点
        vertIter = om.MItMeshVertex(MObject) if MItcomponent.isNull() else om.MItMeshVertex(MItDagPath, MItcomponent)
        with open(filePath[0], 'w') as vwfile:
            while not vertIter.isDone():
                weights = skinNode.getWeights(MDagPath, vertIter.currentItem())[0]

                tvList = self.zeroWeightData_Save(weights, infNameList)
                vwfile.write('vtx[%s]--%s\n' % (vertIter.index(), tvList))
                vertIter.next()
        print(u'处理时间: %s' %(time.time()-st))
        DisplayYes().showMessage(u'处理完成!')

    def vtxLoad_api(self, filePath):
        st = time.time()
        selList = om.MGlobal.getActiveSelectionList()
        MDagPath = selList.getDagPath(0)  # 存储所选物体的路径
        MObject = selList.getDependNode(0)  # 存储所选物体的组件的列表

        #_selType = MDagPath.apiType()
        #_selShapeType = MDagPath.extendToShape().apiType()
		
        skCluster = mel.eval('findRelatedSkinCluster("%s")' % MDagPath.partialPathName())
        selList.add(skCluster)
        skinObj = selList.getDependNode(1)
        skinNode = omAni.MFnSkinCluster(skinObj)
        infs = skinNode.influenceObjects()
        infNameList = [infs[i].partialPathName() for i in range(len(infs))]  # 骨骼列表

        allLine = self.readWeightData_Load(filePath[0])
        if allLine == 'toMel':
            self.vtxLoad_Mel(filePath)
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
            skinNode.setWeights(MDagPath, vertIter.currentItem(), jntindex, weights, True)  # False规格化开关默认为True
            _Num += 1
            vertIter.next()
        for j, l in zip(infNameList, jntLock):
            cmds.setAttr(j + '.liw', l)
        print(u'处理时间: %s' %(time.time()-st))
        DisplayYes().showMessage(u'处理完成!')

    def vtxSave_dW(self, filePath):
        st = time.time()
        selobj = cmds.ls(sl=1, o=1)[0]
        skCluster = mel.eval('findRelatedSkinCluster("%s")' % selobj)
        
        fileANDPath = filePath[0].rsplit('\\', 1) if '\\' in filePath else filePath[0].rsplit('/', 1)
        attributes = ['envelope', 'skinningMethod', 'normalizeWeights', 'deformUserNormals', 'useComponents']
        cmds.deformerWeights(fileANDPath[1], path=fileANDPath[0], ex=1, vc=1, wp=6, attribute=attributes, deformer=[skCluster])
        print(u'处理时间: %s' %(time.time()-st))
        DisplayYes().showMessage(u'处理完成!')

    def vtxLoad_dW(self, filePath):
        st = time.time()
        selobj = cmds.ls(sl=1, o=1)[0]
        skCluster = mel.eval('findRelatedSkinCluster("%s")' % selobj)

        jntList = cmds.skinCluster(selobj, q=1, inf=1)
        jntLock = []
        for j in jntList:
            jntLock.append(cmds.getAttr(j + '.liw'))
            cmds.setAttr(j + '.liw', 0)
        
        fileANDPath = filePath[0].rsplit('\\', 1) if '\\' in filePath else filePath[0].rsplit('/', 1)
        cmds.deformerWeights(fileANDPath[1], path=fileANDPath[0], deformer=[skCluster], im=1, method='nearest', ws=1)
        cmds.skinCluster([skCluster], e=1, forceNormalizeWeights=1)

        for j, l in zip(jntList, jntLock):
            cmds.setAttr(j + '.liw', l)
        print(u'处理时间: %s' %(time.time()-st))
        DisplayYes().showMessage(u'处理完成!')

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
            py3 = 1 if not '[u\'' in line else 0   #没有[u'说明是py3存的文件
            while line:
                strsplit = line.split('--')
                if '][' in strsplit[0]:
                    return 'toMel'
                vtx = strsplit[0].split('[', 1)[-1][:-1]
                _data = strsplit[-1].strip()
                if '], [' in _data:
                    jointList = []
                    _jointListapp = jointList.append
                    weightList = []
                    _weightListapp = weightList.append
                    if py3:
                        for i in _data[2:-2].split('], ['):
                            _str = i.split(', ')
                            _jointListapp(_str[0][1:-1])
                            _weightListapp(float(_str[1]))
                        _allappend([vtx, jointList, weightList])
                    else:
                        for i in _data[2:-2].split('], ['):
                            _str = i.split(', ')
                            _jointListapp(_str[0][2:-1])
                            _weightListapp(float(_str[1]))
                        _allappend([vtx, jointList, weightList])
                else:
                    _str = _data[2:-2].split(', ')
                    if py3:
                        _allappend([vtx, [_str[0][1:-1]], [float(_str[1])]])
                    else:
                        _allappend([vtx, [_str[0][2:-1]], [float(_str[1])]])
                line = vwfile.readline()
            _allappend([-1, None, None])
        return allLine

#WeightTool_BbBB().refreshBoxChange(9)   #报绿脚本兼容



class WeightCheckTool_BbBB():

    def ToolUi(self):
        self.Ui = 'WeightCheckTool_Ui'
        if cmds.window(self.Ui, q=1, ex=1):
            cmds.deleteUI(self.Ui)
        cmds.window(self.Ui, t='WeightCheckTool', rtf=1, tlb=1, wh=(180, 350))
        MainformLayout = cmds.formLayout()
        cmds.textScrollList('%s_vtxList' %self.Ui, ams=1, w=100, vis=0, 
                            sc=lambda *args: cmds.textScrollList('%s_weightList' %self.Ui, e=1, da=1, sii=cmds.textScrollList('%s_vtxList' %self.Ui, q=1, sii=1)))
        cmds.textScrollList('%s_weightList' %self.Ui, ams=1, vis=0, 
                            sc=lambda *args: cmds.textScrollList('%s_vtxList' %self.Ui, e=1, da=1, sii=cmds.textScrollList('%s_weightList' %self.Ui, q=1, sii=1)))
        cmds.button('%s_unfold' %self.Ui, l='>', w=20, c=lambda *args: Switchfold())
        def Switchfold():
            if cmds.button('%s_unfold' %self.Ui, q=1, l=1) == '<':
                cmds.button('%s_unfold' %self.Ui, e=1, l='>')
                cmds.textScrollList('%s_vtxList' %self.Ui, e=1, vis=0)
                cmds.textScrollList('%s_weightList' %self.Ui, e=1, vis=0)
                cmds.window(self.Ui, e=1, wh=(165, 350))
            else:
                cmds.button('%s_unfold' %self.Ui, e=1, l='<')
                cmds.textScrollList('%s_vtxList' %self.Ui, e=1, vis=1)
                cmds.textScrollList('%s_weightList' %self.Ui, e=1, vis=1)
                cmds.window(self.Ui, e=1, rtf=1, wh=(400, 350))
        cLayout = cmds.columnLayout(cat=('left', 3), h=300, w=140, rs=2)
        cmds.button(l=u'加载', w=80, h=26, c=lambda *args: self.Load())
        cmds.button(l=u'清理', w=80, h=26, c=lambda *args: self.Clean())
        cmds.button(l=u'选择', w=80, h=26, c=lambda *args: self.selectVtx()) 
        radiocollection = cmds.radioCollection()
        cmds.radioButton('%s_DecimalText' %self.Ui, l=u'小数点精度', h=22)
        cmds.intField('%s_DecimalInt' %self.Ui, w=80, v=3)
        cmds.radioButton('%s_InfluenceText' %self.Ui, l=u'骨骼影响值', h=22)
        cmds.intField('%s_InfluenceInt' %self.Ui, w=80, v=4)
        cmds.radioCollection(radiocollection, e=1, sl='%s_InfluenceText' %self.Ui)
        cmds.setParent('..')
        cmds.formLayout(MainformLayout, e=1, af=[('%s_vtxList' %self.Ui, 'top', 3),('%s_vtxList' %self.Ui, 'bottom', 3), ('%s_vtxList' %self.Ui, 'left', 3), 
                                                    ('%s_weightList' %self.Ui, 'top', 3),('%s_weightList' %self.Ui, 'bottom', 3), 
                                                    ('%s_unfold' %self.Ui, 'top', 3), ('%s_unfold' %self.Ui, 'bottom', 3), 
                                                    (cLayout, 'top', 3), (cLayout, 'right', 3)])
        cmds.formLayout(MainformLayout, e=1, ac=[('%s_weightList' %self.Ui, 'left', 3, '%s_vtxList' %self.Ui), 
                                                    ('%s_weightList' %self.Ui, 'right', 3, '%s_unfold' %self.Ui), ('%s_unfold' %self.Ui, 'right', 3, cLayout)])
        cmds.showWindow(self.Ui)
    
    def getSel(self):
        sel = cmds.ls(sl=1, fl=1)
        if not sel:
            om.MGlobal.displayError(u'什么都没选')
            return None, None
        selVtx = cmds.filterExpand(sel, sm=[28, 31, 36, 40, 46])
        selobj = cmds.ls(sl=1, o=1)[0]
        self.saveObj = selobj
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
            om.MGlobal.displayError(u'选择的物体没有蒙皮')
            return None, None
        return selVtx, clusterName

    def Load(self, mode=0):
        cmds.radioButton('%s_DecimalText' %self.Ui, e=1, l=u'小数点精度')
        cmds.radioButton('%s_InfluenceText' %self.Ui, e=1, l=u'骨骼影响值')
        listVis = 0 if cmds.button('%s_unfold' %self.Ui, q=1, l=1) == '>' else 1
        selVtx, clusterName = self.getSel()
        if not selVtx or not clusterName:
            return
        cmds.textScrollList('%s_vtxList' %self.Ui, e=1, ra=1)
        cmds.textScrollList('%s_weightList' %self.Ui, e=1, ra=1)
        self.BadList = []
        self.LoadInfo = 0
        if cmds.radioButton('%s_InfluenceText' %self.Ui, q=1, sl=1):
            self.LoadInfo = 1   #Influence
            maxValue = cmds.intField('%s_InfluenceInt' %self.Ui, q=1, v=1)
            for i in selVtx:
                valueList = cmds.skinPercent(clusterName, i, ib=.000000001, q=1, v=1)
                transList = cmds.skinPercent(clusterName, i, ib=.000000001, q=1, t=None)
                if len(valueList) > maxValue:
                    self.BadList.append(i)
                tvStr = ''
                for w, j in zip(valueList, transList):
                    tvStr += '%s ~ %s @ ' % (j, w)
                if not mode and listVis:
                    cmds.textScrollList('%s_vtxList' %self.Ui, e=1, a=i.split('.')[1])
                    cmds.textScrollList('%s_weightList' %self.Ui, e=1, a=tvStr)
            if self.BadList:
                cmds.radioButton('%s_InfluenceText' %self.Ui, e=1, l=u'超影响值的数量: %s' %len(self.BadList))
                if not mode and listVis:
                    cmds.textScrollList('%s_vtxList' %self.Ui, e=1, si=[i.split('.')[1] for i in self.BadList])
                    cmds.textScrollList('%s_weightList' %self.Ui, e=1, sii=cmds.textScrollList('%s_vtxList' %self.Ui, q=1, sii=1))
        else:
            self.LoadInfo = 2   #Decimal
            maxValue = cmds.intField('%s_DecimalInt' %self.Ui, q=1, v=1) + 2   #加上0.两位
            for i in selVtx:
                valueList = cmds.skinPercent(clusterName, i, ib=.000000001, q=1, v=1)
                transList = cmds.skinPercent(clusterName, i, ib=.000000001, q=1, t=None)
                tvStr = ''
                addTag = 0
                for w, j in zip(valueList, transList):
                    tvStr += '%s ~ %s @ ' % (j, w)
                    if not addTag and len(str(w)) > maxValue:
                        addTag = 1
                if addTag:
                    self.BadList.append(i)
                if not mode and listVis:
                    cmds.textScrollList('%s_vtxList' %self.Ui, e=1, a=i.split('.')[1])
                    cmds.textScrollList('%s_weightList' %self.Ui, e=1, a=tvStr)
            if self.BadList:
                cmds.radioButton('%s_DecimalText' %self.Ui, e=1, l=u'超小数点的数量: %s' %len(self.BadList))
                if not mode and listVis:
                    cmds.textScrollList('%s_vtxList' %self.Ui, e=1, si=[i.split('.')[1] for i in self.BadList])
                    cmds.textScrollList('%s_weightList' %self.Ui, e=1, sii=cmds.textScrollList('%s_vtxList' %self.Ui, q=1, sii=1))

    def Clean(self):
        if cmds.radioButton('%s_InfluenceText' %self.Ui, q=1, sl=1):
            if cmds.ls(sl=1, o=1)[0] == self.saveObj and self.LoadInfo == 1:
                self.RemoveInfluence()
            else:
                self.Load(1)   #不刷新界面
                self.RemoveInfluence()
        else:
            if cmds.ls(sl=1, o=1)[0] == self.saveObj and self.LoadInfo == 2:
                self.CleanDecimal()
            else:
                self.Load(1)   #不刷新界面
                self.CleanDecimal()

    def selectVtx(self):
        #vtxList = cmds.textScrollList('%s_vtxList' %Ui, q=1, si=1)
        if not self.BadList:
            return
        _shapeN = self.saveObj
        cmds.hilite(_shapeN)
        cmds.select(self.BadList, r=1)

    def CleanDecimal(self):
        clusterName = mel.eval('findRelatedSkinCluster("%s")' % self.saveObj)
        if not self.BadList:
            om.MGlobal.displayInfo(u'没有需要清理的顶点')
            return
        if not clusterName:
            return
        jntList = cmds.skinCluster(self.saveObj, q=1, inf=1)
        jntLock = []
        for j in jntList:
            jntLock.append(cmds.getAttr(j + '.liw'))
            cmds.setAttr(j + '.liw', 0)
        decimal.getcontext().rounding = 'ROUND_HALF_UP'
        _decimalInt = cmds.intField('%s_DecimalInt' %self.Ui, q=1, v=1)
        cmds.skinPercent(clusterName, prw=(10**-_decimalInt)-(10**(-_decimalInt-1)))   #生成小数点后10**-n位
        _decimalStr = "{:.%sf}" %_decimalInt
        _decimal = decimal.Decimal(_decimalStr.format(1))
        _decimal1 = decimal.Decimal('1.0')
        for i in self.BadList:
            transList = cmds.skinPercent(clusterName, i, ib=.000000001, q=1, t=None)
            _tv = []
            _Num = 0
            for j in transList:
                # mel.eval('global proc float _rounding(float $f, int $n){float $N = pow(10, ($n));float $a = $f%(1/$N)*$N;float $B;     \
                #            if($a>0.5)$B = ceil($f*$N)/$N;else$B = floor($f*$N/$N);return $B;}')     #精度问题?
                #Value = mel.eval('_rounding(%s, %s)' %(cmds.skinPercent(clusterName, i, ib=.000000001, q=1, t=j), cmds.intField('DecimalInt', q=1, v=1)))
                Value = decimal.Decimal(str(cmds.skinPercent(clusterName, i, ib=.000000001, q=1, t=j))).quantize(_decimal)
                if Value == 1:
                    _tv.append([j, 1])
                    break
                if Value == 0:
                    continue
                _Num += Value
                _tv.append([j, round(float(Value), _decimalInt)])
            _tv[-1][1] = round(float(decimal.Decimal(str(_tv[-1][1])) + _decimal1 - _Num), _decimalInt)
            cmds.skinPercent(clusterName, i, tv=_tv, nrm=1)
        for j, l in zip(jntList, jntLock):
            cmds.setAttr(j + '.liw', l)
        self.Load()

    def RemoveInfluence(self):
        clusterName = mel.eval('findRelatedSkinCluster("%s")' % self.saveObj)
        if not self.BadList:
            om.MGlobal.displayInfo(u'没有需要清理的顶点')
            return
        if not clusterName:
            return
        jntList = cmds.skinCluster(self.saveObj, q=1, inf=1)
        jntLock = []
        for j in jntList:
            jntLock.append(cmds.getAttr(j + '.liw'))
            cmds.setAttr(j + '.liw', 0)
        Influence = cmds.intField('%s_InfluenceInt' %self.Ui, q=1, v=1)
        for v in self.BadList:
            transList = cmds.skinPercent(clusterName, v, ib=.000000001, q=1, t=None)
            while len(transList) > Influence:
                valueList = cmds.skinPercent(clusterName, v, ib=.000000001, q=1, v=1)
                tvdic = {}
                for w, j in zip(valueList, transList):
                    tvdic[j] = w
                tvList = sorted(tvdic.items(), key=lambda item: item[1])
                cmds.skinPercent(clusterName, v, tv=(tvList[0][0], 0), nrm=1)
                transList = cmds.skinPercent(clusterName, v, ib=.000000001, q=1, t=None)
        for j, l in zip(transList, jntLock):
            cmds.setAttr(j + '.liw', l)
        self.Load()

#WeightTool_BbBB().ToolUi()
#WeightCheckTool_BbBB().ToolUi()
