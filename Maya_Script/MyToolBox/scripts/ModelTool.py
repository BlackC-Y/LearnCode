# -*- coding: UTF-8 -*-
from maya import cmds, mel
from maya import OpenMayaUI as OmUI
from maya.api import OpenMaya as om
from PySide2.QtWidgets import QPushButton
import shiboken2
from MyToolBox import apiundo

from .Utils import QtStyle
from .DisplayYes import *

from functools import partial
import hashlib


class SymmetryTool_BbBB():

    def ToolUi(self, layout=0):
        Ver = 0.12
        self.UiName = "SymmetryTool_BbBB"
        if cmds.window(self.UiName, q=1, ex=1):
            cmds.deleteUI(self.UiName)
        if not layout:
            cmds.window(self.UiName, title="Symmetry %s" %Ver, s=1, mb=1, tlb=1, bgc=QtStyle.backgroundColor)
        cmds.columnLayout(rs=3, cat=('both', 2), cw=230, adj=1)
        cmds.rowLayout(nc=4, adj=4)
        cmds.radioButtonGrp('AxisRB_%s' %self.UiName, nrb=3, l1='X', l2='Y', l3='Z', sl=1, cw3=(35, 35, 35))
        cmds.checkBox('spaceCB_%s' %self.UiName, l=u'物体轴向', v=1, 
                      onc="cmds.checkBox('spaceCB_%s', e=1, l=u'物体轴向')" %self.UiName, ofc="cmds.checkBox('spaceCB_%s', e=1, l=u'世界轴向')" %self.UiName)
        #cmds.setParent('..')
        #cmds.rowLayout(nc=2, adj=2)
        cmds.text(l=u'容差值', w=50)
        cmds.floatField('toleranceValue_%s' %self.UiName, min=0.0001, value=.001)
        cmds.setParent('..')
        cmds.separator()
        _ToolButtonList = []
        cmds.rowLayout(nc=2, adj=2)
        _ToolButtonList.append(cmds.button(l=u'加载默认模型', w=155, c=lambda *args: self.loadBaseModel()))
        cmds.text('BaseMeshText_%s' %self.UiName, al='center', l='', h=24, bgc=(.251, .251, .251))
        self.BaseModel = None
        cmds.setParent('..')
        cmds.rowLayout(nc=2, cw2=(155, 155), ct2=('both', 'both'))
        _ToolButtonList.append(cmds.button(l=u'检查对称', c=lambda *args: ModelUtils_BbBB.checkSymmetry(
                axis=cmds.radioButtonGrp('AxisRB_%s' %self.UiName, q=1, sl=1)-1, 
                tol=cmds.floatField('toleranceValue_%s' %self.UiName, q=1, v=1), 
                space=self.getSpace()
                )))
        cmds.popupMenu()
        cmds.menuItem('trySymCB_%s' %self.UiName, l=u'尝试匹配对称', cb=0)
        _ToolButtonList.append(cmds.button(l=u'选择有移动的点', c=lambda *args: self.selectMovedVertex()))
        cmds.setParent('..')
        cmds.rowLayout(nc=2, cw2=(155, 155), ct2=('both', 'both'))
        _ToolButtonList.append(cmds.button(l=u'镜像模型', c=lambda *args: self.mirror_flipSelMesh()))
        cmds.popupMenu()
        cmds.menuItem(l=u"从负轴向正轴镜像", c=lambda *args: self.mirror_flipSelMesh(NtP=1))
        _ToolButtonList.append(cmds.button(l=u'翻转模型', c=lambda *args: self.mirror_flipSelMesh(flip=1)))
        cmds.setParent('..')

        for i in _ToolButtonList:
            shiboken2.wrapInstance(int(OmUI.MQtUtil.findControl(i)), QPushButton).setStyleSheet(QtStyle.QButtonStyle(height=26))

        if not layout:
            cmds.showWindow()

    def loadBaseModel(self):
        #thread = Thread(target=ModelUtils_BbBB.checkSymmetry,args=(*))
        #thread.start()
        #thread.join()
        slList = cmds.ls(sl=1)
        if not slList:
            cmds.text('BaseMeshText_%s' %self.UiName, e=1, l='')
            self.BaseModel = None
            om.MGlobal.displayError(u'什么都没选 这让我很难办啊')
            return
        self.PosIdList, self.NegIdList = ModelUtils_BbBB.checkSymmetry(
                cmds.radioButtonGrp('AxisRB_%s' %self.UiName, q=1, sl=1) - 1, 
                cmds.floatField('toleranceValue_%s' %self.UiName, q=1, v=1), 
                self.getSpace(), 
                cmds.menuItem('trySymCB_%s' %self.UiName, q=1, cb=1))
        cmds.text('BaseMeshText_%s' %self.UiName, e=1, l=slList[0])
        self.BaseModel = om.MGlobal.getActiveSelectionList()

    def selectMovedVertex(self, result=0):
        selMSList = om.MGlobal.getActiveSelectionList()
        selMSList.merge(self.BaseModel)
        if not selMSList.length() == 2:
            om.MGlobal.displayError(u'请选择模型')
            return
        
        origMFnMesh = om.MFnMesh(selMSList.getDagPath(0)).getPoints(self.getSpace())
        selMFnMesh = om.MFnMesh(selMSList.getDagPath(1)).getPoints(self.getSpace())
        movedVtx = []
        for i, v in enumerate(selMFnMesh):
            if v != origMFnMesh[i]:
                movedVtx.append(i)
        if result:
            return movedVtx
        selObj = selMSList.getSelectionStrings()[0]
        cmds.select(['%s.vtx[%s]' %(selObj, i) for i in movedVtx], r=1)

    def mirror_flipSelMesh(self, flip=0, NtP=0):
        selMSList = om.MGlobal.getActiveSelectionList()
        if not self.BaseModel or not selMSList.length():
            return
        Axis = cmds.radioButtonGrp('AxisRB_%s' %self.UiName, q=1, sl=1) - 1
        PosIdList, NegIdList = self.PosIdList, self.NegIdList

        objMFnMesh = om.MFnMesh(selMSList.getDagPath(0))
        allPoints = objMFnMesh.getPoints()
        apiundo.commit(undo=partial(objMFnMesh.setPoints, om.MPointArray(allPoints)))
        #inverMatrix = om.MMatrix.kIdentity.setElement(Axis, Axis, -1)
        moveId = self.selectMovedVertex(1)
        if not moveId:
            return
        moveId = set(moveId)

        if NtP:
            PosIdList, NegIdList = NegIdList, PosIdList
        if flip:
            for p, n in zip(PosIdList, NegIdList):
                if p in moveId or n in moveId:
                #if moveId.intersection({p, n}):
                    aPoint = om.MPoint(allPoints[p])
                    bPoint = om.MPoint(allPoints[n])
                    aPoint[Axis] = -aPoint[Axis]
                    bPoint[Axis] = -bPoint[Axis]
                    allPoints[p], allPoints[n] = bPoint, aPoint
                    #allPoints[p], allPoints[n] = om.MPoint(allPoints[n]) * inverMatrix, om.MPoint(allPoints[p]) * inverMatrix
        else:
            for p, n in zip(PosIdList, NegIdList):
                if p in moveId:
                    aPoint = om.MPoint(allPoints[p])
                    aPoint[Axis] = -aPoint[Axis]
                    allPoints[n] = aPoint
        objMFnMesh.setPoints(allPoints)

    def getSpace(self):
        if cmds.checkBox('spaceCB_%s' %self.UiName, q=1, v=1):
            return 2
        else:
            return 4
    

