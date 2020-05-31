# -*- coding: utf-8 -*-
try:
    from PySide2 import QtCore, QtGui, QtWidgets
    import shiboken2
except ImportError:
    from PySide import QtGui as QtWidgets
    from PySide import QtCore
    import shiboken as shiboken2
from maya import cmds, mel
import maya.OpenMaya as Om
import maya.OpenMayaUI as Omui
import decimal


class WeightTool():

    def ToolUi(self):
        self.ToolUi = 'WeightTool'
        if cmds.window(self.ToolUi, q=1, ex=1):
            cmds.deleteUI(self.ToolUi)
        cmds.window(self.ToolUi, t=self.ToolUi, rtf=1, mb=1, mxb=0, wh=(230, 500))
        cmds.menu(l='S/L', to=1)
        cmds.menuItem(l='Save', c=lambda *args: WeightTool().vtxSave())
        cmds.menuItem(l='Load', c=lambda *args: WeightTool().vtxLoad())
        cmds.menu(l='Select', to=1)
        cmds.menuItem(l='Save', c=lambda *args: WeightTool().createSelect())
        cmds.menuItem(l='Save', c=lambda *args: WeightTool().getSelect())
        cmds.columnLayout('FiristcL', cat=('both', 2), rs=2, cw=220, adj=1)
        cmds.text('spJobchangeVtx', p='FiristcL', vis=0)
        cmds.scriptJob(e=['SelectTypeChanged', 'WeightTool().refreshBoxChange(None)'], p='spJobchangeVtx')
        cmds.rowLayout(nc=6, adj=2)
        cmds.iconTextCheckBox('refresh', i='refresh.png', w=20, h=20,
                                onc=lambda *args: self.spJobStart(), ofc=lambda *args: self.refreshBoxChange(9))
        cmds.textField('searchText', h=22, tcc=lambda *args: self.searchList())
        cmds.popupMenu()
        cmds.radioMenuItemCollection()
        cmds.menuItem('HImeunItem', l='Hierarchy', rb=1, c=lambda *args: self.refreshJointList())
        cmds.menuItem('AImeunItem', l='Alphabetically', rb=0, c=lambda *args: self.refreshJointList())
        cmds.menuItem('FImeunItem', l='Filter Zero', cb=1, c=lambda *args: self.refreshJointList())
        #cmds.iconTextButton(i='expandInfluenceList.png', w=20, h=20,
        #    c=lambda *args: cmds.treeView('JointTV', e=1, h=cmds.treeView('JointTV', q=1, h=1) + 20))
        #cmds.iconTextButton(i='retractInfluenceList.png', w=20, h=20,
        #    c=lambda *args: cmds.treeView('JointTV', e=1, h=cmds.treeView('JointTV', q=1, h=1) - 20))
        #invertSelection.png
        cmds.iconTextButton(i='invertSelection.png', w=20, h=20, c=lambda *args: self.reSelect())
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.formLayout('JointTVLayout')
        cmds.treeView('JointTV', nb=1, h=100, scc='pass', pc=(1, self.lock_unLock))
        cmds.popupMenu()
        cmds.menuItem(l='Lock All')
        cmds.menuItem(l='Unlock All')
        #cmds.menuItem(l='Select Vtx')
        cmds.formLayout('JointTVLayout', e=1, af=[('JointTV', 'top', 0), ('JointTV', 'bottom', 0),
                                                    ('JointTV', 'left', 3), ('JointTV', 'right', 3)])
        cmds.setParent('..')
        cmds.columnLayout('vtxToolcL', cat=('both', 2), rs=2, cw=225)
        cmds.rowLayout(nc=4, cw4=(50, 50, 50, 50))
        cmds.floatField(v=.05, w=52, h=26, pre=4, min=0, max=1, ec='wait')
        cmds.button(w=50, h=26, l='Copy', c=lambda *args: self.copyVtxWeight())
        cmds.button(w=50, h=26, l='Paste', c=lambda *args: self.pasteVtxWeight())
        cmds.popupMenu()
        cmds.menuItem(l='PasteAll', c=lambda *args: mel.eval("polyConvertToShell;artAttrSkinWeightPaste;"))
        cmds.button(w=65, h=26, l='Hammer', c=lambda *args: mel.eval('weightHammerVerts'))
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
        cmds.floatField('ASFloat', v=0.05, h=26, w=50, pre=3, min=0, max=1)
        cmds.button(w=38, h=26, l='+', c=lambda *args: self.editVtxWeight('+'))
        cmds.button(w=38, h=26, l='-', c=lambda *args: self.editVtxWeight('-'))
        cmds.setParent('..')
        cmds.rowLayout(nc=4, cw4=(80, 60, 38, 38))
        cmds.text(l='M/D Weight', w=80)
        cmds.floatField('MDFloat', v=0.95, h=26, w=50, pre=3, min=0, max=1)
        cmds.button(w=38, h=26, l='*', c=lambda *args: self.editVtxWeight('*'))
        cmds.button(w=38, h=26, l='/', c=lambda *args: self.editVtxWeight('/'))
        cmds.setParent('..')

        cmds.showWindow(self.ToolUi)

    def spJobStart(self):
        if cmds.text('spJobVtxParent', q=1, ex=1):
            return
        cmds.text('spJobVtxParent', p='FiristcL', vis=0)
        cmds.scriptJob(e=['Undo', 'WeightTool().refreshJointList()'], p='spJobVtxParent')
        cmds.scriptJob(e=['SelectionChanged', 'WeightTool().refreshJointList()'], p='spJobVtxParent')
        #cmds.scriptJob(e=['ToolChanger', '自毁'], p='spJobVtxParent')
        cmds.scriptJob(uid=['WeightTool', 'WeightTool().refreshBoxChange(9)'])
        mel.eval('global proc dagMenuProc(string $parent, string $object){ \
                if(objectType($object) == "joint"){ \
                string $selCmd = "python (\\\"SelectInfluence(\'" + $object + "\')\\\")"; \
                menuItem -l "Select Influence" -ec true -c $selCmd -rp "N" -p $parent; \
                }else{ \
                menuItem -l "Object Mode" -ec true -c \
                    "python (\\\"WeightTool().refreshBoxChange(9)\\\");maintainActiveChangeSelectMode OvO 0" -rp "E" -p $parent;}}')

    def refreshBoxChange(self, force):
        if force == 9 or not cmds.selectType(q=1, ocm=1, pv=1):
            if cmds.text('spJobVtxParent', q=1, ex=1):
                cmds.deleteUI('spJobVtxParent', ctl=1)
            mel.eval('source "dagMenuProc.mel"')
            if cmds.window(self.ToolUi, q=1, ex=1):
                cmds.iconTextCheckBox('refresh', e=1, v=0)
        else:
            self.spJobStart()
            cmds.iconTextCheckBox('refresh', e=1, v=1)
    
    def refreshJointList(self):
        if not cmds.selectType(q=1, ocm=1, pv=1):
            self.refreshBoxChange(9)
            return
        sel = cmds.ls(sl=1, fl=1)
        if not sel:
            return
        selobj = cmds.ls(sl=1, o=1)[0]
        if cmds.menuItem('FImeunItem', q=1, cb=1):
            jointList = cmds.skinCluster(selobj, q=1, wi=1)
        else:
            jointList = cmds.skinCluster(selobj, q=1, inf=1)
        cmds.treeView('JointTV', e=1, ra=1)
        for i in jointList:
            if cmds.menuItem('HImeunItem', q=1, rb=1):
                self.addHItoList(i, jointList)
            else:
                cmds.treeView('JointTV', e=1, ai=[i, ''])
        allItem = cmds.treeView('JointTV', q=1, ch='')
        clusterName = mel.eval('findRelatedSkinCluster("%s")' % selobj)
        for j in allItem:
            if cmds.getAttr(j + '.liw'):
                cmds.treeView('JointTV', e=1, i=(j, 1, 'Lock_ON.png'))
            else:
                cmds.treeView('JointTV', e=1, i=(j, 1, 'Lock_OFF_grey.png'))
            Value = '%.3f' % cmds.skinPercent(clusterName, sel[0], ib=.000000000000001, q=1, t=j)
            if not float(Value):
                continue
            cmds.treeView('JointTV', e=1, dl=(j, '%s   |   %s' % (j, Value)))
            
    def addHItoList(self, i, jointList):
        jointP = cmds.listRelatives(i, p=1)
        if not jointP:
            if not cmds.treeView('JointTV', q=1, iex=i):
                cmds.treeView('JointTV', e=1, ai=[i, ''])
        elif cmds.treeView('JointTV', q=1, iex=jointP[0]):
            if not cmds.treeView('JointTV', q=1, iex=i):
                cmds.treeView('JointTV', e=1, ai=[i, jointP[0]])
        elif jointP[0] in jointList:
            self.addHItoList(jointP[0], jointList)
            if not cmds.treeView('JointTV', q=1, iex=i):
                cmds.treeView('JointTV', e=1, ai=[i, jointP[0]])
        else:
            if not cmds.treeView('JointTV', q=1, iex=i):
                cmds.treeView('JointTV', e=1, ai=[i, ''])

    def lock_unLock(self, jnt, but):
        #cmds.getAttr(i + '.liw', l=1)
        slItem = cmds.treeView('JointTV', q=1, si=1)
        if not slItem:
            slItem = [jnt]
        if cmds.getAttr(jnt + '.liw'):
            for i in slItem:
                cmds.setAttr(i + '.liw', 0)
                cmds.treeView('JointTV', e=1, i=(i, 1, 'Lock_OFF_grey.png'))
        else:
            for i in slItem:
                cmds.setAttr(i + '.liw', 1)
                cmds.treeView('JointTV', e=1, i=(i, 1, 'Lock_ON.png'))

    def reSelect(self):
        allItem = cmds.treeView('JointTV', q=1, iv=1)
        slItem = cmds.treeView('JointTV', q=1, si=1)
        cmds.treeView('JointTV', e=1, cs=1)
        #for i in slItem:
        #    allItem.remove(i)
        for i in allItem:
            if i in slItem:
                continue
            cmds.treeView('JointTV', e=1, si=(i, 1))
    
    def editVtxWeight(self, mode):
        sel = cmds.ls(sl=1, fl=1)
        if not sel:
            return
        selVtx = cmds.filterExpand(sel, sm=[28, 31, 36, 40, 46])
        if not selVtx:
            return
        selobj = cmds.ls(sl=1, o=1)[0]
        clusterName = mel.eval('findRelatedSkinCluster("%s")' %selobj)
        if not clusterName:
            return
        sljntList = cmds.treeView('JointTV', q=1, si=1)
        if not sljntList:
            Om.MGlobal.displayError('Not Selected Joint')
            return
        if mode == '+' or mode == '-':
            for v in selVtx:
                tvList = []
                for j in sljntList:
                    Value = cmds.skinPercent(clusterName, v, ib=.000000000000001, q=1, t=j)
                    Value = Value + cmds.floatField('ASFloat', q=1, v=1)   \
                        if mode == '+' else Value - cmds.floatField('ASFloat', q=1, v=1)
                    tvList.append((j, Value))
                cmds.skinPercent(clusterName, v, tv=tvList)
        elif mode == '*' or mode == '/':
            for v in selVtx:
                tvList = []
                for j in sljntList:
                    Value = cmds.skinPercent(clusterName, v, ib=.000000000000001, q=1, t=j)
                    Value = Value * cmds.floatField('MDFloat', q=1, v=1)   \
                        if mode == '*' else Value / cmds.floatField('MDFloat', q=1, v=1)
                    tvList.append((j, Value))
                cmds.skinPercent(clusterName, v, tv=tvList)
        else:
            for v in selVtx:
                tvList = []
                for j in sljntList:
                    Value = float(mode)
                    tvList.append((j, Value))
                cmds.skinPercent(clusterName, v, tv=tvList)
        siItem = cmds.treeView('JointTV', q=1, si=1)
        self.refreshJointList()
        for i in siItem:
            cmds.treeView('JointTV', e=1, si=(i, 1))

    def searchList(self):
        text = cmds.textField('searchText', q=1, tx=1)
        allItem = cmds.treeView('JointTV', q=1, ch='')
        if not allItem:
            return
        if not text:
            self.refreshJoiniftList()
            return
        for i in allItem:
            if text in i:
                chList = cmds.treeView('JointTV', q=1, ch=i)
                __Temp = cmds.treeView('JointTV', e=1, ri=i)
                if len(chList) == 1:
                    return
                else:
                    for i in chList:
                        self.addHItoList(i, chList)
                        
    # # # # # # # # # #
    def copyVtxWeight(self):
        selVtx = cmds.filterExpand(cmds.ls(sl=1)[0], sm=[28, 31, 36, 40, 46])
        if not selVtx:
            Om.MGlobal.displayError('Not Selected Vtx')
            return
        selobj = cmds.ls(sl=1, o=1)[0]
        clusterName = mel.eval('findRelatedSkinCluster("%s")' %selobj)
        if not clusterName:
            Om.MGlobal.displayError('Select No Skin')
            return
        ValueList = cmds.skinPercent(clusterName, selVtx, q=1, ib=.000000000000001, v=1)
        TransList = cmds.skinPercent(clusterName, selVtx, q=1, ib=.000000000000001, t=None)
        '''   #倒序循环
        for i in range(len(ValueList)-1, -1, -1):
            if ValueList[i] < .0001:
                del ValueList[i], TransList[i]
        '''
        self.vtxWeightInfo = [clusterName, TransList, ValueList]
        #print(self.vtxWeightInfo)

    def pasteVtxWeight(self):
        selVtx = cmds.filterExpand(cmds.ls(sl=1, fl=1), sm=[28, 31, 36, 40, 46])
        if not selVtx:
            Om.MGlobal.displayError('Not Selected Vtx')
            return
        selObj = cmds.ls(sl=1, o=1)[0]
        clusterName = mel.eval('findRelatedSkinCluster("%s")' %selObj)
        if not clusterName:
            Om.MGlobal.displayError('Select No Skin')
            return
        if clusterName != self.vtxWeightInfo[0]:
            jointList = cmds.skinCluster(selObj, q=1, inf=1)
            for j in self.vtxWeightInfo[1]:
                if not j in jointList:
                    Om.MGlobal.displayError('Joint are different !!!')
                    return
        tvList = []
        for i in range(len(self.vtxWeightInfo[1])):
            tvList.append((self.vtxWeightInfo[1][i], self.vtxWeightInfo[2][i]))
        #print(tvList)
        for i in selVtx:
            exec('cmds.skinPercent("%s", "%s", nrm=0, zri=1, tv=%s)' %(clusterName, i, tvList))
    # # # # # # # # # #

    def createSelect(self):
        selvtx = cmds.ls(sl=1)
        selobj = cmds.ls(sl=1, o=1)[0]
        cluWs = cmds.getAttr(cmds.cluster(n='_tempClu_')[1] + 'Shape.origin')[0]
        Curname = cmds.circle(n='_selectCur_')[0]
        cmds.setAttr(Curname + '.translate', cmds.polyEvaluate(selobj, b=1)[0][1] + 1, cluWs[1], cluWs[2])
        cmds.addAttr(Curname, ln='vtxinfo', dt='string')
        cmds.setAttr(Curname + '.vtxinfo', '', type='string')
        for i in selvtx:
            cmds.setAttr(Curname + '.vtxinfo', cmds.getAttr(Curname + '.vtxinfo') + i + ',', type='string')
        cmds.delete('_tempClu_Handle')
        cmds.setAttr(cmds.listRelatives(Curname, c=1, s=1)[0] + '.overrideEnabled', 1)
        cmds.setAttr(cmds.listRelatives(Curname, c=1, s=1)[0] + '.overrideColor', 16)

    def getSelect(self):
        onevtx = cmds.getAttr(cmds.ls(sl=1)[0] + '.vtxinfo').split(',')[0:-1]
        cmds.select(cl=1)
        for i in onevtx:
            cmds.select(i, add=1)

    def vtxSave(self):
        sel = cmds.ls(sl=1, fl=1)
        if not sel:
            Om.MGlobal.displayError('Select Nothing')
            return
        selVtx = cmds.filterExpand(sel, sm=[28, 31, 36, 40, 46])
        if not selVtx:
            selobj = cmds.ls(sl=1, o=1)[0]
            if not selobj:
                return
            seltyp = cmds.objectType(cmds.listRelatives(selobj, s=1, f=1)[0])
            if seltyp == 'mesh':
                suf = '.vtx'
            elif seltyp == 'nurbsCurve' or seltyp == 'nurbsSurface':
                suf = '.cv'
            elif seltyp == 'subdiv':
                suf = '.smp'
            elif seltyp == 'lattice':
                suf = '.pt'
            selVtx = cmds.ls(selobj + suf + '[*]', fl=1)
        clusterName = mel.eval('findRelatedSkinCluster("%s")' %selobj)
        if not clusterName:
            Om.MGlobal.displayError('Select No Skin')
            return
        filePath = cmds.fileDialog(m=1, dm='*.vtxWeight')
        if not filePath:
            return
        with open(filePath, 'w') as vwfile:
            gMainProgressBar = mel.eval('$tmp = $gMainProgressBar')
            cmds.progressBar(gMainProgressBar, e=1, bp=1, ii=1, st='Save ...', max=len(selVtx))
            for i in selVtx:
                cmds.progressBar(gMainProgressBar, e=1, s=1)
                valueList = cmds.skinPercent(clusterName, i, ib=.000000000000001, q=1, v=1)
                transList = cmds.skinPercent(clusterName, i, ib=.000000000000001, q=1, t=None)
                tvList = [[transList[u], valueList[u]] for u in range(len(valueList))]
                wtStr = '%s--%s\r\n' %(i.split('.')[-1], tvList)
                vwfile.write(wtStr)
            cmds.progressBar(gMainProgressBar, e=1, ep=1)
        DisplayYes().showMessage('Finish!')

    def vtxLoad(self):
        sel = cmds.ls(sl=1, fl=1)
        if not sel:
            Om.MGlobal.displayError('Select Nothing')
            return
        selobj = cmds.ls(sl=1, o=1)[0]
        clusterName = mel.eval('findRelatedSkinCluster("%s")' %selobj)
        if not clusterName:
            Om.MGlobal.displayError('Select No Skin')
            return
        filePath = cmds.fileDialog(m=0, dm='*.vtxWeight')
        if not filePath:
            return
        allLine = []
        with open(filePath, 'r') as vwfile:
            line = vwfile.readline()
            while line:
                allLine.append(line)
                line = vwfile.readline()
        gMainProgressBar = mel.eval('$tmp = $gMainProgressBar')
        cmds.progressBar(gMainProgressBar, e=1, bp=1, ii=1, st='Load ...', max=len(allLine))
        for i in allLine:
            cmds.progressBar(gMainProgressBar, e=1, s=1)
            vtx = i.split('--')[0].strip()
            tvList = i.split('--')[-1].strip()
            exec('cmds.skinPercent("%s", "%s", tv=%s)' % (clusterName, selobj + '.' + vtx, tvList))
        cmds.progressBar(gMainProgressBar, e=1, ep=1)
        DisplayYes().showMessage('Finish!')


