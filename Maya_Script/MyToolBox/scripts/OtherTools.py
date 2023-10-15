# -*- coding: UTF-8 -*-
from maya import cmds, mel
from maya.api import OpenMaya as om
import os
import re


class otherTools():

    @staticmethod
    def resetWindowLoc():
        """
        重置打开窗口的位置
        """
        try:
            from PySide2.QtWidgets import QApplication
        except:
            from PySide.QtGui import QApplication
        for i in QApplication.topLevelWidgets():
            try:
                i.move(100, 100)
            except:
                pass
        for i in cmds.lsUI(type='window'):
            try:
                cmds.window(i, e=1, tlc=[100, 100])
            except:
                pass
    
    @staticmethod
    def selectSorted():
        """
        选择组，按照内容的结尾编号，在大纲中进行排序
        """
        slList = cmds.ls(sl=1)
        childList = cmds.listRelatives(slList[0], c=1, s=0, f=1)
        numList = [int(re.search(r'\d*$', i).group()) for i in childList]
        numList, childList = zip(*sorted(zip(numList, childList)))
        cmds.parent(childList, w=1)
        cmds.parent([i.rsplit('|', i)[-1] for i in childList], slList[0])

    @staticmethod
    def constraintFromLast(mode):
        """
        mode: 0-3分别为父子/点/旋转/缩放
        """
        sllist = cmds.ls(sl=1)
        if mode == 0:
            for i in sllist[:-1]:
                cmds.parentConstraint(sllist[-1], i, mo=1, w=1)
        elif mode == 1:
            for i in sllist[:-1]:
                cmds.pointConstraint(sllist[-1], i, mo=1, w=1)
        elif mode == 2:
            for i in sllist[:-1]:
                cmds.orientConstraint(sllist[-1], i, mo=1, w=1)
        elif mode == 3:
            for i in sllist[:-1]:
                cmds.scaleConstraint(sllist[-1], i, mo=1, w=1)

    @staticmethod
    def createLocator():
        alist = cmds.ls(sl=1, fl=1)
        for i in alist:
            txyz = cmds.xform(i, q=1, ws=1, t=1)
            cmds.setAttr(cmds.spaceLocator(n=i+'_loc')[0]+'.translate', txyz[0], txyz[1], txyz[2])

    @staticmethod
    def polytoCurve():
        blist = cmds.ls(sl=1)
        for i in blist:
            vnum = cmds.polyEvaluate(i, v=1)
            for v in range(vnum):
                enum = cmds.ls(cmds.polyListComponentConversion('%s.vtx[%s]' %(i, v), fv=1, ff=1, fuv=1, fvf=1, te=1), fl=1)
                if len(enum) == 4:
                    break
            arclen = []
            for e in enum:
                earclen = 0.0
                for el in cmds.polySelectSp(e, q=1, loop=1):
                    earclen += cmds.arclen(el)
                arclen.append(earclen)
            cmds.polySelectSp(enum[arclen.index(max(arclen))], loop=1)
            cname = cmds.rename(cmds.polyToCurve(ch=0, form=2, degree=3), i + '_Cur')
            if cmds.xform('%s.cv[0]', q=1, ws=1, t=1)[1] %cname < cmds.xform('%s.cv[%s]' %(cname, cmds.getAttr("%s.controlPoints", size=1) %cname), q=1, ws=1, t=1)[1]:
                cmds.reverseCurve(cname, ch=0, rpo=1)

    @staticmethod
    def xiuxingJoint():
        Raxial = 'Y'     #Z
        Taxial = 'z'     #y
        joint = cmds.ls(sl=1, type="joint")[0]
        cmds.select(cl=1)
        blendJoint = cmds.joint(n=joint+"_BlendJoint")
        cmds.delete(cmds.parentConstraint(joint, blendJoint, w=1))
        cmds.parent(blendJoint, joint)
        cmds.setAttr(blendJoint+".rotate", 0, 0, 0)
        cmds.setAttr(blendJoint+".jointOrient", 0, 0, 0)
        cmds.select(cl=1)
        blendJointEnd = cmds.joint(n=joint+"_BlendJointEnd")
        cmds.delete(cmds.parentConstraint(joint, blendJointEnd, w=1))
        cmds.parent(blendJointEnd, blendJoint)
        cmds.setAttr(blendJointEnd+".rotate", 0, 0, 0)
        cmds.setAttr(blendJointEnd+".jointOrient", 0, 0, 0)
        cmds.select(cl=1)
        cmds.addAttr(blendJointEnd, ln="BlendJointScale", at='double', min=0, dv=1)
        cmds.addAttr(blendJointEnd, ln="vectorV", at='double', dv=0)
        cmds.setAttr(blendJointEnd+".BlendJointScale", e=1, keyable=1)
        cmds.setAttr(blendJointEnd+".vectorV", -1)
        cmds.setAttr(blendJointEnd+".BlendJointScale", 0.05)
        mathNode = cmds.createNode("multiplyDivide")
        cmds.connectAttr(joint+".rotate", mathNode+".input1", f=1)
        cmds.setAttr(mathNode+".input2", -.5, -.5, -.5)
        cmds.connectAttr(mathNode+".output", blendJoint+".rotate", f=1)
        floatMathA = cmds.createNode("floatMath")
        cmds.setAttr(floatMathA+".operation", 2)
        floatMathB = cmds.createNode("floatMath")
        cmds.setAttr(floatMathB+".operation", 2)
        floatMathC = cmds.createNode("floatMath")
        cmds.connectAttr(blendJointEnd+".BlendJointScale", floatMathA+".floatB", f=1)
        cmds.connectAttr(blendJointEnd+".vectorV", floatMathA+".floatA", f=1)
        cmds.setAttr(floatMathC+".floatB", 0.2)
        cmds.connectAttr(floatMathA + ".outFloat", floatMathB + ".floatB", f=1)
        cmds.connectAttr(floatMathB + ".outFloat", floatMathC + ".floatA", f=1)
        cmds.connectAttr(floatMathC + ".outFloat", blendJointEnd + ".t" + Taxial, f=1)
        cmds.connectAttr(joint + ".rotate" + Raxial, floatMathB + ".floatA", f=1)

    @staticmethod
    def xiuxingJointHang():
        jot_name = cmds.ls(sl=1, typ="joint")
        jot_bs_name1 = cmds.joint(n=(jot_name[0] + "_bs"), rad=3)
        jot_bs_name2 = cmds.joint(n=(jot_name[0] + "_bsend"), rad=3)
        jot_rotY = cmds.getAttr(jot_name[0] + ".jointOrientY")
        jot_rotZ = cmds.getAttr(jot_name[0] + ".jointOrientZ")
        jot_attibuteY = [".tx", ".ty", ".rx", ".ry", ".rz", ".sx", ".sy", ".sz"]
        jot_attibuteZ = [".tx", ".tz", ".rx", ".ry", ".rz", ".sx", ".sy", ".sz"]
        cmds.select(cl=1)
        cnmulti1 = cmds.createNode('multiplyDivide')
        cnmulti2 = cmds.createNode('multiplyDivide')
        cnmulti3 = cmds.createNode('addDoubleLinear')
        cnmulti4 = cmds.createNode('multiplyDivide')
        cmds.connectAttr(jot_name[0] + ".rotate", cnmulti1 + ".input1", f=1)
        cmds.setAttr(cnmulti1 + ".input2", -.5, -.5, -.5)
        cmds.connectAttr(cnmulti1 + ".output", jot_bs_name1 + ".rotate", f=1)
        if abs(jot_rotY) > abs(jot_rotZ):
            cmds.connectAttr(cnmulti1 + ".input1Y", cnmulti4 + ".input1X", f=1)
            cmds.setAttr(cnmulti4 + ".input2X", 0.01)
            cmds.connectAttr(cnmulti4 + ".outputX", cnmulti2 + ".input1X", f=1)
            cmds.addAttr('jot_bs_name2', ln="BS_Long", at='double', min=-10, max=10, dv=0)
            cmds.setAttr(jot_bs_name2 + ".BS_Long", e=1, keyable=1)
            cmds.connectAttr(jot_bs_name2 + ".BS_Long", cnmulti2 + ".input2X", f=1)
            cmds.addAttr('jot_bs_name2', ln="mumu", at='double')
            cmds.connectAttr(cnmulti2 + ".outputX", cnmulti3 + ".input1", f=1)
            cmds.connectAttr(jot_bs_name2 + ".mumu", cnmulti3 + ".input2", f=1)
            cmds.connectAttr(cnmulti3 + ".output", jot_bs_name2 + ".translateZ", f=1)
            if jot_rotY > 0:
                cmds.setAttr(jot_bs_name2 + ".mumu", 0.5)
            elif jot_rotY < 0:
                cmds.setAttr(jot_bs_name2 + ".mumu", -0.5)
            for i in range(7):
                cmds.setAttr(jot_bs_name2 + jot_attibuteY[i], lock=1, keyable=0, channelBox=0)
        elif abs(jot_rotZ) > abs(jot_rotY):
            cmds.connectAttr(cnmulti1 + ".input1Z", cnmulti4 + ".input1X", f=1)
            cmds.setAttr(cnmulti4 + ".input2X", 0.01)
            cmds.connectAttr(cnmulti4 + ".outputX", cnmulti2 + ".input1X", f=1)
            cmds.addAttr(jot_bs_name2, ln="BS_Long", at='double', min=-10, max=10, dv=1)
            cmds.setAttr(jot_bs_name2 + ".BS_Long", e=1, keyable=0, channelBox=1)
            cmds.connectAttr(jot_bs_name2 + ".BS_Long", cnmulti2 + ".input2X", f=1)
            cmds.addAttr(jot_bs_name2, ln="mumu", at='double')
            cmds.connectAttr(cnmulti2 + ".outputX", cnmulti3 + ".input1", f=1)
            cmds.connectAttr(jot_bs_name2 + ".mumu", cnmulti3 + ".input2", f=1)
            cmds.connectAttr(cnmulti3 + ".output", jot_bs_name2 + ".translateY", f=1)
            if jot_rotZ < 0:
                cmds.setAttr(jot_bs_name2 + ".mumu", -0.5)
            elif jot_rotZ > 0:
                cmds.setAttr(jot_bs_name2 + ".mumu", 0.5)
            for i in range(7):
                cmds.setAttr(jot_bs_name2 + jot_attibuteZ[i], lock=1, keyable=0, channelBox=0)

    @staticmethod
    def TransferUV():
        dobj = cmds.ls(sl=1)
        if cmds.polyEvaluate(dobj[0], v=1) != cmds.polyEvaluate(dobj[1], v=1):
            dupobj = cmds.duplicate(dobj[1], rr=1)
            cmds.transferAttributes(dobj[0], dupobj, pos=0, nml=0, uvs=2, col=2, spa=0, sus="map1", tus="map1", sm=3, fuv=0, clb=1)
            cmds.delete(dupobj, ch=1)
            cmds.polyTransfer(dobj[1], uv=1, ao=dupobj[0])
            cmds.delete(dupobj)
        else:
            cmds.polyTransfer(dobj[1], uv=1, ao=dobj[0])

    @staticmethod
    def createFollicleOnsurface_ToolUi():
        ui = 'ToolsBoxUI3'
        try:
            cmds.deleteUI(ui)
        except:
            pass
        cmds.window(ui, tlb=1, t='createFollicleOnface')
        cmds.columnLayout(cat=("both", 2), columnWidth=180, rowSpacing=3)
        cmds.textFieldGrp('UI3nameTextFieldGrp', l=u'名称', h=28, cw2=(50, 100))
        cmds.intFieldGrp('UI3numIntFieldGrp', l=u'数量', h=28, cw2=(50, 100))
        cmds.flowLayout(columnSpacing=5)
        cmds.checkBox('UI3JointcheckBox', l=u'创建骨骼', w=80)
        cmds.button('UI3RunButton', l="Run", h=28, w=80, 
                        c=lambda *args: createFollicleOnsurface(
                                cmds.textFieldGrp('UI3nameTextFieldGrp', q=1, tx=1),
                                cmds.intFieldGrp('UI3numIntFieldGrp', q=1, v1=1),
                                cmds.checkBox('UI3JointcheckBox', q=1, v=1))
        )
        cmds.setParent('..')
        cmds.showWindow(ui)

        def createFollicleOnsurface(name='', num='', joint=0):
            #UI
            shape = cmds.listRelatives(cmds.ls(sl=1)[0], s=1, type='nurbsSurface')
            if not shape:
                om.MGlobal.displayError(u'没选择曲面')
                return
            Follicle_Grp = name + "_foll_grp"
            Joint_Grp = name + "_Joint_grp"
            if cmds.ls(Follicle_Grp, typ='transform') or cmds.ls(Joint_Grp, typ='transform'):
                om.MGlobal.displayError(u'有重名毛囊或骨骼')
                return
            cmds.group(em=1, n=Follicle_Grp)
            if joint:
                cmds.group(em=1, n=Joint_Grp)
            
            follList = []
            for i in range(num):
                if i == num:
                    break
                follicS = cmds.createNode('follicle', n='%s_follShape' %name)
                follicT = cmds.listRelatives(follicS, p=1)[0]
                
                cmds.connectAttr("%s.local" %shape[0], "%s.inputSurface" %follicS, f=1)
                cmds.connectAttr("%s.worldMatrix[0]" %shape[0], "%s.inputWorldMatrix" %follicS, f=1)
                cmds.connectAttr("%s.outTranslate" %follicS, "%s.translate" %follicT, f=1)
                cmds.connectAttr("%s.outRotate" %follicS, "%s.rotate" %follicT, f=1)
                cmds.setAttr("%s.parameterV" %follicS, .5)
                cmds.setAttr("%s.parameterU" %follicS, i*1.0/(num-1))
                #cmds.parent(follicT, Follicle_Grp)
                if joint:
                    cmds.select(cl=1)
                    jointN = cmds.joint(n='%s%sJoint' %(name, i))
                    cmds.parentConstraint(follicT, jointN, weight=1)
                    #cmds.parent(jointN, Joint_Grp)
                follList.append([follicT, jointN])
            for i in follList:
                cmds.parent(i[0], Follicle_Grp)
                cmds.parent(i[1], Joint_Grp)
    
    @staticmethod
    def connectBsCommand():
        """
        打印出Bs现有连接的命令
        """
        slbs = cmds.ls(sl=1, typ='blendShape')
        if not slbs:
            om.MGlobal.displayError(u'未选择BS节点')
            return
        for i in cmds.getAttr('%s.w' %slbs[0], mi=1):
            connectInfo = cmds.listConnections('%s.w[%s]' %(slbs[0], i), c=1, d=0, p=1, scn=1)
            if connectInfo:
                print('connectAttr -r "%s" "%s";' %(connectInfo[1], connectInfo[0]))

    @staticmethod
    def removeUnknownPlugin():
        for i in cmds.unknownPlugin(q=1, l=1):
            cmds.unknownPlugin(i, r=1)

    @staticmethod
    def FixError_ToolUi():
        UiName = 'FixError_ToolUi'
        if cmds.window(UiName, q=1, ex=1):
            cmds.deleteUI(UiName)
        cmds.window(UiName, t='FixError', rtf=1, mb=1, tlb=1, wh=(300, 85))
        cmds.columnLayout(cat=('both', 2), rs=2, cw=300, adj=2)
        cmds.text(l=u'鼠标放在按钮上 查看使用说明', h=40, fn='fixedWidthFont')
        cmds.scrollLayout(hst=16, vsb=16)
        cmds.columnLayout(cat=('both', 2), rs=2, cw=290)
        cmds.button(l=u'大纲look爆红', c=lambda *args: FixRed_look(), 
                    ann=u'解决在大纲选择物体时Maya爆红"look"的问题')
        cmds.button(l=u'开关文件爆红', c=lambda *args: FixRed_uiConfigScriptNode(), 
                    ann=u'解决在打开文件或新建文件时爆红的问题\n请重开maya, 在打开问题文件时取消勾选右上角的"Execute script nodes"\n打开文件后运行此工具, 然后保存')
        cmds.button(l=u'创建模型不显示，修改材质报错', c=lambda *args: FixUnpublishLock(), 
                    ann=u'解锁文件中Unpublish的节点')
        cmds.showWindow(UiName)
    
        def FixRed_look():
            mel.eval('outlinerEditor -e -sec "" outlinerPanel1')

        def FixRed_uiConfigScriptNode():
            if cmds.ls('uiConfigurationScriptNode', typ='script'):
                cmds.delete('uiConfigurationScriptNode')

        def FixUnpublishLock():
            allObject = cmds.ls()
            allState = cmds.lockNode(allObject, q=1, lockUnpublished=1)
            if allState.count(True):
                [cmds.lockNode(allObject[i], lu=0, l=0) for i, v in enumerate(allState) if v]
            else:
                cmds.warning(u"没发现节点锁定情况")

    @staticmethod
    def cRivet(mode):

        def cLoc(mode, uV = .5, vV = .5):
            locName = 'rivet%s' %(len(cmds.ls('rivet*', typ='locator')) + 1)
            locN = cmds.spaceLocator(n=locName)[0]
            cmds.group(locN, n='%s_grp' %locN)
            if mode:
                cmds.addAttr(locN, ln='U', at='double', dv=0)
                cmds.addAttr(locN, ln='V', at='double', dv=0)
            else:
                cmds.addAttr(locN, ln='U', at='double', min=0, max=1, dv=0)
                cmds.addAttr(locN, ln='V', at='double', min=0, max=1, dv=0)
            cmds.setAttr('%s.U' %locN, e=1, keyable=1)
            cmds.setAttr('%s.U' %locN, uV)
            cmds.setAttr('%s.V' %locN, e=1, keyable=1)
            cmds.setAttr('%s.V' %locN, vV)
            return locN, '%s_grp' %locN
        
        slmesh = cmds.ls(sl=1, o=1, typ='mesh')
        slsurface = cmds.ls(sl=1, o=1, typ='nurbsSurface')
        if slmesh:
            twoEdge = cmds.filterExpand(sm=32)
            if len(twoEdge) != 2 or not twoEdge:
                om.MGlobal.displayError(u'需要选择两条模型线')
                return
            nCFME1 = cmds.createNode('curveFromMeshEdge', n='rivetCFME01')
            cmds.setAttr('%s.ei[0]' %nCFME1, int(twoEdge[0].split('[')[1].split(']')[0]))
            cmds.connectAttr('%s.w' %slmesh[0], '%s.im' %nCFME1, f=1)
            nCFME2 = cmds.createNode('curveFromMeshEdge', n='rivetCFME02')
            cmds.setAttr('%s.ei[0]' %nCFME2, int(twoEdge[1].split('[')[1].split(']')[0]))
            cmds.connectAttr('%s.w' %slmesh[0], '%s.im' %nCFME2, f=1)
            nLoft = cmds.createNode('loft', n='rivetLoft01')
            cmds.setAttr('%s.u' %nLoft, 1)
            cmds.connectAttr('%s.oc' %nCFME1, '%s.ic[0]' %nLoft, f=1)
            cmds.connectAttr('%s.oc' %nCFME2, '%s.ic[1]' %nLoft, f=1)
            if mode == 'follicle':
                locN, locgrpN = cLoc(0)
                nFollicle = cmds.createNode('follicle', p=locgrpN, n='%s_FollicleShape' %locN)
                cmds.setAttr('%s.visibility' %nFollicle, 0)
                cmds.setAttr('%s.sim' %nFollicle, 0)
                cmds.connectAttr('%s.U' %locN, '%s.pu' %nFollicle, f=1)
                cmds.connectAttr('%s.V' %locN, '%s.pv' %nFollicle, f=1)
                cmds.connectAttr('%s.os' %nLoft, '%s.is' %nFollicle, f=1)
            else:
                locN, locgrpN = cLoc(0)
                nPOSI = cmds.createNode('pointOnSurfaceInfo', n='rivetPOSI01')
                cmds.setAttr('%s.top' %nPOSI, 1)
                cmds.connectAttr('%s.U' %locN, '%s.u' %nPOSI, f=1)
                cmds.connectAttr('%s.V' %locN, '%s.v' %nPOSI, f=1)
                cmds.connectAttr('%s.os' %nLoft, '%s.is' %nPOSI, f=1)
        elif slsurface:
            onepoint = cmds.filterExpand(sm=41)
            if len(onepoint) != 1 or not onepoint:
                om.MGlobal.displayError(u'需要选择一个曲面点')
                return
            pointUV = re.findall(r'[[](.*?)[]]', onepoint[0])
            if mode == 'follicle':
                locN, locgrpN = cLoc(0, 1.0 / (cmds.getAttr('%s.mxu' %slsurface[0]) / float(pointUV[0])), 
                                                1.0 / (cmds.getAttr('%s.mxv' %slsurface[0]) / float(pointUV[1])))
                nFollicle = cmds.createNode('follicle', p=locgrpN, n='%s_FollicleShape' %locN)
                cmds.setAttr('%s.visibility' %nFollicle, 0)
                cmds.setAttr('%s.sim' %nFollicle, 0)
                cmds.connectAttr('%s.U' %locN, '%s.pu' %nFollicle, f=1)
                cmds.connectAttr('%s.V' %locN, '%s.pv' %nFollicle, f=1)
                cmds.connectAttr('%s.ws' %slsurface[0], '.is' %nFollicle, f=1)
            else:
                locN, locgrpN = cLoc(1, float(pointUV[0]), float(pointUV[1]))
                nPOSI = cmds.createNode('pointOnSurfaceInfo', n='rivetPOSI01')
                cmds.setAttr('%s.top' %nPOSI, 0)
                cmds.connectAttr('%s.U' %locN, '%s.u' %nPOSI, f=1)
                cmds.connectAttr('%s.V' %locN, '%s.v' %nPOSI, f=1)
                cmds.connectAttr('%s.ws' %slsurface[0], '%s.is' %nPOSI, f=1)
        else:
            om.MGlobal.displayError(u'需要选择 模型线 或者 曲面点')
            return
        
        if mode == 'follicle':
            cmds.connectAttr('%s.ot' %nFollicle, '%s.t' %locgrpN, f=1)
            cmds.connectAttr('%s.or' %nFollicle, '%s.r' %locgrpN, f=1)
        elif mode == 'Matrix':
            if not cmds.pluginInfo('decomposeMatrix', q=1, l=1):
                cmds.loadPlugin('matrixNodes', quiet=1)
            nFBFM = cmds.createNode('fourByFourMatrix', n='rivetFBFM01')
            cmds.connectAttr('%s.nx' %nPOSI, '%s.in00' %nFBFM, f=1)
            cmds.connectAttr('%s.ny' %nPOSI, '%s.in01' %nFBFM, f=1)
            cmds.connectAttr('%s.nz' %nPOSI, '%s.in02' %nFBFM, f=1)
            cmds.connectAttr('%s.tux' %nPOSI, '%s.in10' %nFBFM, f=1)
            cmds.connectAttr('%s.tuy' %nPOSI, '%s.in11' %nFBFM, f=1)
            cmds.connectAttr('%s.tuz' %nPOSI, '%s.in12' %nFBFM, f=1)
            cmds.connectAttr('%s.tvx' %nPOSI, '%s.in20' %nFBFM, f=1)
            cmds.connectAttr('%s.tvy' %nPOSI, '%s.in21' %nFBFM, f=1)
            cmds.connectAttr('%s.tvz' %nPOSI, '%s.in22' %nFBFM, f=1)
            cmds.connectAttr('%s.px' %nPOSI, '%s.in30' %nFBFM, f=1)
            cmds.connectAttr('%s.py' %nPOSI, '%s.in31' %nFBFM, f=1)
            cmds.connectAttr('%s.pz' %nPOSI, '%s.in32' %nFBFM, f=1)
            nDM = cmds.createNode('decomposeMatrix', n='rivetDM01')
            cmds.connectAttr('%s.output' %nFBFM, '%s.inputMatrix' %nDM, f=1)
            cmds.connectAttr('%s.outputTranslate' %nDM, '%s.t' %locgrpN, f=1)
            cmds.connectAttr('%s.outputRotate' %nDM, '%s.r' %locgrpN, f=1)
        elif mode == 'Aim':
            nAimC = cmds.createNode('aimConstraint', p=locgrpN, n='%s_AimConstraint1' %locN)
            cmds.setAttr('%s.tg[0].tw' %nAimC, 1)
            cmds.setAttr('%s.a' %nAimC, 0, 1, 0, type='double3')
            cmds.setAttr('%s.u' %nAimC, 0, 0, 1, type='double3')
            cmds.connectAttr('%s.n' %nPOSI, '%s.tg[0].tt' %nAimC, f=1)
            cmds.connectAttr('%s.tv' %nPOSI, '%s.wu' %nAimC, f=1)
            cmds.connectAttr('%s.p' %nPOSI, '%s.t' %locgrpN, f=1)
            cmds.connectAttr('%s.cr' %nAimC, '%s.r' %locgrpN, f=1)

    @staticmethod
    def AdvskinClusterLargeFix():
        for i in cmds.ls(sl=1, typ='joint'):
            mulMatrix = cmds.createNode('multMatrix')
            cmds.connectAttr('%s.worldMatrix[0]' %i, '%s.matrixIn[0]' %mulMatrix, f=1)
            cmds.connectAttr('DeformationSystem.worldInverseMatrix[0]', '%s.matrixIn[1]' %mulMatrix, f=1)
            skinC = cmds.listConnections('%s.worldMatrix[0]' %i, type='skinCluster', p=1)
            if skinC:
                for s in skinC:
                    cmds.connectAttr('%s.matrixSum' %mulMatrix, s, f=1)
        cmds.parentConstraint('Main', 'DeformationSystem', mo=1)
        cmds.connectAttr('DeformationSystem.t', 'Geometry.t', f=1)
        cmds.connectAttr('DeformationSystem.r', 'Geometry.r', f=1)
        cmds.connectAttr('DeformationSystem.s', 'Geometry.s', f=1)

    @staticmethod
    def IkFkSeamlessSwitch_ToolUi(layout=0):
        Ui = 'IkFkSeamlessSwitch_Ui'
        if cmds.window(Ui, q=1, ex=1):
            cmds.deleteUI(Ui)
        if not layout:
            cmds.window(Ui, t=Ui, rtf=1, mb=1, tlb=1, wh=(300, 85))
        cmds.columnLayout(cat=('both', 2), rs=2, cw=300, adj=1)
        cmds.button(l=u'默认Adv创建 (选择Adv的IKFK切换控制器)(可重建)', w=255, c=lambda *args: doAdv())
        cmds.separator(height=5, style='in')
        cmds.textFieldButtonGrp('%s_IFSwitchAttr' %Ui, l=u'IKFK切换属性', bl=u'选择', adj=2, ed=0, cw3=[100, 200, 60], bc=lambda *args: _select('_IFSwitchAttr'))
        cmds.textFieldButtonGrp('%s_IkPole' %Ui, l=u'Ik和极向量控制器', bl=u'选择', adj=2, ed=0, cw3=[100, 200, 60], bc=lambda *args: _select('_IkPole'))
        cmds.textFieldButtonGrp('%s_3FkCtrl' %Ui, l=u'顺序Fk控制器', bl=u'选择', adj=2, ed=0, cw3=[100, 200, 60], bc=lambda *args: _select('_3FkCtrl'))
        cmds.textFieldButtonGrp('%s_3SkinJoint' %Ui, l=u'顺序蒙皮骨骼', bl=u'选择', adj=2, ed=0, cw3=[100, 200, 60], bc=lambda *args: _select('_3SkinJoint'))
        cmds.button(l=u'创建', w=255, c=lambda *args: doIt(dataList))

        dataList = [[], [], [], []]
        def _select(ui):
            sllist = cmds.ls(sl=1)
            if not sllist:
                om.MGlobal.displayError(u'什么都没选哇')
                return
            if ui == '_IFSwitchAttr':
                slAttr = cmds.channelBox('mainChannelBox', q=1, sma=1)
                if not slAttr:
                    om.MGlobal.displayError(u'要选切换属性哦')
                    return
                dataList[0] = [sllist[0], slAttr[0]]
                cmds.textFieldButtonGrp('%s%s' %(Ui, ui), e=1, tx='%s.%s' %(sllist[0], slAttr[0]))
                return
            elif ui == '_IkPole':
                if len(sllist) != 2:
                    om.MGlobal.displayError(u'要选2个控制器哦')
                    return
                dataList[1] = sllist
            elif ui == '_3FkCtrl':
                if len(sllist) != 3:
                    om.MGlobal.displayError(u'要选3个控制器哦')
                    return
                dataList[2] = sllist
            elif ui == '_3SkinJoint':
                if len(sllist) != 3:
                    om.MGlobal.displayError(u'要选3个骨骼哦')
                    return
                dataList[3] = sllist
            cmds.textFieldButtonGrp('%s%s' %(Ui, ui), e=1, tx=' | '.join(sllist))
        if not layout:
            cmds.showWindow(Ui)

        def doAdv():
            sllist = cmds.ls(sl=1)
            if len(sllist) != 1 or len(cmds.listAttr(sllist[0], st=['FKIKBlend', 'startJoint', 'middleJoint', 'endJoint'])) != 4:
                om.MGlobal.displayError(u'请选择Adv的IKFK切换控制器')
                return
            cmds.addAttr(sllist[0], ln="SeamlessSwitch", at='enum', en='FK:IK:')
            cmds.setAttr("%s.SeamlessSwitch" %sllist[0], e=1, cb=1)
            cmds.addAttr(sllist[0], ln="refresh", at='bool')
            cmds.setAttr("%s.refresh" %sllist[0], e=1, cb=1)
            if cmds.ls('AdvIKFKSeamlessSwitch', typ='script'):
                #Script = cmds.scriptNode('AdvIKFKSeamlessSwitch', q=1, beforeScript=1)
                #Script += "\nscriptJob -attributeChange {IFSwitch}.SeamlessSwitch AdvSeamlessSwitchFKIK -kws;".format(IFSwitch = sllist[0])
                #cmds.scriptNode('AdvIKFKSeamlessSwitch', e=1, beforeScript=Script)
                #cmds.scriptNode('AdvIKFKSeamlessSwitch', eb=1)
                Script = cmds.expression('AdvIKFKSeamlessSwitch_Exp', q=1, s=1)
                Script += "\n{IFSwitch}.refresh = {IFSwitch}.SeamlessSwitch;".format(IFSwitch = sllist[0])
                cmds.expression('AdvIKFKSeamlessSwitch_Exp', e=1, s=Script)
            else:
                fileDir = '%s/AdvSwitchMel' %os.path.dirname(__file__)
                with open(fileDir, 'r') as f:
                    Script = f.read()
                #Script += "\nscriptJob -attributeChange {IFSwitch}.SeamlessSwitch AdvSeamlessSwitchFKIK -kws;".format(IFSwitch = sllist[0])
                cmds.scriptNode(beforeScript=Script, n='AdvIKFKSeamlessSwitch', sourceType='mel', scriptType=1)
                cmds.scriptNode('AdvIKFKSeamlessSwitch', eb=1)
                cmds.expression(n='AdvIKFKSeamlessSwitch_Exp', s='AdvSeamlessSwitchFKIK;\n{IFSwitch}.refresh = {IFSwitch}.SeamlessSwitch;'.format(IFSwitch = sllist[0]), o='', ae=0, uc='none')

        def doIt(data):
            IKFKSwitch = data[0]   #切换控制器、切换属性
            IKPoleCtrl = data[1]   #IK 极向量 控制器
            FkCtrl = data[2]
            SkinJoint = data[3]

            cmds.addAttr(IKFKSwitch[0], ln="SeamlessSwitch", at='enum', en='FK:IK:')
            cmds.setAttr("%s.SeamlessSwitch" %IKFKSwitch[0], e=1, cb=1)
            cmds.addAttr(IKFKSwitch[0], ln="refresh", at='bool')
            cmds.setAttr("%s.refresh" %IKFKSwitch[0], e=1, cb=1)

            _IKFKCtrlLoc = cmds.spaceLocator(p=(0, 0, 0), n="%sloc" %IKFKSwitch[0])[0]
            cmds.parent(_IKFKCtrlLoc, IKFKSwitch[0])
            cmds.setAttr('%s.t' %_IKFKCtrlLoc, 0, 0, 0)
            cmds.setAttr('%s.v' %_IKFKCtrlLoc, 0)
            cmds.addAttr(_IKFKCtrlLoc, ln='%sState' %IKFKSwitch[0], at='bool')

            cmds.addAttr(IKFKSwitch[0], ln='IkCtrl', at='bool')
            cmds.addAttr(IKPoleCtrl[0], ln='IkCtrl', at='bool')
            cmds.connectAttr('%s.IkCtrl' %IKFKSwitch[0], '%s.IkCtrl' %IKPoleCtrl[0], f=1)
            cmds.addAttr(IKFKSwitch[0], ln='IkPole', at='bool')
            cmds.addAttr(IKPoleCtrl[1], ln='IkPole', at='bool')
            cmds.connectAttr('%s.IkPole' %IKFKSwitch[0], '%s.IkPole' %IKPoleCtrl[1], f=1)
            cmds.addAttr(IKFKSwitch[0], ln='Fk1st', at='bool')
            cmds.addAttr(FkCtrl[0], ln='FK1st', at='bool')
            cmds.connectAttr('%s.Fk1st' %IKFKSwitch[0], '%s.FK1st' %FkCtrl[0], f=1)
            cmds.addAttr(IKFKSwitch[0], ln='Fk2nd', at='bool')
            cmds.addAttr(FkCtrl[1], ln='FK2nd', at='bool')
            cmds.connectAttr('%s.Fk2nd' %IKFKSwitch[0], '%s.FK2nd' %FkCtrl[1], f=1)
            cmds.addAttr(IKFKSwitch[0], ln='Fk3rd', at='bool')
            cmds.addAttr(FkCtrl[2], ln='Fk3rd', at='bool')
            cmds.connectAttr('%s.Fk3rd' %IKFKSwitch[0], '%s.Fk3rd' %FkCtrl[2], f=1)
            
            _IkFkSwitchLoc = cmds.spaceLocator(p=(0, 0, 0), n="%s_IkFkSwitchLoc" %IKPoleCtrl[1])[0]
            _IkFkSwitchLocGrp = cmds.group(_IkFkSwitchLoc, n="%s_IkFkSwitchLocGrp" %IKPoleCtrl[1])
            cmds.setAttr('%s.v' %_IkFkSwitchLocGrp, 0)
            cmds.matchTransform(_IkFkSwitchLocGrp, FkCtrl[1], pos=1, rot=1)
            cmds.parent(_IkFkSwitchLocGrp, FkCtrl[1])

            for ctrl, parentC in zip(IKPoleCtrl + FkCtrl, [SkinJoint[-1], _IkFkSwitchLoc] + SkinJoint):
                AimXform = cmds.rename(cmds.duplicate(ctrl, po=1, rr=1), '%sAimXform' %ctrl)
                cmds.addAttr(ctrl, ln='aimXformObj', at='bool')
                cmds.addAttr(AimXform, ln='aimXformObj', at='bool')
                cmds.connectAttr('%s.aimXformObj' %ctrl, '%s.aimXformObj' %AimXform, f=1)
                cmds.setAttr('%s.t' %AimXform, 0, 0, 0)
                cmds.setAttr('%s.rx' %AimXform, l=0)
                cmds.setAttr('%s.ry' %AimXform, l=0)
                cmds.setAttr('%s.rz' %AimXform, l=0)
                #cmds.setAttr('%s.v' %AimXform, 0)
                cmds.parentConstraint(parentC, AimXform, mo=1, w=1)

            if cmds.ls('IKFKSeamlessSwitch', typ='script'):
                #Script = cmds.scriptNode('IKFKSeamlessSwitch', q=1, beforeScript=1)
                #Script += "\ncmds.scriptJob(attributeChange=['{IFSwitch}.SeamlessSwitch', 'SeamlessSwitchIKFKClass.Proc()'], kws=1)".format(IFSwitch = IKFKSwitch[0])
                #cmds.scriptNode('IKFKSeamlessSwitch', e=1, beforeScript=Script)
                #cmds.scriptNode('IKFKSeamlessSwitch', eb=1)
                Script = cmds.expression('AdvIKFKSeamlessSwitch_Exp', q=1, s=1)
                Script += "\n{IFSwitch}.refresh = {IFSwitch}.SeamlessSwitch;".format(IFSwitch = IKFKSwitch[0])
                cmds.expression('AdvIKFKSeamlessSwitch_Exp', e=1, s=Script)
            else:
                Script ="""from maya import cmds
class SeamlessSwitchIKFKClass():
    @staticmethod
    def FkToIk():
        sl = cmds.ls(sl=1, typ='transform')[0]
        IkCtrl = cmds.listConnections('%s.IkCtrl' %sl, s=0, d=1)
        IkPole = cmds.listConnections('%s.IkPole' %sl, s=0, d=1)
        IkCtrlXformObj = cmds.listConnections('%s.aimXformObj' %IkCtrl[0], s=1, d=1)
        IkPoleXformObj = cmds.listConnections('%s.aimXformObj' %IkPole[0], s=1, d=1)
        IkCtrlPos = cmds.xform(IkCtrlXformObj[0], q=1, a=1, ws=1, t=1)
        IkCtrlRot = cmds.getAttr('%s.r' %IkCtrlXformObj[0])[0]
        cmds.setAttr('%s.r' %IkCtrl[0], IkCtrlRot[0], IkCtrlRot[1], IkCtrlRot[2], typ='float3')
        cmds.xform(IkCtrl[0], a=1, ws=1, t=IkCtrlPos)
        cmds.xform(IkPole[0], a=1, ws=1, t=cmds.xform(IkPoleXformObj, q=1, a=1, ws=1, t=1))
        cmds.setAttr('%s.{SwitchAttr}' %sl, 10)
    @staticmethod
    def IkToFk():
        sl = cmds.ls(sl=1, typ='transform')[0]
        Fk1st = cmds.listConnections('%s.Fk1st' %sl, s=0, d=1)
        Fk2nd = cmds.listConnections('%s.Fk2nd' %sl, s=0, d=1)
        Fk3rd = cmds.listConnections('%s.Fk3rd' %sl, s=0, d=1)
        Fk1stXformObj = cmds.listConnections('%s.aimXformObj' %Fk1st[0], s=1, d=1)
        Fk2ndXformObj = cmds.listConnections('%s.aimXformObj' %Fk2nd[0], s=1, d=1)
        Fk3rdXformObj = cmds.listConnections('%s.aimXformObj' %Fk3rd[0], s=1, d=1)
        Rot = cmds.getAttr('%s.r' %Fk1stXformObj[0])[0]
        cmds.setAttr('%s.r' %Fk1st[0], Rot[0], Rot[1], Rot[2], typ='float3')
        Rot = cmds.getAttr('%s.r' %Fk2ndXformObj[0])[0]
        cmds.setAttr('%s.r' %Fk2nd[0], Rot[0], Rot[1], Rot[2], typ='float3')
        Rot = cmds.getAttr('%s.r' %Fk3rdXformObj[0])[0]
        cmds.setAttr('%s.r' %Fk3rd[0], Rot[0], Rot[1], Rot[2], typ='float3')
        cmds.setAttr('%s.{SwitchAttr}' %sl, 0)
    @staticmethod
    def Proc():
        if cmds.getAttr('%s.SeamlessSwitch' %cmds.ls(sl=1)[0]):
            SeamlessSwitchIKFKClass.FkToIk()
        else:
            SeamlessSwitchIKFKClass.IkToFk()
    """.format(SwitchAttr = IKFKSwitch[1])
                #Script += "\ncmds.scriptJob(attributeChange=['{IFSwitch}.SeamlessSwitch', 'SeamlessSwitchIKFKClass.Proc()'], kws=1)".format(IFSwitch = IKFKSwitch[0])
                cmds.scriptNode(beforeScript=Script, n='IKFKSeamlessSwitch', sourceType='python', scriptType=1)
                cmds.scriptNode('IKFKSeamlessSwitch', eb=1)
                cmds.expression(n='AdvIKFKSeamlessSwitch_Exp', s='python("SeamlessSwitchIKFKClass.Proc()");\n{IFSwitch}.refresh = {IFSwitch}.SeamlessSwitch;'.format(IFSwitch = IKFKSwitch[0]), o='', ae=0, uc='none')

