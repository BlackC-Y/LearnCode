from PySide2 import QtCore, QtGui, QtWidgets
import maya.cmds as cmds
import maya.mel as mm
import maya.OpenMayaUI as Omui
import shiboken2


class BoxUi(object):

    def setupUi(self, BoxUi):
        try:
            Boxui.close()
        except:
            pass
        BoxUi.setObjectName("BoxUi")
        BoxUi.resize(300, 500)
        self.searchEdit = QtWidgets.QLineEdit(BoxUi)
        self.searchEdit.setGeometry(QtCore.QRect(10, 20, 280, 28))
        self.searchEdit.setObjectName("searchEdit")
        self.listView = QtWidgets.QListWidget(BoxUi)
        self.listView.setGeometry(QtCore.QRect(10, 60, 280, 250))
        self.listView.setSortingEnabled(True)
        self.listView.setObjectName("listView")
        self.detail = QtWidgets.QLabel(BoxUi)
        self.detail.setGeometry(QtCore.QRect(10, 320, 280, 120))
        self.detail.setWordWrap(True)
        self.detail.setFont(QtGui.QFont('Courier New', 10, QtGui.QFont.Bold))
        self.detail.setObjectName("detailText")
        self.runJio = QtWidgets.QPushButton(BoxUi)
        self.runJio.setGeometry(QtCore.QRect(10, 460, 280, 28))
        self.runJio.setObjectName("runJio")

        self.retranslateUi(BoxUi)
        QtCore.QMetaObject.connectSlotsByName(BoxUi)

    def retranslateUi(self, BoxUi):
        BoxUi.setWindowTitle(u"BoxUi")
        for i in Showwindow.Jio:
            self.listView.addItem(i)
        self.listView.currentTextChanged.connect(lambda: self.detail.setText(Showwindow.Jio[self.listView.currentItem().text()]))
        #QtCore.QObject.connect(self.listView, QtCore.SIGNAL("currentTextChanged(QString)"), self.label.setText)
        self.searchEdit.textEdited.connect(lambda: self.finditem())
        self.detail.setText(u"说明:")
        self.runJio.setText(u"执行")
        self.runJio.clicked.connect(lambda *args: eval('ToolsBox().' + self.listView.currentItem().text() + '()'))

    def finditem(self):
        self.listView.clear()
        for i in Showwindow.Jio:
            if self.searchEdit.text() in i or self.searchEdit.text() in Showwindow.Jio[i]:
                self.listView.addItem(i)


class Showwindow(BoxUi, QtWidgets.QWidget):

    Jio = {
        'createloc': u'在选择物体的位置创建Locator',
        'polytoCurve': u'批量提取曲线__仅适用于单片模型',
        'movevtxUI': u'修型时传递点 \n选择要传递的点 填写被传递的模型',
        'samevtxUI': u'移动点达到对称修形 \n选择原模型上要对称的点 分别填写模型',
        'xiuxingJoint': u'创建修型骨骼(高自定义) \n选择要修型的骨骼',
        'xiuxingJointWang': u'创建修型骨骼(乖孙版) \n选择要修型的骨骼',
        'TransferUV': u'传递UV \n选择UV模型+要传递的模型',
    }

    def __init__(self):
        super(Showwindow, self).__init__()
        self.setupUi(self)
        self.setParent(shiboken2.wrapInstance(long(Omui.MQtUtil.mainWindow()), QtWidgets.QMainWindow))
        self.setWindowFlags(QtCore.Qt.Window)
        self.setWindowTitle('ToolsBox')
        self.show()


class ToolsBox(object):

    def chuangjian(self):
        cmds.undoInfo(ock=1)
        alist = cmds.ls(sl=1, fl=1)
        for i in alist:
            txyz = cmds.xform(i, q=1, ws=1, t=1)
            cmds.setAttr(cmds.spaceLocator(n=i+'_loc')[0]+'.translate', txyz[0], txyz[1], txyz[2])
        cmds.undoInfo(cck=1)

    def polytoCurve(self):
        cmds.undoInfo(ock=1)
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
        cmds.undoInfo(cck=1)

    def movevtx_UI(self):
        ui = 'ToolsBoxUI1'
        try:
            cmds.deleteUI(ui)
        except:
            pass
        cmds.window(ui, t='movevtx')
        cmds.columnLayout(rowSpacing=3)
        cmds.textFieldGrp('objTextFieldGrp', h=28, cw2=(30, 50))
        cmds.button('RunButton', l="Run", h=28, w=100, c=lambda*args: self.movevtx(cmds.textFieldGrp('objTextFieldGrp', q=1, tx=1)))
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
        cmds.textFieldGrp('obj1TextFieldGrp',l='已修形模型', h=28, cw2=(30, 50))
        cmds.textFieldGrp('obj2TextFieldGrp',l='要对称模型', h=28, cw2=(30, 50))
        cmds.button('RunButton', l="Run", h=28, w=100, c=lambda *args:
                    self.samevtx(cmds.textFieldGrp('obj1TextFieldGrp', q=1, tx=1), cmds.textFieldGrp('obj2TextFieldGrp', q=1, tx=1)))
        cmds.showWindow(ui)

    def samevtx(self, obj1='', obj2=''):
        list = cmds.ls(sl=1, fl=1)
        obj = list[0].split('.', 1)[0]
        mm.eval("reflectionSetMode objectx;")
        for i in list:
            lvtxT = cmds.xform(obj1+'.'+i.split('.', 1)[1], q=1, os=1, t=1)
            cmds.select(i, sym=1, r=1)
            dvtx = cmds.ls(sl=1, fl=1)
            del dvtx[dvtx.index(i)]
            cmds.xform(obj2+'.'+dvtx[0].split('.', 1)[1], os=1, t=(lvtxT[0]*-1, lvtxT[1], lvtxT[2]))
        mm.eval("reflectionSetMode none;")

    def xiuxingJoint(self):
        cmds.undoInfo(ock=1)
        joint = cmds.ls(sl=1, type="joint")
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
        cmds.connectAttr(floatMathA+".outFloat", floatMathB+".floatB", f=1)
        cmds.connectAttr(floatMathB+".outFloat", floatMathC+".floatA", f=1)
        cmds.connectAttr(floatMathC+".outFloat", blendJointEnd+".ty", f=1)
        cmds.connectAttr(joint+".rotateZ", floatMathB+".floatA", f=1)
        cmds.undoInfo(cck=1)

    def xiuxingJointWang(self):
        cmds.undoInfo(ock=1)
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
        cmds.undoInfo(cck=1)

    def TransferUV(self):
        cmds.undoInfo(ock=1)
        dobj = cmds.ls(sl=1)
        if cmds.polyEvaluate(dobj[0], v=1) != cmds.polyEvaluate(dobj[1], v=1):
            dupobj = cmds.duplicate(dobj[1], rr=1)
            cmds.transferAttributes(dobj[0], dupobj,
                                    transferPositions=0, transferNormals=0, transferUVs=2, transferColors=2, sampleSpace=0,
                                    sourceUvSpace="map1", targetUvSpace="map1", searchMethod=3, flipUVs=0, colorBorders=1)
            cmds.delete(dupobj, ch=1)
            cmds.polyTransfer(dobj[1], uv=1, ao=dupobj[0])
            cmds.delete(dupobj)
        else:
            cmds.polyTransfer(dobj[1], uv=1, ao=dobj[0])
        cmds.undoInfo(cck=1)


Boxui = Showwindow()
Boxui.show()
