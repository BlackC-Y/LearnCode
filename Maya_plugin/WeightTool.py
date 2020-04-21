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


class WeightTool():

    def __init__(self):
        pass

    def WeightToolUi(self):
        self.WeightToolUi = 'WeightTool'
        if cmds.window(self.WeightToolUi, q=1, ex=1):
            cmds.deleteUI(self.WeightToolUi)
        cmds.window(self.WeightToolUi, t=self.WeightToolUi, mb=1, mxb=0, wh=(255, 500))
        cmds.menu(l='S/L', to=1)
        cmds.menuItem(l='Save', c=lambda *args: LTools().vtxSave())
        cmds.menuItem(l='Load', c=lambda *args: LTools().vtxLoad())
        cmds.menu(l='Select', to=1)
        cmds.menuItem(l='Save', c=lambda *args: LTools().createSelect())
        cmds.menuItem(l='Save', c=lambda *args: LTools().getSelect())
        cmds.columnLayout('MaincL', cat=('both', 2), rs=2, cw=250, adj=1)
        cmds.text('spJobchangeVtx', p='MaincL', vis=0)
        cmds.scriptJob(e=['SelectTypeChanged', 'WeightTool().refreshBoxChange(None)'], p='spJobchangeVtx')
        cmds.rowLayout(nc=6, adj=2)
        cmds.iconTextCheckBox('refresh', i='refresh.png', w=20, h=20,
            onc=lambda *args: self.spJobStart(), ofc=lambda *args: self.refreshBoxChange(9))
        cmds.textField('searchText', h=22, cc='Wait', ec='Wait')
        cmds.popupMenu()
        cmds.radioMenuItemCollection()
        cmds.menuItem('HImeunItem', l='Hierarchy', rb=1, c=lambda *args: 'pass')
        cmds.menuItem('AImeunItem', l='Alphabetically', rb=0, c=lambda *args: 'pass')
        cmds.menuItem('FImeunItem', l='Filter Zero', cb=1, c=lambda *args: 'pass')
        cmds.iconTextButton(i='expandInfluenceList.png', w=20, h=20,
            c=lambda *args: cmds.treeView('JointTV', e=1, h=cmds.treeView('JointTV', q=1, h=1) + 20))
        cmds.iconTextButton(i='retractInfluenceList.png', w=20, h=20,
            c=lambda *args: cmds.treeView('JointTV', e=1, h=cmds.treeView('JointTV', q=1, h=1) - 20))
        #revealSelected.png
        #invertSelection.png
        cmds.setParent('..')
        cmds.treeView('JointTV', p='MaincL', nb=1,
                    h=300, scc='pass', pc=(1, 'pass'))
        cmds.popupMenu()
        cmds.rowLayout(nc=4, cw4=(60, 50, 50, 60))
        cmds.floatField(v=0.05, w=62, h=26, pre=3, min=0, max=1, ec='wait')
        cmds.button(w=50, h=26, l='Copy', c=lambda *args: mel.eval("artAttrSkinWeightCopy"))
        cmds.button(w=55, h=26, l='Paste', c=lambda *args: mel.eval("artAttrSkinWeightPaste"))
        cmds.button(w=70, h=26, l='PasteAll', c=lambda *args: mel.eval("polyConvertToShell;artAttrSkinWeightPaste;"))
        cmds.setParent('..')
        cmds.rowLayout(nc=5, cw5=(47, 47, 47, 47, 47))
        cmds.button(w=47, h=26, l='Loop', c=lambda *args: cmds.polySelectSp(loop=1))
        cmds.button(w=47, h=26, l='Ring',
            c=lambda *args: mel.eval("PolySelectConvert 2;PolySelectTraverse 2;polySelectEdges edgeRing;PolySelectConvert 3;"))
        cmds.button(w=47, h=26, l='Shell', c=lambda *args: mel.eval("polyConvertToShell"))
        cmds.button(w=47, h=26, l='Shrink', c=lambda *args: cmds.polySelectConstraint(pp=2))
        cmds.button(w=47, h=26, l='Grow', c=lambda *args: cmds.polySelectConstraint(pp=1))
        cmds.setParent('..')
        cmds.rowLayout(nc=7, cw=[(1, 33), (2, 33), (3, 33), (4, 33), (5, 33), (6, 33), (7, 33)])
        cmds.button(w=33, h=26, l='0', c='Wait')
        cmds.button(w=33, h=26, l='.1', c='Wait')
        cmds.button(w=33, h=26, l='.25', c='Wait')
        cmds.button(w=33, h=26, l='.5', c='Wait')
        cmds.button(w=33, h=26, l='.75', c='Wait')
        cmds.button(w=33, h=26, l='.9', c='Wait')
        cmds.button(w=33, h=26, l='1', c='Wait')
        cmds.setParent('..')
        cmds.rowLayout(nc=4, cw4=(101, 60, 38, 38))
        cmds.text(l='A/S Weight', w=100)
        cmds.floatField(v=0.05, h=26, w=50, pre=3, min=0, max=1)
        cmds.button(w=38, h=26, l='+', c='Wait')
        cmds.button(w=38, h=26, l='-', c='Wait')
        cmds.setParent('..')
        cmds.rowLayout(nc=4, cw4=(101, 60, 38, 38))
        cmds.text(l='M/D Weight', w=100)
        cmds.floatField(v=0.95, h=26, w=50, pre=3, min=0, max=1)
        cmds.button(w=38, h=26, l='*', c='Wait')
        cmds.button(w=38, h=26, l='/', c='Wait')
        cmds.setParent('..')

        #cmds.window(self.WeightToolUi, e=1, wh=(255, 500))
        cmds.showWindow(self.WeightToolUi)

    def spJobStart(self):
        if cmds.text('spJobVtxParent', q=1, ex=1):
            return
        cmds.text('spJobVtxParent', p='MaincL', vis=0)
        cmds.scriptJob(e=['Undo', '判断选择类型,加载谷歌列表'], p='spJobVtxParent')
        cmds.scriptJob(e=['SelectionChanged', '判断选择类型,加载谷歌列表'], p='spJobVtxParent')
        #cmds.scriptJob(e=['ToolChanger', '自毁'], p='spJobVtxParent')
        #cmds.scriptJob(uid=[self.Ui,'自毁']
        mel.eval('global proc dagMenuProc(string $parent, string $object){ \
                if(objectType($object) == "joint"){ \
                string $selCmd = "python (\\\"SelectInfluence(\'" + $object + "\')\\\")"; \
                menuItem -l "Select Influence" -ec true -c $selCmd -rp "N" -p $parent; \
                }else{ \
                menuItem -l "Object Mode" -ec true -c "python (\\\"WeightTool().refreshBoxChange(9)\\\");maintainActiveChangeSelectMode QAQ 0" -rp "E" -p $parent;}}' )

    def refreshBoxChange(self, force):
        if force == 9:
            if cmds.text('spJobVtxParent', q=1, ex=1):
                cmds.deleteUI('spJobVtxParent', ctl=1)
            mel.eval('source "dagMenuProc.mel"')
            cmds.iconTextCheckBox('refresh', e=1, v=0)
            return
        if not cmds.selectType(q=1, ocm=1, pv=1):
            if cmds.text('spJobVtxParent', q=1, ex=1):
                cmds.deleteUI('spJobVtxParent', ctl=1)
            mel.eval('source "dagMenuProc.mel"')
            cmds.iconTextCheckBox('refresh', e=1, v=0)
        else:
            self.spJobStart()
            cmds.iconTextCheckBox('refresh', e=1, v=1)
    
    def refreshJointList(self):
        if not cmds.selectType(q=1, ocm=1, pv=1):
            return
        sel = cmds.ls(sl=1, fl=1)
        if not sel:
            Om.MGlobal.displayError('Select Nothing')
            return
        selobj = cmds.ls(sl=1, o=1)[0]
        if cmds.menuItem('FImeunItem', q=1, cb=1):
            cmds.skinCluster(selobj, q=1, wi=1)
        else:
            cmds.skinCluster(selobj, q=1, inf=1)

    # # # # # # # # # #
    def copyVtxWeight(self):
        selVtx = cmds.filterExpand(cmds.ls(sl=1)[0], sm=[28, 31, 36, 40, 46])
        if not selVtx:
            Om.MGlobal.displayError('Not Selected Vtx')
            return
        selObj = cmds.ls(sl=1, o=1)[0]
        clusterName = mel.eval('findRelatedSkinCluster("%s")' %selObj)
        if not clusterName:
            Om.MGlobal.displayError('Select No Skin')
            return
        ValueList = cmds.skinPercent(clusterName, selVtx, q=1, v=1)
        wiTransList = cmds.skinPercent(clusterName, selVtx, q=1, ib=.000001, t=None)
        TransList = cmds.skinPercent(clusterName, selVtx, q=1, t=None)
        '''   #倒序循环
        for i in range(len(ValueList)-1, -1, -1):
            if ValueList[i] < .0001:
                del ValueList[i], TransList[i]
        '''
        self.vtxWeightInfo = [clusterName, wiTransList, TransList, ValueList]
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
                    Om.MGlobal.displayError('Joint are different')
                    return
        tvList = []
        for i in range(len(self.vtxWeightInfo[2])):
            tvList.append((self.vtxWeightInfo[2][i], self.vtxWeightInfo[3][i]))
        #print(tvList)
        for i in selVtx:
            exec('cmds.skinPercent("%s", "%s", nrm=0, zri=0, tv=%s)' %(clusterName, i, tvList))
    # # # # # # # # # #


