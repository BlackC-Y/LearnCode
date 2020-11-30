# -*- coding: UTF-8 -*-
'''Roadmap:1.带UI的直接生成在主窗口中，共用一个button.
'''
from maya import cmds, mel


class MaYaToolsBox():

    __Verision = 1.0
    
    def __init__(self):
        self.Info = {
        'createloc': [u'在选择物体的位置创建Locator',],
        'polytoCurve': [u'批量提取曲线__仅适用于单片模型',],
        'movevtx_UI': [u'修型时传递点 \n选择要传递的点 填写被传递的模型',],
        'samevtx_UI': [u'移动点达到对称修形 \n选择原模型上要对称的点 分别填写模型',],
        'xiuxingJoint': [u'创建修型骨骼(高自定义) \n选择要修型的骨骼',],
        'xiuxingJointWang': [u'创建修型骨骼(乖孙版) \n选择要修型的骨骼',],
        'TransferUV': [u'传递UV \n选择UV模型+要传递的模型',],
        'createFollicleOnface_UI': [u'在平面上创建毛囊和骨骼',],
            }

    def ToolUi(self):
        ToolUi = 'MaYaToolsBox'
        if cmds.window(ToolUi, q=1, ex=1):
            cmds.deleteUI(ToolUi)
        cmds.window(ToolUi, t=ToolUi, rtf=1, mb=1, mxb=0, wh=(230, 500))
        cmds.columnLayout('MainCL', cat=('both', 2), rs=2, cw=220, adj=1)
        cmds.textField('searchText', h=24, tcc=lambda *args: self.refreshToolList(cmds.textField('searchText', q=1, tx=1)))
        cmds.textScrollList('ToolList', ams=0, h=200, sc=lambda *args:
                                cmds.text('detailText', e=1, l=self.Info[cmds.textScrollList('ToolList', q=1, si=1)[0]]))
        cmds.columnLayout('EditCL', cat=('both', 2), rs=2, cw=220, adj=1)
        cmds.setParent('..')
        cmds.text('detailText', p='EditCL', h=100, l='说明:')
        cmds.button(l='执行', c=lambda *args: eval('MaYaToolsBox().%s()' % (cmds.textScrollList('ToolList', q=1, si=1)[0])))

        for i in self.Info:
            cmds.textScrollList('ToolList', e=1, a=i)
        cmds.showWindow(ToolUi)

    def refreshToolList(self, string):
        cmds.textScrollList('ToolList', e=1, ra=1)
        for i in self.Info:
            if string.lower() in i.lower() or string.lower() in self.Info[i][0].lower():
                cmds.textScrollList('ToolList', e=1, a=i)

    def chuangjian(self):
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
        cmds.textFieldGrp('UI1objTextFieldGrp', l='模型', h=28, cw2=(30, 130))
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
        for i in range(8):
            cmds.sphere()
        '''
        cmds.progressWindow(isInterruptable=1)
        while 1:
            if cmds.progressWindow(q=1,isCancelled=1): break
        cmds.progressWindow(endProgress=1)
        '''

    def samevtx_UI(self):
        # UI
        ui = 'ToolsBoxUI2'
        try:
            cmds.deleteUI(ui)
        except:
            pass
        cmds.window(ui, t='samevtx')
        cmds.columnLayout(rowSpacing=3)
        cmds.textFieldGrp('UI2obj1TextFieldGrp',l='已修形模型', h=28, cw2=(60, 150))
        cmds.textFieldGrp('UI2obj2TextFieldGrp',l='要对称模型', h=28, cw2=(60, 150))
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

    def xiuxingJointWang(self):
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

    def createFollicleOnface_UI(self):
        ui = 'ToolsBoxUI3'
        try:
            cmds.deleteUI(ui)
        except:
            pass
        cmds.window(ui, t='createFollicleOnface')
        cmds.columnLayout(cat=("both", 2), columnWidth=180, rowSpacing=3)
        cmds.textFieldGrp('UI3nameTextFieldGrp', l='名称', h=28, cw2=(50, 100))
        cmds.intFieldGrp('UI3numIntFieldGrp', l='数量', h=28, cw2=(50, 100))
        cmds.flowLayout(columnSpacing=5)
        cmds.checkBox('UI3JointcheckBox', l='创建骨骼', w=80)
        cmds.button('UI3RunButton', l="Run", h=28, w=80, c=lambda *args: self.createFollicleOnface(
                    cmds.textFieldGrp('UI3nameTextFieldGrp', q=1, tx=1),
                    cmds.intFieldGrp('UI3numIntFieldGrp', q=1, v1=1),
                    cmds.checkBox('UI3JointcheckBox', q=1, v=1)))
        cmds.setParent('..')
        cmds.showWindow(ui)

    def createFollicleOnface(self, name = '', num = '', joint = 0):
        #UI
        shape = cmds.listRelatives(cmds.ls(sl=1)[0],s=1,type='nurbsSurface')
        if not shape:
            cmds.error()
        Follicle_Grp = name + "_foll_grp"
        Joint_Grp = name + "_Joint_grp"
        if cmds.ls(Follicle_Grp,typ='transform') or cmds.ls(Joint_Grp,typ='transform'):
            cmds.error()
        cmds.group(em=1, n=Follicle_Grp)
        if joint:
            cmds.group(em=1, n=Joint_Grp)
        for i in range(num):
            if i == num:
                break
            follicT = cmds.rename(cmds.listRelatives(cmds.createNode('follicle'),p=1), name+'_foll')
            follicS = cmds.rename(cmds.listRelatives(follicT,s=1),name+'_follShape')
            cmds.connectAttr(shape+".worldSpace[0]", follicS+".inputSurface", f=1)
            cmds.connectAttr(shape+".worldMatrix[0]", follicS+".inputWorldMatrix", f=1)
            cmds.connectAttr(follicS+".outTranslate", follicT+".translate", f=1)
            cmds.connectAttr(follicS+".outRotate", follicT+".rotate", f=1)
            cmds.setAttr(follicS+".parameterV", .5)
            cmds.setAttr(follicS+".parameterU", i*1.0/(num-1))
            cmds.parent(follicT,Follicle_Grp)
            if cmds.checkBox('UI3JointcheckBox',q=1,v=1):
                cmds.select(cl=1)
                jointN = cmds.joint(n=name+i+'Joint')
                cmds.parentConstraint(follicT,jointN,weight=1)
                cmds.parent(jointN,Joint_Grp)
    

MaYaToolsBox().ToolUi()