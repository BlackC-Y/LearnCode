# -*- coding: UTF-8 -*-
#Support Maya2016-2020
'''Roadmap:1.试着添加一个由骨骼建立的流程
'''
try:
    from PySide2 import QtCore, QtGui, QtWidgets
    import shiboken2
except ImportError:
    from PySide import QtGui as QtWidgets
    from PySide import QtGui
    from PySide import QtCore
    import shiboken as shiboken2
from maya import cmds, mel
from maya import OpenMaya as Om, OpenMayaUI as Omui
import re


ui_variable = {}

class Ui_ApplePieA(QtWidgets.QWidget):
    
    def __init__(self):
        self._pTCIKVerision = 'v2.41'
        super(Ui_ApplePieA, self).__init__(shiboken2.wrapInstance(long(Omui.MQtUtil.mainWindow()), QtWidgets.QMainWindow))
        self.UiName = 'ApplePieA'
        #self.setFocus()
        self.setupUi()
        
    def setupUi(self):
        if cmds.window(self.UiName, q=1, ex=1):
            cmds.deleteUI(self.UiName)
        self.setObjectName(self.UiName)
        #self.resize(260, 500)
        #self.setMinimumSize(260, 500)
        self.setFixedSize(260, 500)
        self.MainverticalLayout = QtWidgets.QVBoxLayout(self)
        self.MainverticalLayout.setObjectName("MainverticalLayout")
        self.MainverticalLayout.setSpacing(3)
        self.MainverticalLayout.setContentsMargins(0, 0, 0, 0)

        self.tabWidget = QtWidgets.QTabWidget(self)
        self.tabWidget.setObjectName("tabWidget")
        self.child1 = QtWidgets.QWidget()
        self.child1.setObjectName("child1")
        self.child1verLayout = QtWidgets.QVBoxLayout(self.child1)
        self.child1verLayout.setObjectName("child1verticalLayout")
        self.child1verLayout.setSpacing(5)
        self.child1verLayout.setContentsMargins(8, 5, 8, 3)

        self.horLayoutA = QtWidgets.QHBoxLayout()
        self.horLayoutA.setObjectName("horLayout")
        self.RebuildIntText = QtWidgets.QLabel(self.child1)
        self.RebuildIntText.setMinimumSize(QtCore.QSize(80, 26))
        self.RebuildIntText.setObjectName("RebuildIntText")
        ui_variable['RebuildInt'] = self.RebuildInt = QtWidgets.QLineEdit(self.child1)
        self.RebuildInt.setMinimumSize(QtCore.QSize(100, 22))
        self.RebuildInt.setObjectName("RebuildInt")
        self.horLayoutA.addWidget(self.RebuildIntText)
        self.horLayoutA.addWidget(self.RebuildInt)
        self.child1verLayout.addLayout(self.horLayoutA)

        self.horLayoutB = QtWidgets.QHBoxLayout()
        self.horLayoutB.setObjectName("horLayout")
        self.CurveNameText = QtWidgets.QLabel(self.child1)
        self.CurveNameText.setMinimumSize(QtCore.QSize(80, 26))
        self.CurveNameText.setObjectName("CurveNameText")
        ui_variable['CurveName'] = self.CurveName = QtWidgets.QLineEdit(self.child1)
        self.CurveName.setMinimumSize(QtCore.QSize(100, 22))
        self.CurveName.setObjectName("CurveName")
        self.horLayoutB.addWidget(self.CurveNameText)
        self.horLayoutB.addWidget(self.CurveName)
        self.child1verLayout.addLayout(self.horLayoutB)
        #self.CurveNameWar = QtWidgets.QLabel(self.child1)
        #self.CurveNameWar.setAlignment(QtCore.Qt.AlignCenter)
        #self.CurveNameWar.setStyleSheet("color:yellow")
        #self.CurveNameWar.setObjectName("CurveNameWar")

        self.horLayoutC = QtWidgets.QHBoxLayout()
        self.horLayoutC.setObjectName("horLayout")
        self.SelectPolyCurve = QtWidgets.QPushButton(self.child1)
        self.SelectPolyCurve.setMinimumSize(QtCore.QSize(80, 26))
        self.SelectPolyCurve.setObjectName("SelectPolyCurve")
        self.reverseCurve = QtWidgets.QPushButton(self.child1)
        self.reverseCurve.setMinimumSize(QtCore.QSize(80, 26))
        self.reverseCurve.setObjectName("reverseCurve")
        self.horLayoutC.addWidget(self.SelectPolyCurve)
        self.horLayoutC.addWidget(self.reverseCurve)
        self.child1verLayout.addLayout(self.horLayoutC)
        
        self.lineA = QtWidgets.QFrame(self.child1)
        self.lineA.setFrameShape(QtWidgets.QFrame.HLine)
        self.lineA.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.lineA.setMinimumSize(QtCore.QSize(100, 10))
        self.lineA.setObjectName("line")
        self.child1verLayout.addWidget(self.lineA)

        self.horLayoutD = QtWidgets.QHBoxLayout()
        self.horLayoutD.setObjectName("horLayout")
        self.horLayoutD.setSpacing(3)
        ui_variable['SkinCtrlbox'] = self.SkinCtrlbox = QtWidgets.QCheckBox(self.child1)
        self.SkinCtrlbox.setObjectName("SkinCtrlbox")
        self.SkinCtrlbox.setMinimumSize(QtCore.QSize(130, 26))
        ui_variable['ctrlNumhorLineEdit'] = self.ctrlNumLineEdit = QtWidgets.QLineEdit(self.child1)
        self.ctrlNumLineEdit.setMinimumSize(QtCore.QSize(35, 22))
        self.ctrlNumLineEdit.setValidator(QtGui.QIntValidator())
        self.ctrlNumLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.ctrlNumLineEdit.setText('5')
        self.ctrlNumLineEdit.setObjectName("ctrlNumLineEdit")
        spacerItemA = QtWidgets.QSpacerItem(150, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horLayoutD.addWidget(self.SkinCtrlbox)
        self.horLayoutD.addWidget(self.ctrlNumLineEdit)
        self.horLayoutD.addItem(spacerItemA)
        self.child1verLayout.addLayout(self.horLayoutD)

        self.gridLayoutWidget = QtWidgets.QWidget(self.child1)
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setSpacing(3)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")

        ui_variable['IKFKCtrlbox'] = self.IKFKCtrlbox = QtWidgets.QCheckBox(self.child1)
        self.IKFKCtrlbox.setMinimumSize(QtCore.QSize(100, 26))
        self.IKFKCtrlbox.setObjectName("IKFKCtrlbox")
        #self.IKFKCtrlbox.setChecked(True)
        ui_variable['IKjointbox'] = self.IKjointbox = QtWidgets.QCheckBox(self.child1)
        self.IKjointbox.setMinimumSize(QtCore.QSize(80, 26))
        self.IKjointbox.setObjectName("IKjointbox")
        #self.selectboxGrp = QtWidgets.QButtonGroup(self.child1)
        #self.selectboxGrp.addButton(self.selectboxA,11)
        #self.selectboxGrp.addButton(self.selectboxB,12)

        ui_variable['FXCurvebox'] = self.FXCurvebox = QtWidgets.QCheckBox(self.child1)
        self.FXCurvebox.setMinimumSize(QtCore.QSize(80, 26))
        self.FXCurvebox.setObjectName("FXCurvebox")
        ui_variable['OnlyFXCurvebox'] = self.OnlyFXCurvebox = QtWidgets.QCheckBox(self.child1)
        self.OnlyFXCurvebox.setMinimumSize(QtCore.QSize(100, 26))
        self.OnlyFXCurvebox.setObjectName("FXCurvebox")

        self.JointIntText = QtWidgets.QLabel(self.child1)
        self.JointIntText.setMinimumSize(QtCore.QSize(100, 26))
        self.JointIntText.setObjectName("JointIntText")
        ui_variable['JointInt'] = self.JointInt = QtWidgets.QLineEdit(self.child1)
        self.JointInt.setMinimumSize(QtCore.QSize(100, 20))
        self.JointInt.setValidator(QtGui.QIntValidator())
        self.JointInt.setText('8')
        self.JointInt.setObjectName("JointInt")

        self.HairSystemText = QtWidgets.QLabel(self.child1)
        self.HairSystemText.setMinimumSize(QtCore.QSize(80, 26))
        self.HairSystemText.setObjectName("HairSystemText")
        ui_variable['SelectHairSystem'] = self.SelectHairSystem = QtWidgets.QComboBox(self.child1)
        self.SelectHairSystem.setObjectName("SelectHairSystem")
        self.SelectHairSystem.setMinimumSize(QtCore.QSize(100, 22))
        self.SelectHairSystem.installEventFilter(self)

        self.NucleusText = QtWidgets.QLabel(self.child1)
        self.NucleusText.setMinimumSize(QtCore.QSize(60, 26))
        self.NucleusText.setObjectName("NucleusText")
        ui_variable['SelectNucleus'] = self.SelectNucleus = QtWidgets.QComboBox(self.child1)
        self.SelectNucleus.setObjectName("SelectNucleus")
        self.SelectNucleus.setMinimumSize(QtCore.QSize(100, 22))
        self.SelectNucleus.installEventFilter(self)

        self.gridLayout.addWidget(self.IKFKCtrlbox, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.IKjointbox, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.FXCurvebox, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.OnlyFXCurvebox, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.JointIntText, 2, 0, 1, 1)
        self.gridLayout.addWidget(self.JointInt, 2, 1, 1, 1)
        self.gridLayout.addWidget(self.HairSystemText, 3, 0, 1, 1)
        self.gridLayout.addWidget(self.SelectHairSystem, 3, 1, 1, 1)
        self.gridLayout.addWidget(self.NucleusText, 4, 0, 1, 1)
        self.gridLayout.addWidget(self.SelectNucleus, 4, 1, 1, 1)
        self.child1verLayout.addWidget(self.gridLayoutWidget)

        self.BuildCtrl = QtWidgets.QPushButton(self.child1)
        self.BuildCtrl.setObjectName("BuildCtrl")
        self.child1verLayout.addWidget(self.BuildCtrl)

        child1spacerItem0 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.child1verLayout.addItem(child1spacerItem0)

        self.PoseEdit = QtWidgets.QPushButton(self.child1)
        self.PoseEdit.setMaximumSize(QtCore.QSize(100, 26))
        self.PoseEdit.setObjectName("PoseEdit")
        self.child1verLayout.addWidget(self.PoseEdit)

        self.tabWidget.addTab(self.child1, "")


        self.child2 = QtWidgets.QWidget()
        self.child2.setObjectName("child2")
        self.child2verLayout = QtWidgets.QVBoxLayout(self.child2)
        self.child2verLayout.setObjectName("child2verticalLayout")
        self.child2verLayout.setSpacing(8)
        self.child2verLayout.setContentsMargins(8, 5, 8, 3)

        self.SelCtrlCurve = QtWidgets.QPushButton(self.child2)
        self.SelCtrlCurve.setMinimumSize(QtCore.QSize(100, 26))
        self.SelCtrlCurve.setObjectName("SelCtrlCurve")
        self.child2verLayout.addWidget(self.SelCtrlCurve)

        self.CShape = QtWidgets.QPushButton(self.child2)
        self.CShape.setMinimumSize(QtCore.QSize(100, 26))
        self.CShape.setObjectName("CShape")
        self.child2verLayout.addWidget(self.CShape)

        self.horizontalLayoutF = QtWidgets.QHBoxLayout()
        self.horizontalLayoutF.setObjectName("horizontalLayout")
        self.horizontalLayoutF.setSpacing(3)
        self.RotX = QtWidgets.QPushButton(self.child2)
        self.RotX.setMinimumSize(QtCore.QSize(75, 26))
        self.RotX.setObjectName("RotX")
        self.RotY = QtWidgets.QPushButton(self.child2)
        self.RotY.setMinimumSize(QtCore.QSize(75, 26))
        self.RotY.setObjectName("RotY")
        self.RotZ = QtWidgets.QPushButton(self.child2)
        self.RotZ.setMinimumSize(QtCore.QSize(75, 26))
        self.RotZ.setObjectName("RotZ")
        self.horizontalLayoutF.addWidget(self.RotX)
        self.horizontalLayoutF.addWidget(self.RotY)
        self.horizontalLayoutF.addWidget(self.RotZ)
        self.child2verLayout.addLayout(self.horizontalLayoutF)

        self.horizontalLayoutG = QtWidgets.QHBoxLayout()
        self.horizontalLayoutG.setObjectName("horizontalLayout")
        self.horizontalLayoutG.setSpacing(3)
        self.ScaleAdd = QtWidgets.QPushButton(self.child2)
        self.ScaleAdd.setMinimumSize(QtCore.QSize(100, 26))
        self.ScaleAdd.setObjectName("ScaleAdd")
        self.ScaleSub = QtWidgets.QPushButton(self.child2)
        self.ScaleSub.setMinimumSize(QtCore.QSize(100, 26))
        self.ScaleSub.setObjectName("ScaleSub")
        self.horizontalLayoutG.addWidget(self.ScaleAdd)
        self.horizontalLayoutG.addWidget(self.ScaleSub)
        self.child2verLayout.addLayout(self.horizontalLayoutG)

        self.horizontalLayoutH = QtWidgets.QHBoxLayout()
        self.horizontalLayoutH.setObjectName("horizontalLayout")
        self.horizontalLayoutH.setSpacing(3)
        self.SColorview = QtWidgets.QPushButton(self.child2)
        self.SColorview.setMinimumSize(QtCore.QSize(80, 26))
        self.SColorview.setObjectName("SColorview")
        self.horizontalLayoutH.addWidget(self.SColorview)
        ui_variable['SColorInt'] = self.SColorInt = QtWidgets.QSlider(self.child2)
        self.SColorInt.setMinimum(1)
        self.SColorInt.setMaximum(31)
        self.SColorInt.setOrientation(QtCore.Qt.Horizontal)
        self.SColorInt.setObjectName("SColorInt")
        self.horizontalLayoutH.addWidget(self.SColorInt)
        self.child2verLayout.addLayout(self.horizontalLayoutH)

        child2spacerItem0 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.child2verLayout.addItem(child2spacerItem0)

        self.tabWidget.addTab(self.child2, "")
        self.MainverticalLayout.addWidget(self.tabWidget)

        ui_variable['Statusbar'] = self.Statusbar = QtWidgets.QStatusBar(self)
        self.Statusbar.setStyleSheet("color:yellow")
        self.Statusbar.setObjectName("Statusbar")
        self.MainverticalLayout.addWidget(self.Statusbar)

        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(self)
        ApplePieA_Dynamic().Ready_GetNode('HairSystem')
        ApplePieA_Dynamic().Ready_GetNode('Nucleus')

        self.RebuildIntText.setText(u"重建段数")
        self.RebuildInt.setPlaceholderText(u"重建段数")
        self.CurveNameText.setText(u"曲线名")
        self.CurveName.setPlaceholderText(u"曲线名")
        self.SelectPolyCurve.setText(u"选模型的线")
        self.SelectPolyCurve.clicked.connect(lambda *args: ApplePieA_pTCIK().SelectPolyCurve())
        self.reverseCurve.setText(u"反转曲线")
        self.reverseCurve.clicked.connect(lambda *args: ApplePieA_pTCIK().reverseCurve())
        self.SkinCtrlbox.setText(u"骨骼控制             数量： ")
        self.IKFKCtrlbox.setText(u"IKFK控制")
        self.IKjointbox.setText(u'建立IK骨骼')
        self.FXCurvebox.setText(u"添加动力学")
        self.OnlyFXCurvebox.setText(u"仅动力学曲线")
        self.OnlyFXCurvebox.clicked.connect(lambda: self.setdisable())
        self.JointIntText.setText(u"骨骼段数")
        self.HairSystemText.setText(u"HairSystem")
        self.NucleusText.setText(u"Nucleus")
        if int(cmds.about(v=1)) > 2016:
            self.SelectHairSystem.currentTextChanged.connect(lambda *args: ApplePieA_Dynamic().Acondition())
            self.SelectNucleus.currentTextChanged.connect(lambda *args: ApplePieA_Dynamic().Acondition())
        else:
            self.SelectHairSystem.currentIndexChanged.connect(lambda *args: ApplePieA_Dynamic().Acondition())
            self.SelectNucleus.currentIndexChanged.connect(lambda *args: ApplePieA_Dynamic().Acondition())
        self.BuildCtrl.setText(u"Build")
        self.BuildCtrl.clicked.connect(lambda *args: ApplePieA_pTCIK().createCtrl())
        self.PoseEdit.setText(u"PoseEdit_ADV")
        self.PoseEdit.clicked.connect(lambda *args: ApplePieA_pTCIK().PoseCheck())
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.child1), u"本体")

        self.SelCtrlCurve.setText(u'选择控制器')
        self.SelCtrlCurve.clicked.connect(lambda *args: ApplePieA_pTCIK().SelCurve())
        self.CShape.setText(u"换个形状")
        self.CShape.clicked.connect(lambda *args: ApplePieA_pTCIK().cShape())
        self.RotX.setText(u"RotX")
        self.RotX.clicked.connect(lambda *args: ApplePieA_pTCIK().RSCurve('RX'))
        self.RotY.setText(u"RotY")
        self.RotY.clicked.connect(lambda *args: ApplePieA_pTCIK().RSCurve('RY'))
        self.RotZ.setText(u"RotZ")
        self.RotZ.clicked.connect(lambda *args: ApplePieA_pTCIK().RSCurve('RZ'))
        self.ScaleAdd.setText(u"放大曲线")
        self.ScaleAdd.clicked.connect(lambda *args: ApplePieA_pTCIK().RSCurve('SA'))
        self.ScaleSub.setText(u"缩小曲线")
        self.ScaleSub.clicked.connect(lambda *args: ApplePieA_pTCIK().RSCurve('SS'))
        self.SColorInt.valueChanged.connect(lambda*args: self.changeSColorInt())
        self.SColorview.setText(u"改变颜色")
        self.SColorview.clicked.connect(lambda *args: ApplePieA_pTCIK().ChangeCurveColor())
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.child2), u"曲线DLC")
        
        #self.setParent(shiboken2.wrapInstance(long(Omui.MQtUtil.mainWindow()), QtWidgets.QMainWindow))
        self.setWindowFlags(QtCore.Qt.Window)
        #self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)   #置顶
        self.setWindowTitle('pTCIK by_Y')
        ui_variable['Statusbar'].showMessage(self._pTCIKVerision)
        self.show()
        
    def eventFilter(self, object, event):     #鼠标移动就会触发...淦
        if object == self.SelectHairSystem:
            if event.type() == QtCore.QEvent.MouseButtonPress:
                ApplePieA_Dynamic().Ready_GetNode('HairSystem')
            # if event.type() == QtCore.QEvent.MouseButtonDblClick:
            #    if event.button() == QtCore.Qt.RightButton:
            #        pass
            return super(Ui_ApplePieA, self).eventFilter(object, event)
        elif object == self.SelectNucleus:
            if event.type() == QtCore.QEvent.MouseButtonPress:
                ApplePieA_Dynamic().Ready_GetNode('Nucleus')
            return super(Ui_ApplePieA, self).eventFilter(object, event)

    def setdisable(self):
        if self.OnlyFXCurvebox.isChecked():
            self.SkinCtrlbox.setEnabled(False)
            self.ctrlNumLineEdit.setEnabled(False)
            self.IKFKCtrlbox.setEnabled(False)
            self.IKjointbox.setEnabled(False)
            self.FXCurvebox.setEnabled(False)
            self.JointInt.setEnabled(False)
            self.JointIntText.setEnabled(False)
        else:
            self.SkinCtrlbox.setEnabled(True)
            self.ctrlNumLineEdit.setEnabled(True)
            self.IKFKCtrlbox.setEnabled(True)
            self.IKjointbox.setEnabled(True)
            self.FXCurvebox.setEnabled(True)
            self.JointInt.setEnabled(True)
            self.JointIntText.setEnabled(True)

    def changeSColorInt(self):
        ColorInt = int(self.SColorInt.value())
        ColorIndex = [i*255 for i in cmds.colorIndex(ColorInt, q=1)]
        self.SColorview.setStyleSheet('background-color:rgb(%s,%s,%s)' %(ColorIndex[0], ColorIndex[1], ColorIndex[2]))
        #cmds.canvas('CCanvas', e=1, rgbValue=(ColorIndex[0], ColorIndex[1], ColorIndex[2]))