class DisplayYes():   #报绿

    def __init__(self):
        self.gCommandLine = mel.eval('$tmp = $gCommandLine')

    def showMessage(self, message):
        widget = shiboken2.wrapInstance(long(Omui.MQtUtil.findControl(self.gCommandLine)), QtWidgets.QWidget)
        widget.findChild(QtWidgets.QLineEdit).setStyleSheet('background-color:rgb(10,200,15);' + 'color:black;')
        cmds.select('time1', r=1)
        WeightTool().refreshBoxChange(9)
        cmds.text('spJobReLine', p='FiristcL', vis=0)   # p = Layout
        cmds.scriptJob(e=['SelectionChanged', 'DisplayYes().resetLine()'], p='spJobReLine')
        Om.MGlobal.displayInfo(message)

    def resetLine(self):
        cmds.deleteUI('spJobReLine', ctl=1)
        cmds.deleteUI(self.gCommandLine.rsplit('|', 1)[0])
        mel.eval('source "initCommandLine.mel"')


class WeightCheckTool():

    def ToolUi(self):
        ToolUi = 'WeightCheckTool'
        if cmds.window(ToolUi, q=1, ex=1):
            cmds.deleteUI(ToolUi)
        cmds.window(ToolUi, t=ToolUi, rtf=1, mb=1, wh=(500, 300))
        cmds.menu(l='View', to=0)
        cmds.menuItem('SNmenuItem', l='View Object Name', cb=0, c=lambda *args: self.Load())
        cmds.formLayout('MainformLayout')
        cmds.paneLayout('ListLayout', cn='vertical3', ps=(1, 1, 1))
        cmds.textScrollList('vtxList', ams=1, sc=lambda *args:
                                cmds.textScrollList('weightList', e=1, da=1, sii=cmds.textScrollList('vtxList', q=1, sii=1)))
        cmds.textScrollList('weightList', ams=1, sc=lambda *args:
                                cmds.textScrollList('vtxList', e=1, da=1, sii=cmds.textScrollList('weightList', q=1, sii=1)))
        cmds.setParent('..')
        cmds.columnLayout('cLayout', cat=('right', 5), cw=100)
        cmds.text(l='', h=3)
        cmds.button(l='Load', w=80, h=26, c=lambda *args: self.Load())
        cmds.button(l='Clean', w=80, h=26, c=lambda *args: self.Clean())
        cmds.button(l='Remove Min', w=80, h=26, c=lambda *args: self.RemoveMin())
        cmds.popupMenu()
        cmds.menuItem(l='Remove as Value', c=lambda *args: self.RemoveValue())
        cmds.button(l='Select', w=80, h=26, c=lambda *args: cmds.select(self.Number, r=1))
        cmds.text(l='Decimal', h=20)
        cmds.intField('DecimalInt', v=3)
        cmds.text(l='Influence', h=20)
        cmds.intField('InfluenceInt', v=3)
        cmds.text('ViewNum', vis=0, h=20)
        
        cmds.formLayout('MainformLayout', e=1, af=[('ListLayout', 'top', 0), ('ListLayout', 'bottom', 0), ('ListLayout', 'left', 3), ('cLayout', 'right', 3)])
        cmds.formLayout('MainformLayout', e=1, ac=('ListLayout', 'right', 3, 'cLayout'))
        cmds.showWindow(ToolUi)
    
    def getSel(self):
        sel = cmds.ls(sl=1, fl=1)
        if not sel:
            Om.MGlobal.displayError('Select Nothing')
            return None, None
        selVtx = cmds.filterExpand(sel, sm=[28, 31, 36, 40, 46])
        selobj = cmds.ls(sl=1, o=1)[0]
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
            selVtx = cmds.ls(selobj + suf + '[*]', fl=1)
        clusterName = mel.eval('findRelatedSkinCluster("%s")' %selobj)
        if not clusterName:
            Om.MGlobal.displayError('Select No Skin')
            return None, None
        return selVtx, clusterName

    def Load(self):
        cmds.text('ViewNum', e=1, vis=0)
        selVtx, clusterName = self.getSel()
        if not selVtx or not clusterName:
            return
        cmds.textScrollList('vtxList', e=1, ra=1)
        cmds.textScrollList('weightList', e=1, ra=1)
        self.Number = []
        for i in selVtx:
            valueList = cmds.skinPercent(clusterName, i, ib=.000000000000001, q=1, v=1)
            transList = cmds.skinPercent(clusterName, i, ib=.000000000000001, q=1, t=None)
            tvStr = ''
            if len(valueList) > cmds.intField('InfluenceInt', q=1, v=1):
                self.Number.append(i)
            for w, j in zip(valueList, transList):
                Value = str(w).rstrip('0').rstrip('.')
                tvStr += '%s ~ %s @ ' % (j, Value)
            if not cmds.menuItem('SNmenuItem', q=1, cb=1):
                i = i.split('.')[1]
            cmds.textScrollList('vtxList', e=1, a=i)
            cmds.textScrollList('weightList', e=1, a=tvStr)
        if self.Number:
            cmds.text('ViewNum', e=1, vis=1, l='Number: ' + str(len(self.Number)))
            if not cmds.menuItem('SNmenuItem', q=1, cb=1):
                for i in self.Number:
                    i = i.split('.')[1]
                    cmds.textScrollList('vtxList', e=1, si=i)
            else:
                cmds.textScrollList('vtxList', e=1, si=self.Number)
            cmds.textScrollList('weightList', e=1, sii=cmds.textScrollList('vtxList', q=1, sii=1))
            
    def Clean(self):
        selVtx, clusterName = self.getSel()
        if not selVtx or not clusterName:
            return
        jntList = cmds.skinCluster(cmds.ls(selVtx[0], o=1)[0], q=1, inf=1)
        jntLock = [cmds.getAttr(j + '.liw') for j in jntList]
        for i in selVtx:
            transList = cmds.skinPercent(clusterName, i, ib=.000000000000001, q=1, t=None)
            tempCode = '%.' + str(cmds.intField('DecimalInt', q=1, v=1)) + 'f'
            for j in transList:
                cmds.setAttr(j + '.liw', 0)
            for j in transList:
                #mel.eval('global proc float _rounding(float $f, int $n){float $N = pow(10, ($n));float $a = $f%(1/$N)*$N;float $B;     \
                #            if($a>0.5)$B = ceil($f*$N)/$N;else$B = floor($f*$N/$N);return $B;}')     #精度问题?
                #Value = mel.eval('_rounding(%s, %s)' %(cmds.skinPercent(clusterName, i, ib=.000000000000001, q=1, t=j), cmds.intField('DecimalInt', q=1, v=1)))
                decimal.getcontext().rounding = 'ROUND_HALF_UP'
                Value = float(str(decimal.Decimal(str(cmds.skinPercent(clusterName, i, ib=.000000000000001, q=1, t=j))).
                            quantize(decimal.Decimal(tempCode %1))).rstrip('0').rstrip('.'))
                #if Value == 0:
                #    continue
                cmds.skinPercent(clusterName, i, tv=(j, Value))
                cmds.setAttr(j + '.liw', 1)
        for j, l in zip(jntList, jntLock):
            cmds.setAttr(j + '.liw', l)
        self.Load()
    
    def RemoveMin(self):
        if not self.Number:
            return
        obj = cmds.ls(self.Number[0], o=1)[0]
        clusterName = mel.eval('findRelatedSkinCluster("%s")' % obj)
        if not clusterName:
            Om.MGlobal.displayError('Select No Skin')
            return
        for v in self.Number:
            transList = cmds.skinPercent(clusterName, v, ib=.000000000000001, q=1, t=None)
            jntLock = []
            for j in transList:
                jntLock.append(cmds.getAttr(j + '.liw'))
                cmds.setAttr(j + '.liw', 0)
            while len(transList) > cmds.intField('InfluenceInt', q=1, v=1):
                valueList = cmds.skinPercent(clusterName, v, ib=.000000000000001, q=1, v=1)
                tvdic = {}
                for w, j in zip(valueList, transList):
                    tvdic[j] = w
                tvList = sorted(tvdic.items(), key=lambda item: item[1])
                cmds.skinPercent(clusterName, v, tv=(tvList[0][0], 0))
                transList = cmds.skinPercent(clusterName, v, ib=.000000000000001, q=1, t=None)
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
                valueList = cmds.skinPercent(clusterName, i, ib=.000000000000001, q=1, v=1)
                transList = cmds.skinPercent(clusterName, i, ib=.000000000000001, q=1, t=None)
                reTvList = [(j, 0) for w, j in zip(valueList, transList) if w <= reValue]
                cmds.skinPercent(clusterName, i, tv=reTvList)
            for j, l in zip(jntList, jntLock):
                cmds.setAttr(j + '.liw', l)
            self.Load()

WeightTool().ToolUi()
#WeightCheckTool().ToolUi()
