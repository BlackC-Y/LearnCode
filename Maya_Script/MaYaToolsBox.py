# -*- coding: UTF-8 -*-
'''Roadmap:
'''
from maya import cmds, mel
from maya.api import OpenMaya as om
import sys
import os
#try:
#    from importlib import reload
#except :

sys.path.append('%s/MyToolBox' %os.getenv('ALLUSERSPROFILE'))
from CopyWeightTool import *
from CtrlTool import *
from cur2IK_FX import *
from DataSaveUi import *
from PSDshape import *
from Rivet import *
from WeightTool import *


class MayaToolsBox_BlackC():

    #__Verision = 1.1
    
    def ToolUi(self):
        Info = [
            [u'创建Locator', u'在选择物体的位置创建Locator', 'self.createLocator()'],
            [u'从模型提取曲线', u'批量提取曲线 - 仅适用于单片模型', 'self.polytoCurve()'],
            [u'movevtx_Ui', u'修型时传递点 \n选择要传递的点 填写被传递的模型', 'self.movevtx_UI()'],
            [u'samevtx_Ui', u'移动点达到对称修形 \n选择原模型上要对称的点 分别填写模型', 'self.samevtx_UI()'],
            [u'修型骨骼xu', u'创建修型骨骼(高自定义) \n选择要修型的骨骼', 'self.xiuxingJoint()'],
            [u'修型骨骼Hang', u'创建修型骨骼(航少版) \n选择要修型的骨骼', 'self.xiuxingJointHang()'],
            [u'传递UV', u'传递UV \n选择UV模型+要传递的模型', 'self.TransferUV()'],
            [u'曲面上创建毛囊和骨骼_Ui', u'在surface曲面上创建毛囊和骨骼', 'self.createFollicleOnsurface_UI()'],
            [u'ngRelax', u'ngRelax权重', 'self.doPlugin("ngRelax")'],
            [u'拷贝权重工具_Ui', u'拷贝权重工具', 'CopyWeightTool().Ui()'],
            [u'动力学曲线 IK_Ui', u'动力学曲线 IK', 'cur2IK_FX_Ui()'],
            [u'临时储存物体或位置_Ui', u'临时储存物体或位置', 'DataSaveUi().Ui()'],
            [u'PSD修型_Ui', u'PSD修型', 'PSD_PoseUi_KitKat().ToolUi()'],
            [u'Rivet', u'Rivet铆钉', 'cRivet("follicle")'],
            [u'权重工具_Ui', u'点权重调整 \nSave/Load权重', 'WeightTool_JellyBean().ToolUi()'],
            [u'权重检查工具_Ui', u'权重最大影响值检查 清理', 'WeightCheckTool_JellyBean().ToolUi()'],
            [u'控制器Pro_Ui', u'权哥 控制器生成', 'My_CtrllTool().Ui()']
        ]
        self.Info = sorted(Info, key=lambda item: item[0])

        ToolUi = 'MaYaToolsBox'
        if cmds.window(ToolUi, q=1, ex=1):
            cmds.deleteUI(ToolUi)
        cmds.window(ToolUi, t=ToolUi, rtf=1, mb=1, mxb=0, wh=(230, 500))
        cmds.columnLayout('MainCL', cat=('both', 2), rs=2, cw=220, adj=1)
        cmds.textField('searchText', h=24, tcc=lambda *args: self.refreshToolList(cmds.textField('searchText', q=1, tx=1)))
        cmds.textScrollList('ToolList', ams=0, h=250, sc=lambda *args:self.changeToolInfo())
        cmds.columnLayout('EditCL', cat=('both', 2), rs=2, cw=220, adj=1)
        cmds.setParent('..')
        cmds.text('detailText', p='EditCL', h=100, l=u'说明:')
        cmds.button(l=u'执行', c=lambda *args: self.doProc())
        for i in self.Info:
            cmds.textScrollList('ToolList', e=1, a=i[0])
        cmds.showWindow(ToolUi)

    def changeToolInfo(self):
        slitem = cmds.textScrollList('ToolList', q=1, si=1)[0]
        for i in self.Info:
            if slitem == i[0]:
                cmds.text('detailText', e=1, l=i[1])

    def refreshToolList(self, string):
        cmds.textScrollList('ToolList', e=1, ra=1)
        Istr = string.lower()
        for i in self.Info:
            if Istr in i[0].lower() or Istr in i[1].lower():
                cmds.textScrollList('ToolList', e=1, a=i[0])

    def doProc(self):
        slitem = cmds.textScrollList('ToolList', q=1, si=1)[0]
        for i in self.Info:
            if slitem == i[0]:
                cmd = i[2]
                exec(cmd)

    def doPlugin(self, File):
        if File == 'ngRelax':
            ver = int(cmds.about(v=1))
            if ver<2017 or ver>2020:
                om.MGlobal.displayError(u'仅支持2017-2020')
                return
            if cmds.pluginInfo('ngSkinTools.mll', q=1, l=1):
                cmds.ngSkinRelax()
                return
            plugName = '%s%s.mll' %(File, ver)
            if not cmds.pluginInfo(plugName, q=1, l=1):
                cmds.loadPlugin('%s/MyToolBox/plugin/%s' %(os.getenv('ALLUSERSPROFILE'), plugName), qt=1)
            cmds.ngSkinRelax()

    def createLocator(self):
        alist = cmds.ls(sl=1, fl=1)
        for i in alist:
            txyz = cmds.xform(i, q=1, ws=1, t=1)
            cmds.setAttr(cmds.spaceLocator(n=i+'_loc')[0]+'.translate', txyz[0], txyz[1], txyz[2])

    def polytoCurve(self):
        blist = cmds.ls(sl=1)
        for i in blist:
            vnum = cmds.polyEvaluate(i, v=1)
            for v in range(vnum):
                enum = cmds.ls(cmds.polyListComponentConversion(i + '.vtx[' + str(v) + ']', fv=1, ff=1, fuv=1, fvf=1, te=1), fl=1)
                if len(enum) == 4:
                    break
            arclen = []
            for e in enum:
                elist = cmds.polySelectSp(e, q=1, loop=1)
                earclen = 0.0
                for el in elist:
                    earclen += cmds.arclen(el)
                arclen.append(earclen)
            cmds.polySelectSp(enum[arclen.index(max(arclen))], loop=1)
            cname = cmds.rename(cmds.polyToCurve(
                ch=0, form=2, degree=3), i + '_Cur')
            if cmds.xform(cname + '.cv[0]', q=1, ws=1, t=1)[1] < cmds.xform(cname + '.cv[' + str(cmds.getAttr(cname + ".controlPoints", size=1)) + ']', q=1, ws=1, t=1)[1]:
                cmds.reverseCurve(cname, ch=0, rpo=1)

    def movevtx_UI(self):
        ui = 'ToolsBoxUI1'
        try:
            cmds.deleteUI(ui)
        except:
            pass
        cmds.window(ui, t='movevtx')
        cmds.columnLayout(rowSpacing=3)
        cmds.textFieldGrp('UI1objTextFieldGrp', l=u'模型', h=28, cw2=(30, 130))
        cmds.button('UI1RunButton', l="Run", h=28, w=100, c=lambda*args: self.movevtx(cmds.textFieldGrp('UI1objTextFieldGrp', q=1, tx=1)))
        cmds.window(ui, e=True, wh=(180, 100))
        cmds.showWindow(ui)

    def movevtx(self, obj=''):
        # UI
        clist = cmds.ls(sl=1, fl=1)
        for i in clist:
            flo = []
            targe = obj + '.vtx[' + i.split('[', 1)[1]
            for u in range(3):
                flo.append(cmds.xform(i, q=1, t=1, ws=1)[u] - cmds.xform(targe, q=1, t=1, ws=1)[u])
            cmds.select(targe, r=1)
            cmds.move(flo[0], flo[1], flo[2], r=1, os=1, wd=1)
        cmds.select(cl=1)

    def samevtx_UI(self):
        # UI
        ui = 'ToolsBoxUI2'
        try:
            cmds.deleteUI(ui)
        except:
            pass
        cmds.window(ui, t='samevtx')
        cmds.columnLayout(rowSpacing=3)
        cmds.textFieldGrp('UI2obj1TextFieldGrp',l=u'已修形模型', h=28, cw2=(60, 150))
        cmds.textFieldGrp('UI2obj2TextFieldGrp',l=u'要对称模型', h=28, cw2=(60, 150))
        cmds.button('RunButton', l="Run", h=28, w=100, c=lambda *args:
                    self.samevtx(cmds.textFieldGrp('UI2obj1TextFieldGrp', q=1, tx=1), cmds.textFieldGrp('UI2obj2TextFieldGrp', q=1, tx=1)))
        cmds.window(ui, e=True, wh=(220, 100))
        cmds.showWindow(ui)

    def samevtx(self, obj1='', obj2=''):
        list = cmds.ls(sl=1, fl=1)
        obj = list[0].split('.', 1)[0]
        mel.eval("reflectionSetMode objectx;")
        for i in list:
            lvtxT = cmds.xform(obj1+'.'+i.split('.', 1)[1], q=1, os=1, t=1)
            cmds.select(i, sym=1, r=1)
            dvtx = cmds.ls(sl=1, fl=1)
            del dvtx[dvtx.index(i)]
            cmds.xform(obj2+'.'+dvtx[0].split('.', 1)[1], os=1, t=(lvtxT[0]*-1, lvtxT[1], lvtxT[2]))
        mel.eval("reflectionSetMode none;")

    def xiuxingJoint(self):
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

    def xiuxingJointHang(self):
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

    def TransferUV(self):
        dobj = cmds.ls(sl=1)
        if cmds.polyEvaluate(dobj[0], v=1) != cmds.polyEvaluate(dobj[1], v=1):
            dupobj = cmds.duplicate(dobj[1], rr=1)
            cmds.transferAttributes(dobj[0], dupobj, pos=0, nml=0, uvs=2, col=2, spa=0, sus="map1", tus="map1", sm=3, fuv=0, clb=1)
            cmds.delete(dupobj, ch=1)
            cmds.polyTransfer(dobj[1], uv=1, ao=dupobj[0])
            cmds.delete(dupobj)
        else:
            cmds.polyTransfer(dobj[1], uv=1, ao=dobj[0])

    def createFollicleOnsurface_UI(self):
        ui = 'ToolsBoxUI3'
        try:
            cmds.deleteUI(ui)
        except:
            pass
        cmds.window(ui, t='createFollicleOnface')
        cmds.columnLayout(cat=("both", 2), columnWidth=180, rowSpacing=3)
        cmds.textFieldGrp('UI3nameTextFieldGrp', l=u'名称', h=28, cw2=(50, 100))
        cmds.intFieldGrp('UI3numIntFieldGrp', l=u'数量', h=28, cw2=(50, 100))
        cmds.flowLayout(columnSpacing=5)
        cmds.checkBox('UI3JointcheckBox', l=u'创建骨骼', w=80)
        cmds.button('UI3RunButton', l="Run", h=28, w=80, c=lambda *args: self.createFollicleOnsurface(
                    cmds.textFieldGrp('UI3nameTextFieldGrp', q=1, tx=1),
                    cmds.intFieldGrp('UI3numIntFieldGrp', q=1, v1=1),
                    cmds.checkBox('UI3JointcheckBox', q=1, v=1)))
        cmds.setParent('..')
        cmds.showWindow(ui)

    def createFollicleOnsurface(self, name='', num='', joint=0):
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

MayaToolsBox_BlackC().ToolUi()