class BlendShapeTool_BbBB():

    @staticmethod
    def reSetBsTargetUi(layout=0):
        Ui = 'reSetBsTarget_Ui'
        if cmds.window(Ui, q=1, ex=1):
            cmds.deleteUI(Ui)
        if not layout:
            cmds.window(Ui, t=Ui, rtf=1, mb=1, tlb=1, wh=(300, 85), bgc=QtStyle.backgroundColor)
        cmds.columnLayout(cat=('both', 2), rs=2, cw=300, adj=1)
        cmds.textFieldButtonGrp('%s_BsTarget' %Ui, l=u'Bs目标', bl=u'选择', adj=2, ed=0, cw3=[40, 200, 60], bc=lambda *args: select())
        shiboken2.wrapInstance(int(OmUI.MQtUtil.findControl(
            cmds.button(l='Run', w=255, c=lambda *args: doIt(cmds.textFieldButtonGrp('%s_BsTarget' %Ui, q=1, tx=1)))
                )), QPushButton).setStyleSheet(QtStyle.QButtonStyle(height=26))
        
        shiboken2.wrapInstance(int(OmUI.MQtUtil.findControl('%s_BsTarget' %Ui)), QPushButton).setStyleSheet(QtStyle.QButtonStyle(height=26))
        def select():
            slBs = cmds.ls(sl=1, typ='blendShape')
            if not slBs:
                return
            slAttr = cmds.channelBox('mainChannelBox', q=1, sha=1)[0]
            cmds.textFieldButtonGrp('%s_BsTarget' %Ui, e=1, tx='%s.%s' %(slBs[0], slAttr))

        if not layout:
            cmds.showWindow(Ui)

        def doIt(data):
            slList = cmds.ls(sl=1, typ='transform')
            if not slList or not data:
                om.MGlobal.displayError(u'未选择模型')
                return
            data = data.split('.', 1)
            for item in cmds.getAttr('%s.w' %data[0], mi=1):
                if data[1] == cmds.aliasAttr('%s.w[%s]' %(data[0], item), q=1):
                    break
            bsDataAttr = '%s.inputTarget[%s].inputTargetGroup[%s].inputTargetItem[6000].inputGeomTarget' %(data[0], 0, item)
            cmds.connectAttr('%s.outMesh' %slList[0], bsDataAttr, f=1)
            cmds.refresh()
            cmds.disconnectAttr('%s.outMesh' %slList[0], bsDataAttr)

    @staticmethod
    def checkSameModelToolUi(layout=0):
        Ui = 'checkSameModelTool_Ui'
        if cmds.window(Ui, q=1, ex=1):
            cmds.deleteUI(Ui)
        if not layout:
            cmds.window(Ui, t=Ui, rtf=1, mb=1, tlb=1, wh=(300, 85), bgc=QtStyle.backgroundColor)
        cmds.columnLayout(cat=('both', 2), rs=2, cw=300, adj=1)
        cmds.textFieldButtonGrp('%s_BsTarget' %Ui, l=u'基准', bl=u'选择', adj=2, ed=0, cw3=[40, 200, 60], bc=lambda *args: select())
        shiboken2.wrapInstance(int(OmUI.MQtUtil.findControl(
            cmds.button(l='Run', w=255, c=lambda *args: doIt(cmds.textFieldButtonGrp('%s_BsTarget' %Ui, q=1, tx=1)))
                )), QPushButton).setStyleSheet(QtStyle.QButtonStyle(height=26))
        
        shiboken2.wrapInstance(int(OmUI.MQtUtil.findControl('%s_BsTarget' %Ui)), QPushButton).setStyleSheet(QtStyle.QButtonStyle(height=26))
        def select():
            sl = cmds.ls(sl=1, typ='transform')
            if not sl:
                return
            cmds.textFieldButtonGrp('%s_BsTarget' %Ui, e=1, tx=sl[0])

        if not layout:
            cmds.showWindow(Ui)
        
        def doIt(Name):
            baseSel = om.MGlobal.getSelectionListByName(Name)
            slItList = om.MItSelectionList(om.MGlobal.getActiveSelectionList())
            baseFnMesh = om.MFnMesh(baseSel.getDagPath(0))
            baseMd5 = hashlib.md5(str(baseFnMesh.getPoints()).encode("utf-8")).hexdigest()
            
            sameList = om.MSelectionList()
            while not slItList.isDone():
                oneFnMesh = om.MFnMesh(slItList.getDagPath())
                oneMd5 = hashlib.md5(str(oneFnMesh.getPoints()).encode("utf-8")).hexdigest()
                if oneMd5 == baseMd5:
                    sameList.add(slItList.getDagPath())
                slItList.next()
            om.MGlobal.setActiveSelectionList(sameList)

    @staticmethod
    def ExBsModelToolUi(layout=0):
        Ui = 'ExBsModelTool_Ui'
        if cmds.window(Ui, q=1, ex=1):
            cmds.deleteUI(Ui)
        if not layout:
            cmds.window(Ui, t=Ui, rtf=1, mb=1, tlb=1, wh=(300, 85), bgc=QtStyle.backgroundColor)
        cmds.columnLayout(cat=('both', 2), rs=2, cw=300, adj=1)
        cmds.textFieldButtonGrp('%s_MeshTarget' %Ui, l=u'被复制模型', bl=u'选择', adj=2, ed=0, cw3=[60, 180, 60], bc=lambda *args: select(0))
        cmds.textFieldButtonGrp('%s_BsNodeTarget' %Ui, l=u'Bs节点', bl=u'选择', adj=2, ed=0, cw3=[60, 180, 60], bc=lambda *args: select(1))
        shiboken2.wrapInstance(int(OmUI.MQtUtil.findControl(
            cmds.button(l='Run', w=255, c=lambda *args: doIt(cmds.textFieldButtonGrp('%s_MeshTarget' %Ui, q=1, tx=1), 
                                                             cmds.textFieldButtonGrp('%s_BsNodeTarget' %Ui, q=1, tx=1)))
                )), QPushButton).setStyleSheet(QtStyle.QButtonStyle(height=26))
        shiboken2.wrapInstance(int(OmUI.MQtUtil.findControl('%s_MeshTarget' %Ui)), QPushButton).setStyleSheet(QtStyle.QButtonStyle(height=26))
        shiboken2.wrapInstance(int(OmUI.MQtUtil.findControl('%s_BsNodeTarget' %Ui)), QPushButton).setStyleSheet(QtStyle.QButtonStyle(height=26))
        def select(mode):
            if mode:
                sl = cmds.ls(sl=1, typ='blendShape')
                if not sl:
                    return
                cmds.textFieldButtonGrp('%s_BsNodeTarget' %Ui, e=1, tx=sl[0])
            else:
                sl = cmds.ls(sl=1, typ='transform')
                if not sl:
                    return
                cmds.textFieldButtonGrp('%s_MeshTarget' %Ui, e=1, tx=sl[0])

        if not layout:
            cmds.showWindow(Ui)

        def doIt(mesh, bsNode):
            modbbox = cmds.xform(mesh, q=1, bb=1)
            cmds.setAttr('%s.envelope' %bsNode, 1)
            saveGrp = cmds.group(n='ExtBs_Grp', em=1, w=1)
            for index, value in enumerate(cmds.getAttr('%s.w' %bsNode, mi=1)):
                try:
                    cmds.setAttr('%s.w[%s]' %(bsNode, value), 1)
                except:
                    continue
                extName = cmds.duplicate(mesh, n=cmds.aliasAttr('%s.w[%s]' %(bsNode, value), q=1))[0]
                cmds.parent(extName, saveGrp)
                cmds.setAttr('%s.tx' %extName, (index + 1) * abs(modbbox[0] - modbbox[3]) / 2)
                cmds.setAttr('%s.w[%s]' %(bsNode, value), 0)