class DisplayYes():   #报绿

    def __init__(self):
        self.gCommandLine = mel.eval('$tmp = $gCommandLine')

    def showMessage(self, message):
        widget = shiboken2.wrapInstance(long(Omui.MQtUtil.findControl(self.gCommandLine)), QtWidgets.QWidget)
        widget.findChild(QtWidgets.QLineEdit).setStyleSheet('background-color:rgb(10,200,15);' + 'color:black;')
        cmds.select('time1', r=1)
        WeightTool().refreshBoxChange(9)
        cmds.text('spJobReLine', p='MaincL', vis=0)
        cmds.scriptJob(e=['SelectionChanged', 'DisplayYes().resetLine()'], p='spJobReLine')
        Om.MGlobal.displayInfo(message)

    def resetLine(self):
        cmds.deleteUI('spJobReLine', ctl=1)
        cmds.deleteUI(self.gCommandLine.rsplit('|', 1)[0])
        mel.eval('source "initCommandLine.mel"')


class LTools():

    def __init__(self):
        pass

    def createSelect(self):
        selvtx = cmds.ls(sl=1)
        selobj = cmds.ls(sl=1, o=1)[0]
        cluWs = cmds.getAttr(cmds.cluster(n='_tempClu_')[1] + 'Shape.origin')[0]
        Curname = cmds.circle(n='_selectCur_')[0]
        cmds.setAttr(Curname + '.translate', cmds.polyEvaluate(selobj, b=1)[0][1] + 1, cluWs[1], cluws[2])
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
                valueList = cmds.skinPercent(clusterName, i, ib=.000001, q=1, v=1)
                transList = cmds.skinPercent(clusterName, i, ib=.000001, q=1, t=None)
                tvList = []
                for u in range(len(valueList)):
                    tvList.append([transList[u], valueList[u]])
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


WeightTool().WeightToolUi()