class ApplePieA_pTCIK(object):

    curveShape = 0

    def SelectPolyCurve(self):
        Curvename = ui_variable['CurveName'].text()
        ReBNum = ui_variable['RebuildInt'].text()
        if not ReBNum:
            ui_variable['Statusbar'].showMessage(u'//没填重建段数')
            Om.MGlobal.displayError(u'//没填重建段数')
            return
        if not Curvename:
            ui_variable['Statusbar'].showMessage(u"//没填曲线名")
            Om.MGlobal.displayError(u"//没填曲线名")
            return
        polyEdgeN = cmds.ls(sl=1)
        # bothName = cmp(Curvename,cmds.ls())  #对比名称
        if Curvename in cmds.ls():
            ui_variable['Statusbar'].showMessage(u"//名称冲突")
            Om.MGlobal.displayError(u"//名称冲突")
            return
        cmds.undoInfo(ock=1)
        if cmds.confirmDialog(t='Confirm', m='尝试居中对齐?', b=['Yes', 'No'], db='Yes', cb='No', ds='No') == 'Yes':
            cmds.polyToCurve(ch=0, form=2, degree=3, n='__temp_cur')
            cmds.select(polyEdgeN, r=1)
            mel.eval('PolySelectConvert 3')
            selv = cmds.ls(sl=1, fl=1)
            for v in range(len(selv)):
                cmds.select(selv[v], r=1)
                mel.eval('PolySelectConvert 2')
                cmds.select(polyEdgeN, d=1)
                mel.eval('performSelContiguousEdges 0')
                cmds.cluster(n='__temp_clu')
            node_p = {}
            for c in range(len(cmds.ls('__temp_clu*Handle'))):
                temp_node = cmds.createNode('nearestPointOnCurve', n='__temp_node')
                cmds.connectAttr('__temp_cur.worldSpace[0]', temp_node + '.inputCurve')
                if not c:
                    cmds.connectAttr('__temp_cluHandleShape.origin', temp_node + '.inPosition')
                else:
                    cmds.connectAttr('__temp_clu%sHandleShape.origin', temp_node + '.inPosition' % c)
                node_p[c] = cmds.getAttr(temp_node + '.parameter')
            node_p_list = sorted(node_p.items(), key=lambda item: item[1]) # 字典排序
            tcws = [[0 for y in range(3)] for x in range(len(selv))]
            for v in range(len(selv)):
                c = '' if not node_p_list[v][0] else node_p_list[v][0]
                tcws[v][0] = cmds.getAttr('__temp_clu%sHandleShape.originX' % c)
                tcws[v][1] = cmds.getAttr('__temp_clu%sHandleShape.originY' % c)
                tcws[v][2] = cmds.getAttr('__temp_clu%sHandleShape.originZ' % c)
            cmds.curve(p=tcws, n=Curvename)
            reshape = cmds.listRelatives(Curvename, s=1)
            cmds.rename(reshape, Curvename + 'Shape')
            cmds.delete('__temp_*')
        else:
            cmds.select(polyEdgeN, r=1)
            pTCname = cmds.polyToCurve(ch=0, form=2, degree=3)
            cmds.rename(pTCname[0], Curvename)
        cmds.rebuildCurve(Curvename, ch=0, rpo=1, rt=0, end=1, kr=0, kcp=0, kep=1, kt=0, s=int(ReBNum), d=3, tol=0.01)
        cvSize = cmds.getAttr(Curvename + ".controlPoints", size=1)
        cmds.delete(Curvename + '.cv[1]', Curvename + '.cv[%s]' %(cvSize-2))
        cmds.setAttr(Curvename + ".dispCV", 1)
        cmds.undoInfo(cck=1)

    def checkCurve(self):
        curlist = cmds.ls(sl=1)
        for i in curlist:
            if not cmds.listRelatives(i, s=1, type='nurbsCurve'):
                ui_variable['Statusbar'].showMessage(u'//有非曲线物体')
                Om.MGlobal.displayError(u'//有非曲线物体')
                return
        return curlist

    def reverseCurve(self):
        cmds.undoInfo(ock=1)
        getlist = self.checkCurve()
        if not getlist:
            return
        for i in getlist:
            cmds.reverseCurve(i, ch=0, rpo=1)
        cmds.undoInfo(cck=1)

    def createCtrl(self):
        getlist = self.checkCurve()
        if not getlist:
            return
        cmds.undoInfo(ock=1)
        if ui_variable['OnlyFXCurvebox'].isChecked():
            ApplePieA_Dynamic().FXCurve(getlist)
            return
        if ui_variable['SkinCtrlbox'].isChecked():
            jointint = int(ui_variable['ctrlNumhorLineEdit'].text())
            self.jointCtrlNum = jointint
            for i in getlist:
                cmds.setAttr(i + ".dispCV", 0)
                if not cmds.ls(i + '.ctrlName'):
                    cmds.addAttr(i, ln='ctrlName', dt='string')
                _tempPos = cmds.createNode('pointOnCurveInfo')
                cmds.connectAttr(i + '.worldSpace[0]', _tempPos + '.inputCurve', f=1)
                cmds.setAttr(_tempPos + '.top', 1)
                _ctrlJointList = []
                for num in range(1, jointint + 1):
                    if num != 1:
                        cmds.setAttr(_tempPos + '.pr', 1.0 / float(jointint - 1) * (num - 1))
                    cmds.select(cl=1)
                    _pos = cmds.getAttr(_tempPos + '.p')[0]
                    jotN = cmds.joint(p=_pos, n='%s_control%s' %(i, num))
                    _ctrlJointList.append(jotN)
                    createCur = cmds.circle(ch=0, n="%s_Ctrl" %jotN)[0]
                    ctrlgrp = cmds.group(cmds.group(n=createCur + "_SDK"), n=createCur + "_grp")
                    cmds.setAttr(ctrlgrp + '.t', _pos[0], _pos[1], _pos[2])
                    cmds.parent(jotN, createCur)
                    cmds.delete(cmds.tangentConstraint(i, ctrlgrp, w=1, aim=(0, 0, 1), u=(0, 1, 0), wut="scene"))
                cmds.skinCluster(_ctrlJointList, i, tsb=1, dr=4, mi=4)
                cmds.delete(_tempPos)
                cmds.setAttr(i + '.ctrlName', i + '_control*_Ctrl', type='string')
        else:
            for i in getlist:
                cmds.setAttr(i + ".dispCV", 0)
                cmds.DeleteHistory(i)
                if not cmds.ls(i + '.ctrlName'):
                    cmds.addAttr(i, ln='ctrlName', dt='string')
                curve = cmds.listRelatives(i, s=1, type="nurbsCurve")[0]
                numCVs = cmds.getAttr(i + ".controlPoints", size=1)
                for nu in range(numCVs):
                    createClu = cmds.cluster('%s.cv[%s]' %(curve, nu), n='%s_clu%s' %(i, nu + 1), rel=1)[1]
                    createCur = cmds.circle(ch=0, n="%s_control%s_Ctrl" %(i, nu + 1))[0]
                    ctrlgroup = cmds.group(cmds.group(n=createCur + "_SDK"), n=createCur + "_grp")
                    cmds.connectAttr(createClu + "Shape.origin", ctrlgroup + ".translate", f=1)
                    cmds.disconnectAttr(createClu + "Shape.origin", ctrlgroup + ".translate")
                    cmds.delete(cmds.tangentConstraint(i, ctrlgroup, w=1, aim=(0, 0, 1), u=(0, 1, 0), wut="scene"))
                    cmds.parentConstraint(createCur, createClu, mo=1)
                    cmds.select(cl=1)
                cmds.setAttr(i + '.ctrlName', i + '_control*_Ctrl', type='string')
        cmds.select(getlist, r=1)
        if ui_variable['IKFKCtrlbox'].isChecked():
            self.IKFKCtrl(ui_variable['SkinCtrlbox'].isChecked())
        if ui_variable['FXCurvebox'].isChecked():
            ApplePieA_Dynamic().FXCurve(getlist)
        if ui_variable['IKjointbox'].isChecked():
            if ui_variable['FXCurvebox'].isChecked():
                for i in getlist:
                    self.CurveToIK(i + '_Blend')
            else:
                for i in getlist:
                    self.CurveToIK(i)
        cmds.undoInfo(cck=1)

    def IKFKCtrl(self, ctrlmode):
        getlist = self.checkCurve()
        if not getlist:
            return
        for i in getlist:
            ctrlSize = self.jointCtrlNum if ctrlmode else cmds.getAttr(i + ".controlPoints", size=1)
            lastCtrl = "%s_control%s_Ctrl" %(i, ctrlSize)
            cmds.addAttr(lastCtrl, ln='IKFK', at='bool')
            cmds.setAttr(lastCtrl + ".IKFK", 1 ,e=1, k=1)
            for n in range(ctrlSize - 1):
                _tempcon = cmds.parentConstraint("%s_control%s_Ctrl" %(i, n + 1), "%s_control%s_Ctrl_grp" %(i, n + 2), mo=1)[0]
                cmds.connectAttr(lastCtrl + ".IKFK", '%s.%s' %(_tempcon, cmds.listAttr(_tempcon, st='*W0')[0]), f=1)

    def cShape(self):
        self.curSample = [
            [((-.5, .5, .5), (-.5, .5, -.5), (.5, .5, -.5), (.5, .5, .5), (-.5, .5, .5), (-.5, -.5, .5), (-.5, -.5, -.5), (-.5, .5, -.5), (-.5, .5, .5), (-.5, -.5, .5),(.5, -.5, .5), (.5, .5, .5), (.5, .5, -.5), (.5, -.5, -.5), (.5, -.5, .5), (.5, -.5, -.5), (-.5, -.5, -.5)), (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16)],
            [((0, 1, 0), (0, 0.92388, 0.382683), (0, 0.707107, 0.707107), (0, 0.382683, 0.92388), (0, 0, 1), (0, -0.382683, 0.92388), (0, -0.707107, 0.707107), (0, -0.92388, 0.382683), (0, -1, 0), (0, -0.92388, -0.382683), (0, -0.707107, -0.707107), (0, -0.382683, -0.92388), (0, 0, -1), (0, 0.382683, -0.92388), (0, 0.707107, -0.707107), (0, 0.92388, -0.382683), (0, 1, 0), (0.382683, 0.92388, 0), (0.707107, 0.707107, 0), (0.92388, 0.382683, 0), (1, 0, 0), (0.92388, -0.382683, 0), (0.707107, -0.707107, 0), (0.382683, -0.92388, 0), (0, -1, 0), (-0.382683, -0.92388, 0), (-0.707107, -0.707107, 0), (-0.92388, -0.382683, 0), (-1, 0, 0), (-0.92388, 0.382683, 0), (-0.707107, 0.707107, 0),(-0.382683, 0.92388, 0), (0, 1, 0), (0, 0.92388, -0.382683), (0, 0.707107, -0.707107), (0, 0.382683, -0.92388), (0, 0, -1), (-0.382683, 0, -0.92388), (-0.707107, 0, -0.707107), (-0.92388, 0, -0.382683), (-1, 0, 0), (-0.92388, 0, 0.382683), (-0.707107, 0, 0.707107), (-0.382683, 0, 0.92388), (0, 0, 1), (0.382683, 0, 0.92388), (0.707107, 0, 0.707107), (0.92388, 0, 0.382683), (1, 0, 0), (0.92388, 0, -0.382683), (0.707107, 0, -0.707107), (0.382683, 0, -0.92388), (0, 0, -1)), (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52)],
            [((-1.6, -6.4, 0), (-1.6, -1.6, 0), (-6.4, -1.6, 0), (-6.4, 1.6, 0), (-1.6, 1.6, 0), (-1.6, 6.4, 0), (1.6, 6.4, 0), (1.6, 1.6, 0), (6.4, 1.6, 0),(6.4, -1.6, 0), (1.6, -1.6, 0), (1.6, -6.4, 0), (-1.6, -6.4, 0)), (0, 4.8, 9.6, 12.8, 17.6, 22.4, 25.6, 30.4, 35.2, 38.4, 43.2, 48, 51.2)],
                            ]
        if ApplePieA_pTCIK.curveShape == 4:
            ApplePieA_pTCIK.curveShape = 0
        getlist = self.checkCurve()
        if not getlist:
            return
        cmds.undoInfo(ock=1)
        if ApplePieA_pTCIK.curveShape == 3:
            cmds.circle(n='__temp_Shape')
        else:
            cmds.curve(d=1, p=self.curSample[ApplePieA_pTCIK.curveShape][0], k=self.curSample[ApplePieA_pTCIK.curveShape][1], n='__temp_Shape')
        for i in getlist:
            cmds.connectAttr('__temp_Shape.worldSpace[0]', cmds.listRelatives(i, s=1, type="nurbsCurve")[0] + '.create', f=1)
        ApplePieA_pTCIK.curveShape += 1
        cmds.select(getlist, r=1)
        cmds.undoInfo(cck=1)
        cmds.evalDeferred("cmds.delete('__temp_Shape')")  #延迟执行

    def SelCurve(self):
        getlist = self.checkCurve()
        if not getlist:
            ui_variable['Statusbar'].showMessage(u'//未选择曲线或控制器')
            Om.MGlobal.displayError(u'//未选择曲线或控制器')
            return
        cmds.undoInfo(ock=1)
        cmds.select(cl=1)
        for i in getlist:
            if cmds.ls(i + '.ctrlName'):
                cmds.select(cmds.getAttr(i + '.ctrlName'), add=1)
            elif re.findall('_control\d*_Ctrl', i):
                cmds.select(i.split('_', 1)[0] + '_control*_Ctrl', add=1)
            else:
                return
        cmds.undoInfo(cck=1)

    def RSCurve(self, mode):
        getlist = self.checkCurve()
        if not getlist:
            return
        cmds.undoInfo(ock=1)
        cmds.select(cl=True)
        for c in getlist:
            cmds.select(c + ".controlPoints[*]", add=1)
        if mode == 'RX':
            cmds.rotate(90, 0, 0, r=1, ocp=1, os=1, xc='edge', xn=1, fo=1)
        elif mode == 'RY':
            cmds.rotate(0, 90, 0, r=1, ocp=1, os=1, xc='edge', xn=1, fo=1)
        elif mode == 'RZ':
            cmds.rotate(0, 0, 90, r=1, ocp=1, os=1, xc='edge', xn=1, fo=1)
        elif mode == 'SA':
            cmds.scale(1.2, 1.2, 1.2, r=1)
        elif mode == 'SS':
            cmds.scale(.8, .8, .8, r=1)
        cmds.select(getlist, r=1)
        cmds.undoInfo(cck=1)

    def ChangeCurveColor(self):
        ColorNum = int(ui_variable['SColorInt'].value())
        selCurve = cmds.ls(sl=1)
        cmds.undoInfo(ock=1)
        for n in range(len(selCurve)):
            CurShape = cmds.listRelatives(selCurve[n], c=1, s=1)
            cmds.setAttr(CurShape[0] + ".overrideEnabled", 1)
            cmds.setAttr(CurShape[0] + ".overrideColor", ColorNum)
        cmds.undoInfo(cck=1)

    def CurveToIK(self, curveN):   # 来自张老师
        JointNum = int(ui_variable['JointInt'].text())
        Atype = 3
        SavecurveN = curveN
        mz_dd = []
        mz_Loc = []
        for i in range(JointNum+1):
            NodemP = cmds.createNode('motionPath', n='%s_MP%s' %(curveN, i))
            cmds.setAttr(NodemP + ".fractionMode", 1)
            cmds.setAttr(NodemP + ".follow", 1)
            cmds.setAttr(NodemP + ".frontAxis", 0)
            cmds.setAttr(NodemP + ".upAxis", 1)
            cmds.setAttr(NodemP + ".worldUpType", Atype)
            B = cmds.spaceLocator(p=(0, 0, 0), n="%s_Loc%s" %(curveN, i))
            cmds.connectAttr(cmds.listRelatives(curveN, s=1)[0] + ".worldSpace[0]", NodemP + ".geometryPath", f=1)
            if cmds.objExists("%s.V%s" %(curveN, i)) == 0:
                cmds.addAttr(curveN, ln="V%s" %i, at='double', min=0, max=1, dv=0)
                cmds.setAttr("%s.V%s" %(curveN, i), e=1, k=True)
            cmds.connectAttr("%s.V%s" %(curveN, i), NodemP + ".uValue", f=1)
            cmds.setAttr("%s.V%s" %(curveN, i), 1.0 * i / JointNum)
            cmds.connectAttr(NodemP + ".allCoordinates", B[0] + ".translate", f=1)
            cmds.connectAttr(NodemP + ".rotate", B[0] + ".rotate", f=1)
            if Atype == 2:
                cmds.pathAnimation(NodemP, e=1, wuo=cmds.listRelatives(curveN, s=1)[0])
            mz_dd.append(NodemP)
            mz_Loc.append(B[0])
        cmds.select(cl=1)
        if '_Blend' in curveN:   #修改名称
            curveN = curveN.rsplit('_', 1)[0]
        Qv = cmds.xform(mz_Loc[0], q=1, ws=1, t=1)
        yt = cmds.joint(p=(Qv[0], Qv[1], Qv[2]), n=curveN + "_Jot0")
        mz_jot = []
        mz_jot.append(yt)
        for i in range(1, len(mz_Loc)):
            Qv = cmds.xform(mz_Loc[i], q=1, ws=1, t=1)
            yt = cmds.joint(p=(Qv[0], Qv[1], Qv[2]), n="%s_Jot%s" %(curveN, i))
            cmds.joint("%s_Jot%s" %(curveN, i - 1), e=1, zso=1, oj='xyz')
            mz_jot.append(yt)
        cmds.select(cl=1)
        cmds.setAttr(mz_jot[len(mz_jot) - 1] + ".jointOrientX", 0)
        cmds.setAttr(mz_jot[len(mz_jot) - 1] + ".jointOrientY", 0)
        cmds.setAttr(mz_jot[len(mz_jot) - 1] + ".jointOrientZ", 0)
        ctrlSize = self.jointCtrlNum if ui_variable['SkinCtrlbox'].isChecked() else cmds.getAttr(curveN + ".controlPoints", size=1)
        lastCtrl = "%s_control%s_Ctrl" %(curveN, ctrlSize)
        if cmds.objExists(lastCtrl + ".stretch") == 0:
            cmds.addAttr(lastCtrl, ln="stretch", at='double', min=0, max=1, dv=0)
            cmds.setAttr(lastCtrl + ".stretch", e=1, keyable=1)
        if cmds.objExists(curveN + ".scaleAttr") == 0:
            cmds.addAttr(curveN, ln="scaleAttr", at='double', dv=1)
            cmds.setAttr(curveN + ".scaleAttr", e=1, keyable=1)
        for i in range(1, len(mz_dd)):
            mz_dB = cmds.createNode('distanceBetween', n=mz_dd[i] + "_dB")
            cmds.connectAttr(mz_dd[i-1] + ".allCoordinates", mz_dd[i] + "_dB.point1", f=1)
            cmds.connectAttr(mz_dd[i] + ".allCoordinates", mz_dd[i] + "_dB.point2", f=1)
            gh = cmds.getAttr(mz_dd[i] + "_dB.distance")
            cmds.createNode('multiplyDivide', n=mz_dd[i] + "_dB_MPA")
            cmds.connectAttr(mz_dd[i] + "_dB.distance", mz_dd[i] + "_dB_MPA.input1X", f=1)
            cmds.connectAttr(curveN + ".scaleAttr", mz_dd[i] + "_dB_MPA.input2X", f=1)
            cmds.setAttr(mz_dd[i] + "_dB_MPA.operation", 2)
            cmds.createNode('blendColors', n=mz_dd[i] + "_blendC")
            cmds.connectAttr(lastCtrl + ".stretch", mz_dd[i] + "_blendC.blender", f=1)
            cmds.connectAttr(mz_dd[i] + "_dB_MPA.outputX", mz_dd[i] + "_blendC.color1R", f=1)
            cmds.setAttr(mz_dd[i] + "_blendC.color2R", gh)
            cmds.connectAttr(mz_dd[i] + "_blendC.outputR", mz_jot[i] + ".translateX", f=1)
        cmds.ikHandle(sol='ikSplineSolver', ccv=0, sj=mz_jot[0], ee=mz_jot[len(mz_jot) - 1], c=SavecurveN, n=curveN + "_SplineIkHandle")
        #cmds.select(SavecurveN)
        cmds.delete(mz_Loc)
        self.doFinish(curveN, SavecurveN)

    def doFinish(self, Name, fx):
        mainList = [Name, "%s_control*_Ctrl_grp" %Name, '%s_Jot0' %Name, '%s_SplineIkHandle' %Name]
        cluList = ['%s_clu*Handle' %Name] 
        fxList = ['%s_Blend' %Name, '%s_toFX' %Name, '%s_OutFX' %Name, '%s_onlyCtrl' %Name]
        if '_Blend' in fx:
            mainList = mainList + fxList
            cmds.setAttr(fx + '.inheritsTransform', 0)
            cmds.hide(fxList[1:-1])
        if not ui_variable['SkinCtrlbox'].isChecked():
            mainList = mainList + cluList
            cmds.hide(cluList[0])
        cmds.group(mainList, n=Name + '_allGrp')
        cmds.hide('%s_SplineIkHandle' %Name)
        if cmds.ls('buildPose') and cmds.ls('DeformationSystem'):
            cmds.setAttr('buildPose.udAttr', '%s/*addItem*/xform -os -t 0 0 0 -ro 0 0 0 \"%s_clu*Handle_Ctrl\";'
                            %(cmds.getAttr('buildPose.udAttr'), Name), type='string')

    # # # # # # # # # #
    def PoseCheck(self):
        if not cmds.ls('buildPose.udAttr'):
            ui_variable['Statusbar'].showMessage(u"//无Pose系统")
            Om.MGlobal.displayError(u"//无Pose系统")
            return
        self.buildposeText = cmds.getAttr('buildPose.udAttr')
        splitbuild = self.buildposeText.split('/*addItem*/')
        del splitbuild[0]
        splitText = [splitbuild[i].split('xform -os -t 0 0 0 -ro 0 0 0 ')[1] for i in range(len(splitbuild))]
        uiPose = 'ListA'
        if cmds.window(uiPose, q=1, ex=1):
            cmds.deleteUI(uiPose)
        cmds.window(uiPose, t='List')
        cmds.columnLayout(rs=5)
        cmds.textScrollList('textList', nr=20, shi=4)
        cmds.button('Add', l="Add", h=28, w=100, c=lambda*args: self.PoseEdit('add'))
        cmds.button('Delete', l="Delete", h=28, w=100, c=lambda*args: self.PoseEdit('delete'))
        cmds.showWindow(uiPose)
        ls = cmds.ls(type='transform')
        for i in splitText:
            self.editi = (i.split('_clu*Handle_Ctrl\";')[0]).split('\"', 1)[1]   \
                if '_clu*Handle_Ctrl' in i else (i.split('\"', 1)[1]).rsplit('\"', 1)[0]
            if self.editi in ls:
                cmds.textScrollList('textList', e=1, a=i)
            else:
                cmds.textScrollList('textList', e=1, a=i + '  //NeedDelete//')

    def PoseEdit(self, mode):
        if mode == 'delete':
            poseSplit = self.buildposeText.split('/*addItem*/xform -os -t 0 0 0 -ro 0 0 0 %s;'
                            %(cmds.textScrollList('textList', q=1, si=1)[0].split(';')[0]))
            cmds.setAttr('buildPose.udAttr', poseSplit[0] + poseSplit[1], typ='string')
            cmds.textScrollList('textList', e=1, rii=cmds.textScrollList('textList', q=1, sii=1)[0])
        elif mode == 'add':
            if cmds.promptDialog(t='addPose', b=['OK', 'Cancel'], db='OK', cb='Cancel', ds='Cancel') == 'OK':
                inputText = cmds.promptDialog(q=True, t=True)
                lsinput = cmds.ls(inputText)
                if not lsinput:
                    cmds.error('无此物体')
                elif len(lsinput) >= 2:
                    cmds.error('有重复物体')
                cmds.setAttr('buildPose.udAttr', 
                    cmds.getAttr('buildPose.udAttr') + '/*addItem*/xform -os -t 0 0 0 -ro 0 0 0 \"' + inputText + '\";', typ='string')
                cmds.textScrollList('textList', e=1, a='\"' + inputText + '\";')
    # # # # # # # # # #