class ModelUtils_BbBB():

    @staticmethod
    def checkSymmetry(axis=0, tol=0.001, space=2, trySym=0):
        """
        axis: 对称轴 X-0/Y-1/Z-2
        tol: 坐标容差值
        space: 位置空间 2-物体/4-世界
        trySym: 将不对称的点强制匹配对应点
        """
        import time
        st = time.time()
        selMSList = om.MGlobal.getActiveSelectionList()
        if not selMSList.length():
            om.MGlobal.displayError(u'什么都没选 这让我很难办啊')
            return
        if not axis in (0, 1, 2):
            om.MGlobal.displayError(u'轴向错误')
            return

        objDagPath = selMSList.getDagPath(0)  # 存储所选物体的路径
        objObject = selMSList.getDependNode(0)  # 存储所选物体的组件的列表
        objMFnMesh = om.MFnMesh(objDagPath)
        selMSList.add('%s.vtx[0:%s]' %(objDagPath.partialPathName(), objMFnMesh.numVertices-1))   #线程不支持.vtx[]形式
        comDagPath, comObject = selMSList.getComponent(1)
        PositiveList = []
        NegativeList = []
        allNegIdList = []
        symmetryMSList = om.MSelectionList()

        vertIter = om.MItMeshVertex(objObject)
        while not vertIter.isDone():
            loc = vertIter.position(space)
            if loc[axis] > tol:
                PositiveList.append([vertIter.currentItem(), loc, vertIter.index()])
            elif loc[axis] < -tol:
                allNegIdList.append(vertIter.index())
                #NegativeList.append([vertIter.currentItem(), loc, vertIter.index()])
            else:
                symmetryMSList.add((objDagPath, vertIter.currentItem()))
            vertIter.next()
        
        """import bisect 基于列表元素的 应处位置判断"""
        #def rangeCheck(x, y, tol):   #纯对比速度快 但不是纯距离实际偏移更大
        #    return 0 if x <= y - tol or x >= y + tol else 1
        
        gMainProgressBar = mel.eval('$tmp = $gMainProgressBar')
        cmds.progressBar(gMainProgressBar, e=1, bp=1, st=u'检查中...', max=100)
        oneInAll = objMFnMesh.numVertices/200.0
        cycle = 1
        PosIdList = []
        NegIdList = []
        '''
        for i, pos in enumerate(PositiveList):
            nowLocP = pos[1]
            for neg in NegativeList:
                nowLocN = om.MPoint(neg[1])
                nowLocN[axis] = -nowLocN[axis]
                if nowLocP.isEquivalent(nowLocN, tol):
                if rangeCheck(nowLocP[axis], -nowLocN[axis], tol):
                    if rangeCheck(nowLocP[(axis+1)%3], nowLocN[(axis+1)%3], tol):
                        if rangeCheck(nowLocP[(axis+2)%3], nowLocN[(axis+2)%3], tol):
                            PosIdList.append(pos[2])
                            NegIdList.append(neg[2])
                            symmetryMSList.add((objDagPath, pos[0]))
                            symmetryMSList.add((objDagPath, neg[0]))
                            break
            if i > oneInAll * cycle:
                cmds.progressBar(gMainProgressBar, e=1, s=1)
                cycle += 1
        '''
        allPointLoc = objMFnMesh.getPoints(space)
        for i, pos in enumerate(PositiveList):
            nowLocP = om.MPoint(pos[1])
            nowLocP[axis] = -nowLocP[axis]
            clostLoc, closeFaceID = objMFnMesh.getClosestPoint(nowLocP, space)
            clostPointList = objMFnMesh.getPolygonVertices(closeFaceID)
            distance = [nowLocP.distanceTo(allPointLoc[index]) for index in clostPointList]
            minDis = min(distance)
            if minDis < tol:
                clostPointID = clostPointList[distance.index(minDis)]
                PosIdList.append(pos[2])
                NegIdList.append(clostPointID)
                symmetryMSList.add((objDagPath, pos[0]))
                symmetryMSList.add('%s.vtx[%s]' %(objDagPath.partialPathName(), clostPointID))
            if i > oneInAll * cycle:
                cmds.progressBar(gMainProgressBar, e=1, s=1)
                cycle += 1
        
        if trySym:
            noSymNegList = set(allNegIdList).difference(set(NegIdList))
            for i in noSymNegList:
                iLoc = om.MPoint(allPointLoc[i])
                iLoc[axis] = -iLoc[axis]
                clostLoc, closeFaceID = objMFnMesh.getClosestPoint(iLoc, space)
                clostPointList = objMFnMesh.getPolygonVertices(closeFaceID)
                distance = [iLoc.distanceTo(allPointLoc[index]) for index in clostPointList]
                clostPointID = clostPointList[distance.index(min(distance))]
                PosIdList.append(clostPointID)
                NegIdList.append(i)

        #symmetryMSList.merge(PositiveMSList)
        symmetryMSList.toggle(comDagPath, comObject)
        cmds.progressBar(gMainProgressBar, e=1, ep=1)
        print(time.time()-st)
        if symmetryMSList.length():
            om.MGlobal.displayWarning(u'已选择不对称的点')
            om.MGlobal.setActiveSelectionList(symmetryMSList)
            #om.MGlobal.selectCommand(symmetryMSList) >2019版本
        else:
            DisplayYes().showMessage(u'恭喜 模型是对称的')
        return PosIdList, NegIdList
    
    def invertShape_Bs():
        try:
            cmds.loadPlugin('invertShape.mll', qt=1)
        except RuntimeError:
            om.MGlobal.displayWarning(u'这个Maya中缺少必要插件, 修型功能将无法使用!')
        cmds.invertShape(orig, sel)
    
#SymmetryTool_BbBB().ToolUi()