class ApplePieA_Dynamic(object):

    def Acondition(self):
        if ui_variable['SelectHairSystem'].currentText() != 'Create New':
            ui_variable['SelectNucleus'].setEnabled(False)
        else:
            ui_variable['SelectNucleus'].setEnabled(True)

    def Ready_GetNode(self, mode):
        if mode == 'HairSystem':
            ui_variable['SelectHairSystem'].clear()
            hairsystemitem = cmds.listRelatives(cmds.ls(typ='hairSystem'), p=1)
            if hairsystemitem:
                for i in hairsystemitem:
                    ui_variable['SelectHairSystem'].addItem(i)
            ui_variable['SelectHairSystem'].addItem('Create New')
        if mode == 'Nucleus':
            ui_variable['SelectNucleus'].clear()
            nucleusitem = cmds.ls(typ='nucleus')
            if nucleusitem:
                for i in nucleusitem:
                    ui_variable['SelectNucleus'].addItem(i)
            ui_variable['SelectNucleus'].addItem('Create New')

    def ifdef(self, mode=''):
        qComboBox = []
        qComboBox.append(ui_variable['SelectNucleus'].currentText())
        qComboBox.append(ui_variable['SelectHairSystem'].currentText())
        if mode == 'NC':
            qComboBox[0] = cmds.createNode('nucleus')
            cmds.connectAttr('time1.outTime', qComboBox[0] + ".currentTime")
            if cmds.upAxis(q=1, axis=1) == "z":
                cmds.setAttr(qComboBox[0] + ".gravityDirection", 0, 0, -1)
        if mode == 'NC' or mode == 'HC':
            qComboBox[1] = cmds.createNode('hairSystem')
            cmds.setAttr(qComboBox[1] + ".hairsPerClump", 1)
            cmds.setAttr(qComboBox[1] + ".clumpWidth", 0)
            cmds.parent(cmds.listRelatives(qComboBox[1], p=1)[0], qComboBox[0])
        if not cmds.connectionInfo(qComboBox[1] + ".nextState", sfd=1):
            mel.eval('addActiveToNSystem("%s", "%s")' %(cmds.listRelatives(qComboBox[1], p=1)[0], qComboBox[0]))
            cmds.connectAttr( 'time1.outTime', qComboBox[1] + '.currentTime', f=1)
            cmds.connectAttr(qComboBox[0] + '.startFrame', qComboBox[1] + '.startFrame', f=1)
            qComboBox[1] = cmds.listRelatives(qComboBox[1], p=1)[0]
        if cmds.listAttr(qComboBox[1], st='ctrlMode'):
            reverseNode = cmds.listConnections(qComboBox[1], c=1, t='reverse')
            if not reverseNode:
                self.reNode = cmds.createNode("reverse")
                cmds.connectAttr(qComboBox[1] + ".ctrlMode", self.reNode + ".inputX")
            else:
                self.reNode = reverseNode[-1]
        else:
            cmds.addAttr(qComboBox[1], ln="ctrlMode", at="enum", en="onlyCtrl:FX:")
            cmds.setAttr(qComboBox[1] + ".ctrlMode", e=1, keyable=1)
            modeNode = cmds.createNode("multiplyDivide")
            cmds.setAttr(modeNode+".input2X", 4)
            cmds.connectAttr(qComboBox[1] + ".ctrlMode", modeNode + ".input1X", f=1)
            cmds.connectAttr(modeNode + ".outputX", qComboBox[1] + ".simulationMethod", f=1)
            cmds.setAttr(qComboBox[1]+".ctrlMode", 1)
            self.reNode = cmds.createNode("reverse")
            cmds.connectAttr(qComboBox[1] + ".ctrlMode", self.reNode+".inputX")
        return qComboBox

    def FXCurve(self, curve):
        if not curve:
            ui_variable['Statusbar'].showMessage(u"//未选取曲线")
            Om.MGlobal.displayError(u"//未选取曲线")
            return
        cmds.undoInfo(ock=1)
        qComboBox = []
        if ui_variable['SelectNucleus'].currentText() != 'Create New' and not cmds.ls(typ='nucleus'):
            self.Ready_GetNode('Nucleus')
        if ui_variable['SelectNucleus'].currentText() == 'Create New':
            qComboBox = self.ifdef('NC')
        elif ui_variable['SelectHairSystem'].currentText() == 'Create New':
            qComboBox = self.ifdef('HC')
        else:
            qComboBox = self.ifdef()
        _tempctrlMode = cmds.getAttr(qComboBox[1] + ".ctrlMode")
        cmds.setAttr(qComboBox[1] + ".ctrlMode", 1)
        for i in range(len(curve)):
            c = curve[i]
            hairfollicle = cmds.createNode('follicle')
            cmds.setAttr(hairfollicle + ".pointLock", 1)
            cmds.setAttr(hairfollicle + ".restPose", 1)
            cmds.setAttr(hairfollicle + ".startDirection", 1)
            cmds.setAttr(hairfollicle + ".degree", 3)
            _follicletransform = cmds.listRelatives(hairfollicle, p=1)[0]
            cmds.setAttr(_follicletransform + '.v', 0)
            cmds.parent(_follicletransform, qComboBox[1])
            hairNum = cmds.listConnections(qComboBox[1] + '.outputHair')
            if not hairNum:
                cmds.connectAttr(qComboBox[1] + '.outputHair[0]', hairfollicle + '.currentPosition', f=1)
                cmds.connectAttr(hairfollicle + '.outHair', qComboBox[1] + '.inputHair[0]', f=1)
            else:
                cmds.connectAttr('%s.outputHair[%s]' %(qComboBox[1], len(hairNum)), hairfollicle + '.currentPosition', f=1)
                cmds.connectAttr(hairfollicle + '.outHair', '%s.inputHair[%s]' %(qComboBox[1], len(hairNum)), f=1)
            cmds.rename(cmds.rebuildCurve(c, ch=1, rpo=0, rt=0, end=1, kr=0, kcp=0, kep=1, kt=0, 
                        s=cmds.getAttr(c + ".controlPoints", size=1) + 5, d=3, tol=0.01)[0], c + '_toFX')
            cmds.duplicate(c, rr=1, n=c + '_onlyCtrl')
            cmds.duplicate(c + '_toFX', rr=1, n=c + '_Blend')
            cmds.connectAttr(cmds.listRelatives(c + '_toFX', s=1)[0] + '.worldSpace[0]', cmds.listRelatives(c + '_onlyCtrl',s=1)[0] + '.create', f=1)
            cmds.parent(c + '_toFX', cmds.listRelatives(hairfollicle, p=1))
            cmds.connectAttr(cmds.listRelatives(c + '_toFX', s=1, type='nurbsCurve')[0] + '.local', hairfollicle + '.startPosition', f=1)
            cmds.connectAttr(c + '_toFX.worldMatrix[0]', hairfollicle+'.startPositionMatrix', f=1)
            cmds.connectAttr(hairfollicle + '.outCurve', cmds.duplicate(c, rr=1, n=c + '_OutFX')[0] + 'Shape.create', f=1)
            cmds.blendShape(c + '_OutFX', c + '_onlyCtrl', c + '_Blend', n=c + '_curveBS')
            cmds.connectAttr(qComboBox[1] + '.ctrlMode', '%s_curveBS.%s_OutFX' %(c, c))
            cmds.connectAttr(self.reNode + ".outputX", '%s_curveBS.%s_onlyCtrl' %(c, c))
        ApplePieA_Dynamic().Ready_GetNode('HairSystem')
        ApplePieA_Dynamic().Ready_GetNode('Nucleus')
        cmds.setAttr(qComboBox[1] + ".ctrlMode", _tempctrlMode)
        cmds.undoInfo(cck=1)

Ui_ApplePieA()
