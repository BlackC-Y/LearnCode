try:
    from PySide2 import QtCore, QtGui, QtWidgets
    import shiboken2
except ImportError:   #316行兼容问题
    from PySide import QtGui as QtWidgets
    from PySide import QtCore
    import shiboken as shiboken2
from maya import cmds, mel
import maya.OpenMaya as Om
import maya.OpenMayaUI as Omui


'''
def pTCIK():
    uiA = 'ApplePieA_testA'
    try:
        cmds.deleteUI(uiA)
    except:
        pass

    cmds.window(uiA, t=('v1.0'), menuBar=True)
    tabs = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5)

    child1 = cmds.columnLayout(cat=("both", 2), rowSpacing=5, columnWidth=250)
    cmds.intFieldGrp('RebuildIntFieldGrp', h=28, label='重建段数', cw2=(80, 100))
    cmds.textFieldGrp('CurveNameTextFieldGrp', h=28,label="曲线名称", cw2=(80, 100))
    cmds.text(label="有曲线名才可操作") 
    cmds.button('Next1Button', l="选模型的线", h=28,c=lambda*args: ApplePieA_pTCIK().SelectPolyCurve())
    cmds.flowLayout(columnSpacing=45)
    cmds.text(l="")
    cmds.text(l="调整曲线", h=28)
    cmds.button('reverseCurveButton', l="反转曲线", h=28, w=80,c=lambda*args: ApplePieA_pTCIK().reverseCurve())
    cmds.setParent('..')
    cmds.button('createCluAndCtrlButton', l="创建簇和控制器", h=28,c=lambda*args: ApplePieA_pTCIK().createCluAndCtrl())
    #cmds.button('CurveToolsButton', l="曲线工具(可选)", h=28,c=lambda*args: ApplePieA_pTCIK().CurveTools())
    cmds.button('parentConButton', l="约束控制", h=28,c=lambda*args: ApplePieA_pTCIK().parentConstraintCurve())
    cmds.flowLayout(columnSpacing=25)
    cmds.button('ParentButton', l="控制器层级化", h=28,w=110,c=lambda*args: ApplePieA_pTCIK().CurveParent(''))
    cmds.button('ReParentButton', l="解开层级", h=28,w=110,c=lambda*args: ApplePieA_pTCIK().CurveParent('reverse'))
    cmds.setParent('..')
    cmds.intFieldGrp('IKJointIntFieldGrp', h=28, label="骨骼段数:", cw2=(80, 100))
    cmds.button('ToIKButton', l="建立IK", h=28,c=lambda*args: ApplePieA_pTCIK().CurveToIK())
    cmds.setParent('..')

    child2 = cmds.columnLayout(cat=("both", 2), rowSpacing=5, columnWidth=250)
    cmds.flowLayout(columnSpacing=3)
    cmds.button('CShapeButton',l='换个形状',h=28,w=123,c=lambda*args: ApplePieA_pTCIK().cShape())
    cmds.button('TangentButton', l="切线对齐", h=28,w=123,c=lambda*args: ApplePieA_pTCIK().Tangent())
    cmds.setParent('..')
    cmds.button('SelButton', l="选择当前曲线的线圈",h=28, c=lambda*args: ApplePieA_pTCIK().SelCurve())
    cmds.flowLayout(columnSpacing=3)
    cmds.button('RotXButton', l="X旋转", h=28,w=80, c=lambda*args: ApplePieA_pTCIK().RSCurve('RX'))
    cmds.button('RotYButton', l="Y旋转", h=28,w=80, c=lambda*args: ApplePieA_pTCIK().RSCurve('RY'))
    cmds.button('RotZButton', l="Z旋转", h=28,w=80, c=lambda*args: ApplePieA_pTCIK().RSCurve('RZ'))
    cmds.setParent('..')
    cmds.flowLayout(columnSpacing=3)
    cmds.button('ScaleAddButton', l="放大曲线", h=28,w=123,c=lambda*args: ApplePieA_pTCIK().RSCurve('SA'))
    cmds.button('ScaleSubButton', l="缩小曲线", h=28,w=123,c=lambda*args: ApplePieA_pTCIK().RSCurve('SS'))
    cmds.setParent('..')
    cmds.canvas('CCanvas', rgbValue=(0, 0, 0),width=100, height=20)  # 颜色显示框 和下行滑条组合
    cmds.intSliderGrp('SColorIntSliderGrp', minValue=1,maxValue=31, dc=lambda*args: ApplePieA_pTCIK().SColor())  # 单行滑条 和上行组合
    # cmds.colorIndexSliderGrp('curveColorIntFieldGrp',min=1,max=32)   #单行颜色滑条
    cmds.button('ChangeCurveColorButton', l="变更颜色", h=28, c=lambda*args: ApplePieA_pTCIK().ChangeCurveColor())
    cmds.setParent('..')

    child3 = cmds.columnLayout(cat=("both", 2), rowSpacing=5, columnWidth=250)
    cmds.flowLayout(columnSpacing=3)
    cmds.textFieldGrp('FXCurveNameTextFieldGrp',h=28,label="曲线名", cw2=(60, 100),ed=0)
    cmds.button('InputCurve',l="拾取曲线",h=28,w=50,c=lambda*args: ApplePieA_Dynamic().Ready_selectCurve())
    cmds.setParent('..')
    cmds.flowLayout(columnSpacing=3)
    pTCIK.HairSystemMenu = cmds.optionMenuGrp('HairSystemMenu',label='HairSystem',cw2=(60,100))
    ApplePieA_Dynamic().Ready_hairSystem()
    cmds.button('shuaxin',l='刷新',h=28,w=25,c=lambda*args: ApplePieA_Dynamic().Ready_hairSystem())
    cmds.button('nucleusSelect',l="->",h=28,w=25,c=lambda*args: ApplePieA_Dynamic().Ready(3))
    cmds.setParent('..')
    
    cmds.button('RunButton', l="创建动力学曲线", h=28,w=123,c=lambda*args: ApplePieA_pTCIK().FXCurve())
    cmds.setParent('..')
    
    cmds.tabLayout( tabs, edit=True, tabLabel=((child1,'本体'),(child2,'曲线DLC'),(child3,'动力学曲线')))
    cmds.window(uiA, e=True, wh=(260, 500))  # 窗口后定值
    cmds.showWindow(uiA)
'''

ui_variable = {}
_pTCIKVerision = 'v2.2.2'

class Ui_ApplePieA(object):

    def setupUi(self, ApplePieA):
        try:
            pTCIKui.close()
            # QtGui.QWidgetAction.deleteWidget("ApplePieA")
        except:
            pass
        ApplePieA.setObjectName("ApplePieA")
        #ApplePieA.resize(260, 500)
        ApplePieA.setFixedSize(260, 500)
        self.tabWidget = QtWidgets.QTabWidget(ApplePieA)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 260, 480))
        self.tabWidget.setObjectName("tabWidget")
        self.child1 = QtWidgets.QWidget()
        self.child1.setObjectName("child1")
        self.verticalLayoutAWidget = QtWidgets.QWidget(self.child1)
        self.verticalLayoutAWidget.setGeometry(QtCore.QRect(5, 5, 245, 300))
        self.verticalLayoutAWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayoutA = QtWidgets.QVBoxLayout(self.verticalLayoutAWidget)
        self.verticalLayoutA.setSpacing(3)
        self.verticalLayoutA.setContentsMargins(0, 0, 0, 0)
        self.verticalLayoutA.setObjectName("verticalLayout")
        self.horizontalLayoutA = QtWidgets.QHBoxLayout()
        self.horizontalLayoutA.setObjectName("horizontalLayout")
        self.RebuildIntText = QtWidgets.QLabel(self.verticalLayoutAWidget)
        self.RebuildIntText.setMaximumSize(QtCore.QSize(50, 20))
        self.RebuildIntText.setObjectName("RebuildIntText")
        self.horizontalLayoutA.addWidget(self.RebuildIntText)
        ui_variable['RebuildInt'] = self.RebuildInt = QtWidgets.QLineEdit(self.verticalLayoutAWidget)
        self.RebuildInt.setMaximumSize(QtCore.QSize(100, 20))
        self.RebuildInt.setObjectName("RebuildInt")
        self.horizontalLayoutA.addWidget(self.RebuildInt)
        self.verticalLayoutA.addLayout(self.horizontalLayoutA)
        self.horizontalLayoutB = QtWidgets.QHBoxLayout()
        self.horizontalLayoutB.setObjectName("horizontalLayout")
        self.CurveNameText = QtWidgets.QLabel(self.verticalLayoutAWidget)
        self.CurveNameText.setMaximumSize(QtCore.QSize(50, 20))
        self.CurveNameText.setObjectName("CurveNameText")
        self.horizontalLayoutB.addWidget(self.CurveNameText)
        self.verticalLayoutA.addLayout(self.horizontalLayoutB)
        ui_variable['CurveName'] = self.CurveName = QtWidgets.QLineEdit(self.verticalLayoutAWidget)
        self.CurveName.setMaximumSize(QtCore.QSize(100, 20))
        self.CurveName.setObjectName("CurveName")
        self.horizontalLayoutB.addWidget(self.CurveName)
        #self.CurveNameWar = QtWidgets.QLabel(self.verticalLayoutAWidget)
        # self.CurveNameWar.setAlignment(QtCore.Qt.AlignCenter)
        # self.CurveNameWar.setStyleSheet("color:yellow")
        #self.CurveNameWar.setMaximumSize(QtCore.QSize(245, 20))
        # self.CurveNameWar.setObjectName("CurveNameWar")
        # self.verticalLayoutA.addWidget(self.CurveNameWar)
        self.horizontalLayoutC = QtWidgets.QHBoxLayout()
        self.horizontalLayoutC.setObjectName("horizontalLayout")
        self.SelectPolyCurve = QtWidgets.QPushButton(self.verticalLayoutAWidget)
        self.SelectPolyCurve.setObjectName("SelectPolyCurve")
        self.horizontalLayoutC.addWidget(self.SelectPolyCurve)
        self.reverseCurve = QtWidgets.QPushButton(self.verticalLayoutAWidget)
        self.reverseCurve.setObjectName("reverseCurve")
        self.horizontalLayoutC.addWidget(self.reverseCurve)
        self.verticalLayoutA.addLayout(self.horizontalLayoutC)
        self.lineA = QtWidgets.QFrame(self.verticalLayoutAWidget)
        self.lineA.setFrameShape(QtWidgets.QFrame.HLine)
        self.lineA.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.lineA.setObjectName("line")
        self.verticalLayoutA.addWidget(self.lineA)
        self.horizontalLayout0 = QtWidgets.QHBoxLayout()
        self.horizontalLayout0.setObjectName("horizontalLayout")
        ui_variable['CtrlParentbox'] = self.CtrlParentbox = QtWidgets.QCheckBox(self.verticalLayoutAWidget)
        self.CtrlParentbox.setMaximumSize(QtCore.QSize(100, 20))
        self.CtrlParentbox.setObjectName("CtrlParentbox")
        # self.CtrlParentbox.setChecked(True)
        self.horizontalLayout0.addWidget(self.CtrlParentbox)
        ui_variable['IKjointbox'] = self.IKjointbox = QtWidgets.QCheckBox(self.verticalLayoutAWidget)
        self.IKjointbox.setMaximumSize(QtCore.QSize(80, 20))
        self.IKjointbox.setObjectName("IKjointbox")
        self.horizontalLayout0.addWidget(self.IKjointbox)
        self.verticalLayoutA.addLayout(self.horizontalLayout0)
        self.horizontalLayout1 = QtWidgets.QHBoxLayout()
        self.horizontalLayout1.setObjectName("horizontalLayout")
        ui_variable['FXCurvebox'] = self.FXCurvebox = QtWidgets.QCheckBox(self.verticalLayoutAWidget)
        self.FXCurvebox.setMaximumSize(QtCore.QSize(80, 20))
        self.FXCurvebox.setObjectName("FXCurvebox")
        self.horizontalLayout1.addWidget(self.FXCurvebox)
        ui_variable['OnlyFXCurvebox'] = self.OnlyFXCurvebox = QtWidgets.QCheckBox(self.verticalLayoutAWidget)
        self.OnlyFXCurvebox.setMaximumSize(QtCore.QSize(100, 20))
        self.OnlyFXCurvebox.setObjectName("FXCurvebox")
        self.horizontalLayout1.addWidget(self.OnlyFXCurvebox)
        self.verticalLayoutA.addLayout(self.horizontalLayout1)
        #self.selectboxGrp = QtWidgets.QButtonGroup(self.verticalLayoutAWidget)
        # self.selectboxGrp.addButton(self.selectboxA,11)
        # self.selectboxGrp.addButton(self.selectboxB,12)
        self.horizontalLayoutD = QtWidgets.QHBoxLayout()
        self.horizontalLayoutD.setObjectName("horizontalLayout")
        self.JointIntText = QtWidgets.QLabel(self.verticalLayoutAWidget)
        self.JointIntText.setMaximumSize(QtCore.QSize(60, 20))
        self.JointIntText.setObjectName("JointIntText")
        self.horizontalLayoutD.addWidget(self.JointIntText)
        ui_variable['JointInt'] = self.JointInt = QtWidgets.QLineEdit(self.verticalLayoutAWidget)
        self.JointInt.setMaximumSize(QtCore.QSize(100, 20))
        self.JointInt.setObjectName("JointInt")
        self.horizontalLayoutD.addWidget(self.JointInt)
        self.verticalLayoutA.addLayout(self.horizontalLayoutD)
        self.horizontalLayoutE = QtWidgets.QHBoxLayout()
        self.horizontalLayoutE.setObjectName("horizontalLayout")
        self.HairSystemText = QtWidgets.QLabel(self.verticalLayoutAWidget)
        self.HairSystemText.setMaximumSize(QtCore.QSize(60, 20))
        self.HairSystemText.setObjectName("HairSystemText")
        self.horizontalLayoutE.addWidget(self.HairSystemText)
        ui_variable['SelectHairSystem'] = self.SelectHairSystem = QtWidgets.QComboBox(self.verticalLayoutAWidget)
        self.SelectHairSystem.setObjectName("SelectHairSystem")
        self.SelectHairSystem.setMaximumSize(QtCore.QSize(100, 20))
        self.SelectHairSystem.installEventFilter(self)
        self.horizontalLayoutE.addWidget(self.SelectHairSystem)
        self.verticalLayoutA.addLayout(self.horizontalLayoutE)
        self.horizontalLayoutF = QtWidgets.QHBoxLayout()
        self.horizontalLayoutF.setObjectName("horizontalLayout")
        self.NucleusText = QtWidgets.QLabel(self.verticalLayoutAWidget)
        self.NucleusText.setMaximumSize(QtCore.QSize(60, 20))
        self.NucleusText.setObjectName("NucleusText")
        self.horizontalLayoutF.addWidget(self.NucleusText)
        ui_variable['SelectNucleus'] = self.SelectNucleus = QtWidgets.QComboBox(self.verticalLayoutAWidget)
        self.SelectNucleus.setObjectName("SelectNucleus")
        self.SelectNucleus.setMaximumSize(QtCore.QSize(100, 20))
        self.SelectNucleus.installEventFilter(self)
        self.horizontalLayoutF.addWidget(self.SelectNucleus)
        self.verticalLayoutA.addLayout(self.horizontalLayoutF)
        self.BuildCtrl = QtWidgets.QPushButton(self.verticalLayoutAWidget)
        self.BuildCtrl.setObjectName("BuildCtrl")
        self.verticalLayoutA.addWidget(self.BuildCtrl)
        self.PoseEdit = QtWidgets.QPushButton(self.child1)
        self.PoseEdit.setGeometry(QtCore.QRect(160, 430, 100, 28))
        self.PoseEdit.setObjectName("PoseEdit")
        self.tabWidget.addTab(self.child1, "")

        self.child2 = QtWidgets.QWidget()
        self.child2.setObjectName("child2")
        self.verticalLayoutBWidget = QtWidgets.QWidget(self.child2)
        self.verticalLayoutBWidget.setGeometry(QtCore.QRect(5, 5, 245, 230))
        self.verticalLayoutBWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayoutB = QtWidgets.QVBoxLayout(self.verticalLayoutBWidget)
        self.verticalLayoutB.setSpacing(3)
        self.verticalLayoutB.setContentsMargins(0, 0, 0, 0)
        self.verticalLayoutB.setObjectName("verticalLayout")
        self.SellastCurve = QtWidgets.QPushButton(self.verticalLayoutBWidget)
        self.SellastCurve.setObjectName("SellastCurve")
        self.verticalLayoutB.addWidget(self.SellastCurve)
        self.CShape = QtWidgets.QPushButton(self.verticalLayoutBWidget)
        self.CShape.setObjectName("CShape")
        self.verticalLayoutB.addWidget(self.CShape)
        self.horizontalLayoutF = QtWidgets.QHBoxLayout()
        self.horizontalLayoutF.setObjectName("horizontalLayout")
        self.horizontalLayoutF.setSpacing(3)
        self.RotX = QtWidgets.QPushButton(self.verticalLayoutBWidget)
        self.RotX.setObjectName("RotX")
        self.horizontalLayoutF.addWidget(self.RotX)
        self.RotY = QtWidgets.QPushButton(self.verticalLayoutBWidget)
        self.RotY.setObjectName("RotY")
        self.horizontalLayoutF.addWidget(self.RotY)
        self.RotZ = QtWidgets.QPushButton(self.verticalLayoutBWidget)
        self.RotZ.setObjectName("RotZ")
        self.horizontalLayoutF.addWidget(self.RotZ)
        self.verticalLayoutB.addLayout(self.horizontalLayoutF)
        self.horizontalLayoutG = QtWidgets.QHBoxLayout()
        self.horizontalLayoutG.setObjectName("horizontalLayout")
        self.horizontalLayoutG.setSpacing(3)
        self.ScaleAdd = QtWidgets.QPushButton(self.verticalLayoutBWidget)
        self.ScaleAdd.setObjectName("ScaleAdd")
        self.horizontalLayoutG.addWidget(self.ScaleAdd)
        self.ScaleSub = QtWidgets.QPushButton(self.verticalLayoutBWidget)
        self.ScaleSub.setObjectName("ScaleSub")
        self.horizontalLayoutG.addWidget(self.ScaleSub)
        self.verticalLayoutB.addLayout(self.horizontalLayoutG)
        self.horizontalLayoutH = QtWidgets.QHBoxLayout()
        self.horizontalLayoutH.setObjectName("horizontalLayout")
        self.horizontalLayoutH.setSpacing(3)
        ui_variable['SColorview'] = self.SColorview = QtWidgets.QPushButton(self.verticalLayoutBWidget)
        self.SColorview.setMinimumSize(QtCore.QSize(80, 20))
        self.SColorview.setObjectName("SColorview")
        self.horizontalLayoutH.addWidget(self.SColorview)
        ui_variable['SColorInt'] = self.SColorInt = QtWidgets.QSlider(self.verticalLayoutBWidget)
        self.SColorInt.setMinimum(1)
        self.SColorInt.setMaximum(31)
        self.SColorInt.setOrientation(QtCore.Qt.Horizontal)
        self.SColorInt.setObjectName("SColorInt")
        self.horizontalLayoutH.addWidget(self.SColorInt)
        self.verticalLayoutB.addLayout(self.horizontalLayoutH)
        self.ChangeColor = QtWidgets.QPushButton(self.verticalLayoutBWidget)
        self.ChangeColor.setObjectName("ChangeColor")
        self.verticalLayoutB.addWidget(self.ChangeColor)
        self.tabWidget.addTab(self.child2, "")

        ui_variable['Statusbar'] = self.Statusbar = QtWidgets.QStatusBar(ApplePieA)
        self.Statusbar.setStyleSheet("color:yellow")
        self.Statusbar.setGeometry(QtCore.QRect(0, 475, 260, 28))
        self.Statusbar.setObjectName("Statusbar")

        self.retranslateUi(ApplePieA)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(ApplePieA)
        ApplePieA_Dynamic().Ready_GetNode('HairSystem')
        ApplePieA_Dynamic().Ready_GetNode('Nucleus')

    def retranslateUi(self, ApplePieA):
        ApplePieA.setWindowTitle(u"ApplePieA")
        self.RebuildIntText.setText(u"重建段数")
        self.RebuildInt.setPlaceholderText(u"重建段数")
        self.CurveNameText.setText(u"曲线名")
        self.CurveName.setPlaceholderText(u"曲线名")
        self.SelectPolyCurve.setText(u"选模型的线")
        self.SelectPolyCurve.clicked.connect(lambda *args: ApplePieA_pTCIK().SelectPolyCurve())
        self.reverseCurve.setText(u"反转曲线")
        self.reverseCurve.clicked.connect(lambda *args: ApplePieA_pTCIK().reverseCurve())
        self.CtrlParentbox.setText(u"控制器层级化")
        self.IKjointbox.setText(u'建立IK骨骼')
        self.FXCurvebox.setText(u"添加动力学")
        self.OnlyFXCurvebox.setText(u"仅动力学曲线")
        self.OnlyFXCurvebox.clicked.connect(lambda: self.setdisable())
        self.JointIntText.setText(u"骨骼段数")
        self.HairSystemText.setText(u"HairSystem")
        self.SelectHairSystem.currentTextChanged.connect(lambda *args: ApplePieA_Dynamic().Acondition())
        self.NucleusText.setText(u"Nucleus")
        self.SelectNucleus.currentTextChanged.connect(lambda *args: ApplePieA_Dynamic().Acondition())
        self.BuildCtrl.setText(u"Build")
        self.BuildCtrl.clicked.connect(lambda *args: ApplePieA_pTCIK().createCtrl())
        self.PoseEdit.setText(u"PoseEdit_ADV")
        self.PoseEdit.clicked.connect(lambda *args: ApplePieA_pTCIK().PoseCheck())
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.child1), u"本体")

        self.SellastCurve.setText(u'选择最后一次生成的控制器')
        self.SellastCurve.clicked.connect(lambda *args: ApplePieA_pTCIK().SelCurve())
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
        self.SColorInt.valueChanged.connect(lambda*args: ApplePieA_pTCIK().SColor())
        self.ChangeColor.setText(u"改变颜色")
        self.ChangeColor.clicked.connect(lambda *args: ApplePieA_pTCIK().ChangeCurveColor())
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.child2), u"曲线DLC")

    def eventFilter(self, object, event):
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
            self.CtrlParentbox.setEnabled(False)
            self.IKjointbox.setEnabled(False)
            self.FXCurvebox.setEnabled(False)
            self.JointInt.setEnabled(False)
            self.JointIntText.setEnabled(False)
        else:
            self.CtrlParentbox.setEnabled(True)
            self.IKjointbox.setEnabled(True)
            self.FXCurvebox.setEnabled(True)
            self.JointInt.setEnabled(True)
            self.JointIntText.setEnabled(True)


class Showwindow(Ui_ApplePieA, QtWidgets.QWidget):

    def __init__(self):
        super(Showwindow, self).__init__()
        self.setupUi(self)
        self.setParent(shiboken2.wrapInstance(long(Omui.MQtUtil.mainWindow()), QtWidgets.QMainWindow))
        self.setWindowFlags(QtCore.Qt.Window)
        # self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)   #置顶
        self.setWindowTitle('pTCIK by_Y')
        ui_variable['Statusbar'].showMessage(_pTCIKVerision)
        self.show()

class ApplePieA_pTCIK(object):

    curveShape = 0

    def __init__(self):
        self.Curvename = ui_variable['CurveName'].text()

    def SelectPolyCurve(self):
        ReBNum = ui_variable['RebuildInt'].text()
        if not ReBNum:
            ui_variable['Statusbar'].showMessage(u'//没填重建段数')
            Om.MGlobal.displayError(u'//没填重建段数')
            return
        if not self.Curvename:
            ui_variable['Statusbar'].showMessage(u"//没填曲线名")
            Om.MGlobal.displayError(u"//没填曲线名")
            return
        #ReBNum = cmds.intFieldGrp('RebuildIntFieldGrp', q=True, v1=True)
        polyEdgeN = cmds.ls(sl=True)
        Namelist = cmds.ls()
        # bothName = cmp(Curvename,Namelist)  #对比名称
        if self.Curvename in Namelist:
            ui_variable['Statusbar'].showMessage(u"//名称冲突")
            Om.MGlobal.displayError(u"//名称冲突")
            return
        '''     #列表对比
		for A in L1:
			if A in L2:
		'''
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
            cl = cmds.ls('__temp_clu*Handle')
            node_p = {}
            for c in range(len(cl)):
                temp_node = cmds.createNode('nearestPointOnCurve', n='__temp_node')
                cmds.connectAttr('__temp_cur.worldSpace[0]', temp_node + '.inputCurve')
                if c == 0:
                    cmds.connectAttr('__temp_cluHandleShape.origin', temp_node + '.inPosition')
                else:
                    cmds.connectAttr('__temp_clu%sHandleShape.origin', temp_node + '.inPosition' %str(c))
                node_p[c] = cmds.getAttr(temp_node + '.parameter')
            node_p_list = sorted(node_p.items(), key=lambda item: item[1]) # 字典排序
            tcws = [[0 for y in range(3)] for x in range(len(selv))]
            for v in range(len(selv)):
                if node_p_list[v][0] == 0:
                    c = ''
                else:
                    c = node_p_list[v][0]
                tcws[v][0] = cmds.getAttr('__temp_clu%sHandleShape.originX' %str(c))
                tcws[v][1] = cmds.getAttr('__temp_clu%sHandleShape.originY' %str(c))
                tcws[v][2] = cmds.getAttr('__temp_clu%sHandleShape.originZ' %str(c))
            cmds.curve(p=tcws, n=self.Curvename)
            reshape = cmds.listRelatives(self.Curvename, s=1)
            cmds.rename(reshape, self.Curvename + 'Shape')
            cmds.delete('__temp_*')
        else:
            cmds.select(polyEdgeN, r=1)
            pTCname = cmds.polyToCurve(ch=0, form=2, degree=3)
            cmds.rename(pTCname[0], self.Curvename)
        cmds.rebuildCurve(self.Curvename, ch=0, rpo=1, rt=0, end=1, kr=0, kcp=0, kep=1, kt=0, s=int(ReBNum), d=3, tol=0.01)
        cvSize = cmds.getAttr(self.Curvename + ".controlPoints", size=1)
        cmds.delete(self.Curvename + '.cv[1]', self.Curvename + '.cv[%s]' %str(cvSize-2))
        cmds.setAttr(self.Curvename + ".dispCV", 1)
        cmds.undoInfo(cck=1)

    def checkCurve(self):
        curlist = cmds.ls(sl=1)
        #if not cmds.listRelatives(curlist, s=1, type='nurbsCurve'):
        #    ui_variable['Statusbar'].showMessage(u"//未选择曲线")
        #    Om.MGlobal.displayError(u"//未选择曲线")
        #    return
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
        if cmds.ls('tempCurveName'):
            cmds.setAttr('tempCurveName.CurName', '', type='string')
        else:
            cmds.createNode('dagPose', n='tempCurveName')
            cmds.addAttr('tempCurveName', ln='CurName', dt='string')
            cmds.setAttr('tempCurveName.CurName', '', type='string')
        for i in getlist:
            cmds.setAttr(i + ".dispCV", 0)
            cmds.DeleteHistory(i)
            curve = cmds.listRelatives(i, s=1, type="nurbsCurve")[0]
            numCVs = cmds.getAttr(i + ".controlPoints", size=1)
            for nu in range(numCVs):
                createClu = cmds.cluster(curve + '.cv[%s]' %(nu), n=i + '_clu', rel=1)[1]
                createCur = cmds.circle(ch=0, n=createClu + "_Ctrl")[0]
                cmds.group(n=createCur+"_SDK")
                ctrlgroup = cmds.group(n=createCur+"_grp")
                cmds.connectAttr(createClu + "Shape.origin", ctrlgroup + ".translate", f=1)
                cmds.disconnectAttr(createClu + "Shape.origin", ctrlgroup + ".translate")
                cmds.select(cl=1)
            cmds.setAttr('tempCurveName.CurName', '%s_clu*Handle_Ctrl,' %(cmds.getAttr('tempCurveName.CurName') + i), type='string' )
        cmds.select(getlist, r=1)
        self.Tangent()
        self.parentConstraintCurve()
        if ui_variable['CtrlParentbox'].isChecked():
            self.CurveParent()
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

    def Tangent(self):
        getlist = self.checkCurve()
        if not getlist:
            return
        for i in getlist:
            cvSize = cmds.getAttr(i+".controlPoints", size=1)
            Tangentgrp = ''
            for r in range(cvSize,):
                if r == 0:
                    Tangentgrp = (i+"_cluHandle_Ctrl_grp")
                else:
                    Tangentgrp = (i+"_clu"+str(r)+"Handle_Ctrl_grp")
                tangentName = cmds.tangentConstraint(i, Tangentgrp, weight=1, aimVector=(0, 0, 1), upVector=(0, 1, 0), worldUpType="scene")
                cmds.delete(tangentName)

    def parentConstraintCurve(self):
        getlist = self.checkCurve()
        if not getlist:
            return
        for i in getlist:
            cvSize = cmds.getAttr(i + ".controlPoints", size=1)
            for r in range(cvSize):
                if r == 0:
                    cmds.parentConstraint(i + "_cluHandle_Ctrl", i + "_cluHandle", mo=1)
                else:
                    cmds.parentConstraint(i + "_clu%sHandle_Ctrl" %(r), i + "_clu%sHandle" %(r), mo=1)

    def CurveParent(self):
        getlist = self.checkCurve()
        if not getlist:
            return
        for i in getlist:
            cvSize = cmds.getAttr(i + ".controlPoints", size=1)
            for p in range(1, cvSize, 1):
                if p == 1:
                    cmds.parent(i + "_clu1Handle_Ctrl_grp", i + "_cluHandle_Ctrl")
                else:
                    cmds.parent(i + "_clu%sHandle_Ctrl_grp" %(p), i + "_clu%sHandle_Ctrl" %(p-1))

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

    def SColor(self):
        ColorInt = int(ui_variable['SColorInt'].value())
        #ColorInt = cmds.intSliderGrp('SColorIntSliderGrp', q=1, v=1)
        ColorIndex = [i*255 for i in cmds.colorIndex(ColorInt, q=1)]
        ui_variable['SColorview'].setStyleSheet('background-color:rgb(%s,%s,%s)' %(ColorIndex[0], ColorIndex[1], ColorIndex[2]))
        #cmds.canvas('CCanvas', e=1, rgbValue=(ColorIndex[0], ColorIndex[1], ColorIndex[2]))

    def SelCurve(self):
        ctrlName = cmds.getAttr('tempCurveName.CurName').split(',')[0:-1]
        cmds.select(cl=1)
        for i in ctrlName:
            cmds.select(i, add=1)

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
        # ColorNum = cmds.colorIndexSliderGrp(curveColorIntFieldGrp,q=1,v=1)   #查询颜色滑条
        # ColorNum = cmds.intSliderGrp('SColorIntSliderGrp', q=1, v=1)  # 查询滑条数值
        selCurve = cmds.ls(sl=1)
        cmds.undoInfo(ock=1)
        for n in range(len(selCurve)):
            CurShape = cmds.listRelatives(selCurve[n], c=1, s=1)
            cmds.setAttr(CurShape[0] + ".overrideEnabled", 1)
            cmds.setAttr(CurShape[0] + ".overrideColor", ColorNum)
        cmds.undoInfo(cck=1)

    def CurveToIK(self, curveN):  # 来自张老师
        JointNum = int(ui_variable['JointInt'].text())
        #JointNum = cmds.intFieldGrp('IKJointIntFieldGrp',q=True,v1=True)
        Atype = 3
        sel = curveN
        #if sel == 1:
        #    Atype = 3
        #else:
        #    Atype = 2
        j = int(JointNum)+1
        mz_dd = []
        mz_Loc = []
        for i in range(0, j, 1):
            NodemP = cmds.createNode('motionPath', n=curveN + '_MP' + str(i))
            cmds.setAttr(NodemP + ".fractionMode", 1)
            cmds.setAttr(NodemP + ".follow", 1)
            cmds.setAttr(NodemP + ".frontAxis", 0)
            cmds.setAttr(NodemP + ".upAxis", 1)
            cmds.setAttr(NodemP + ".worldUpType", Atype)
            B = cmds.spaceLocator(p=(0, 0, 0), n=curveN + "_Loc" + str(i))
            cmds.connectAttr(cmds.listRelatives(curveN, s=1)[0] + ".worldSpace[0]", NodemP + ".geometryPath", f=1)
            #if cmds.objExists(sel + ".V" + str(i)) == 0:
            #    cmds.addAttr(sel, ln="V" + str(i), at='double', min=0, max=1, dv=0)
            #    cmds.setAttr(sel + ".V" + str(i), e=1, keyable=True)
            #cmds.connectAttr(sel + ".V" + str(i), NodemP + ".uValue", f=1)
            cmds.setAttr(NodemP + ".uValue", 1.0*(i)/int(JointNum))
            cmds.connectAttr(NodemP + ".allCoordinates", B[0] + ".translate", f=1)
            cmds.connectAttr(NodemP + ".rotate", B[0] + ".rotate", f=1)
            if Atype == 2:
                cmds.pathAnimation(NodemP, e=1, wuo=cmds.listRelatives(curveN, s=1)[0])
            mz_dd.append(NodemP)
            mz_Loc.append(B[0])
        cmds.select(cl=1)
        Qv = cmds.xform(mz_Loc[0], q=1, ws=1, t=1)
        yt = cmds.joint(p=(Qv[0], Qv[1], Qv[2]), n=curveN + "_Jot0")
        mz_jot = []
        mz_jot.append(yt)
        for i in range(1, len(mz_Loc), 1):
            Qv = cmds.xform(mz_Loc[i], q=1, ws=1, t=1)
            yt = cmds.joint(p=(Qv[0], Qv[1], Qv[2]), n=curveN + "_Jot" + str(i))
            cmds.joint(curveN + "_Jot" + str(i-1), e=1, zso=1, oj='xyz')
            mz_jot.append(yt)
        cmds.select(cl=1)
        cmds.setAttr(mz_jot[len(mz_jot)-1] + ".jointOrientX", 0)
        cmds.setAttr(mz_jot[len(mz_jot)-1] + ".jointOrientY", 0)
        cmds.setAttr(mz_jot[len(mz_jot)-1] + ".jointOrientY", 0)
        if cmds.objExists(sel + ".AutoLe") == 0:
            cmds.addAttr(sel, ln="AutoLe", at='double', min=0, max=1, dv=0)
            cmds.setAttr(sel + ".AutoLe", e=1, keyable=1)
        if cmds.objExists(sel + ".scaleAttr") == 0:
            cmds.addAttr(sel, ln="scaleAttr", at='double', dv=1)
        #    cmds.setAttr(sel + ".scaleAttr", e=1, keyable=1)
        for i in range(1, len(mz_dd), 1):
            mz_dB = cmds.createNode('distanceBetween', n=mz_dd[i] + "_dB")
            cmds.connectAttr(mz_dd[i-1] + ".allCoordinates", mz_dd[i] + "_dB.point1", f=1)
            cmds.connectAttr(mz_dd[i] + ".allCoordinates", mz_dd[i] + "_dB.point2", f=1)
            gh = cmds.getAttr(mz_dd[i] + "_dB.distance")
            cmds.createNode('multiplyDivide', n=mz_dd[i] + "_dB_MPA")
            cmds.connectAttr(mz_dd[i] + "_dB.distance", mz_dd[i] + "_dB_MPA.input1X", f=1)
            cmds.connectAttr(sel + ".scaleAttr", mz_dd[i] + "_dB_MPA.input2X", f=1)
            cmds.setAttr(mz_dd[i] + "_dB_MPA.operation", 2)
            cmds.createNode('blendColors', n=mz_dd[i] + "_blendC")
            cmds.connectAttr(sel + ".AutoLe", mz_dd[i] + "_blendC.blender", f=1)
            cmds.connectAttr(mz_dd[i] + "_dB_MPA.outputX", mz_dd[i] + "_blendC.color1R", f=1)
            cmds.setAttr(mz_dd[i] + "_blendC.color2R", gh)
            cmds.connectAttr(mz_dd[i] + "_blendC.outputR", mz_jot[i] + ".translateX", f=1)
        cmds.ikHandle(sol='ikSplineSolver', ccv=0, sj=mz_jot[0], ee=mz_jot[len(mz_jot)-1], c=sel, n=curveN+"_SplineIkHandle")
        cmds.select(sel)
        cmds.delete(mz_Loc)
        self.doFinish(curveN)

    def doFinish(self, curveN):
        if ui_variable['CtrlParentbox'].isChecked():
            cluHandleCtrlgrp = '_cluHandle_Ctrl_grp'
        else:
            cluHandleCtrlgrp = '_clu*Handle_Ctrl_grp'
        if '_Blend' in curveN:
            editname = curveN.rsplit('_', 1)[0]
            cmds.group(editname, editname + '_clu*Handle', editname + cluHandleCtrlgrp,
                        editname + '_toFX', editname + '_OutFX', editname + '_onlyCtrl', 
                        curveN, curveN + '_Jot0', curveN + '_SplineIkHandle', n=editname + '_grp')
            cmds.hide(editname, editname + '_clu*Handle', editname + '_toFX', editname + '_OutFX', editname + '_onlyCtrl',
                        curveN + '_SplineIkHandle')
            cmds.setAttr(curveN + '.inheritsTransform', 0)
            if cmds.ls('buildPose') and cmds.ls('DeformationSystem'):
                cmds.setAttr('buildPose.udAttr', '%s/*addItem*/xform -os -t 0 0 0 -ro 0 0 0 \"%s_clu*Handle_Ctrl\";'
                                %(cmds.getAttr('buildPose.udAttr'), editname), type='string')
        else:
            cmds.group(curveN, curveN + '_clu*Handle', curveN + cluHandleCtrlgrp,
                        curveN + '_Jot0', curveN + '_SplineIkHandle', n=curveN + '_grp')
            cmds.hide(curveN + '_clu*Handle', curveN + '_SplineIkHandle')
            if cmds.ls('buildPose') and cmds.ls('DeformationSystem'):
                cmds.setAttr('buildPose.udAttr', '%s/*addItem*/xform -os -t 0 0 0 -ro 0 0 0 \"%s_clu*Handle_Ctrl\";'
                                %(cmds.getAttr('buildPose.udAttr'), curveN), type='string')

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
        try:
            cmds.deleteUI(uiPose)
        except:
            pass
        cmds.window(uiPose, t='List')
        cmds.columnLayout(rowSpacing=5)
        cmds.textScrollList('textList', numberOfRows=20, showIndexedItem=4)
        cmds.button('Add', l="Add", h=28, w=100, c=lambda*args: self.PoseEdit('add'))
        cmds.button('Delete', l="Delete", h=28, w=100, c=lambda*args: self.PoseEdit('delete'))
        cmds.showWindow(uiPose)
        ls = cmds.ls(type='transform')
        for i in splitText:
            if '_clu*Handle_Ctrl' in i:
                self.editi = (i.split('_clu*Handle_Ctrl\";')[0]).split('\"', 1)[1]
            else:
                self.editi = (i.split('\"', 1)[1]).rsplit('\"', 1)[0]
            if self.editi in ls:
                cmds.textScrollList('textList', e=1, append=i)
            else:
                cmds.textScrollList('textList', e=1, append=i + '  //NeedDelete//')

    def PoseEdit(self, mode):
        if mode == 'delete':
            poseSplit = self.buildposeText.split('/*addItem*/xform -os -t 0 0 0 -ro 0 0 0 ' + 
                cmds.textScrollList('textList', q=1, selectItem=1)[0].split(';')[0] + ';')
            cmds.setAttr('buildPose.udAttr', poseSplit[0] + poseSplit[1], type='string')
            cmds.textScrollList('textList', e=1, rii=cmds.textScrollList('textList', q=1, sii=1)[0])
        elif mode == 'add':
            if cmds.promptDialog(t='addPose', b=['OK', 'Cancel'], db='OK', cb='Cancel', ds='Cancel') == 'OK':
                inputText = cmds.promptDialog(query=True, text=True)
                lsinput = cmds.ls(inputText)
                if not lsinput:
                    cmds.error('无此物体')
                elif len(lsinput) >= 2:
                    cmds.error('有重复物体')
                cmds.setAttr('buildPose.udAttr', 
                    cmds.getAttr('buildPose.udAttr') + '/*addItem*/xform -os -t 0 0 0 -ro 0 0 0 \"' + inputText + '\";', type='string')
                cmds.textScrollList('textList', e=1, append='\"' + inputText + '\";')
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
            #MenuItem = cmds.optionMenu(pTCIK.HairSystemMenu+'|OptionMenu',q=1,ill=1)
            # if MenuItem:
            #   for i in MenuItem:
            #        cmds.deleteUI(i)
            # cmds.menuItem(parent=(pTCIK.HairSystemMenu+'|OptionMenu'),label='CreateNew')
            hairsystemitem = cmds.listRelatives(cmds.ls(type='hairSystem'), p=1)
            if hairsystemitem:
                for i in hairsystemitem:
                    ui_variable['SelectHairSystem'].addItem(i)
                    # cmds.menuItem(parent=(pTCIK.HairSystemMenu+'|OptionMenu'),label=i)
            ui_variable['SelectHairSystem'].addItem('Create New')
        if mode == 'Nucleus':
            ui_variable['SelectNucleus'].clear()
            nucleusitem = cmds.ls(type='nucleus')
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
            cmds.connectAttr('time1.outTime', qComboBox[0]+".currentTime")
            if cmds.upAxis(q=1, axis=1) == "z":
                cmds.setAttr(qComboBox[0] + ".gravityDirection", 0, 0, -1)
        if mode == 'NC' or mode == 'HC':
            qComboBox[1] = cmds.createNode('hairSystem')
            cmds.setAttr(qComboBox[1] + ".hairsPerClump", 1)
            cmds.setAttr(qComboBox[1] + ".clumpWidth", 0)
            cmds.parent(cmds.listRelatives(qComboBox[1], p=1)[0], qComboBox[0])
        if not cmds.connectionInfo(qComboBox[1]+".nextState", sfd=1):
            mel.eval('addActiveToNSystem("%s", "%s")'%(cmds.listRelatives(qComboBox[1], p=1)[0], qComboBox[0]))
            cmds.connectAttr( 'time1.outTime', qComboBox[1] + '.currentTime', f=1)
            cmds.connectAttr(qComboBox[0] + '.startFrame', qComboBox[1] + '.startFrame', f=1)
            qComboBox[1] = cmds.listRelatives(qComboBox[1], p=1)[0]
        if mel.eval('attributeExists("%s", "ctrlMode")'%qComboBox[1]):
            if not cmds.listConnections(qComboBox[1], c=1, t='reverse'):
                self.reNode = cmds.createNode("reverse")
                cmds.connectAttr(qComboBox[1] + ".ctrlMode", self.reNode+".inputX")
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
        if ui_variable['SelectNucleus'].currentText() != 'Create New' and not cmds.ls(type='nucleus'):
            self.Ready_GetNode('Nucleus')
        if ui_variable['SelectNucleus'].currentText() == 'Create New':
            qComboBox = self.ifdef('NC')
        elif ui_variable['SelectHairSystem'].currentText() == 'Create New':
            qComboBox = self.ifdef('HC')
        else:
            qComboBox = self.ifdef()
        for i in range(len(curve)):
            c = curve[i]
            hairfollicle = cmds.createNode('follicle')
            cmds.setAttr(hairfollicle + ".pointLock", 1)
            cmds.setAttr(hairfollicle + ".restPose", 1)
            cmds.setAttr(hairfollicle + ".startDirection", 1)
            cmds.setAttr(hairfollicle + ".degree", 3)
            cmds.parent(cmds.listRelatives(hairfollicle, p=1)[0], qComboBox[1])
            hairNum = cmds.listConnections(qComboBox[1]+'.outputHair')
            if not hairNum:
                cmds.connectAttr(qComboBox[1]+'.outputHair[0]', hairfollicle+'.currentPosition', f=1)
                cmds.connectAttr(hairfollicle+'.outHair', qComboBox[1]+'.inputHair[0]', f=1)
            else:
                cmds.connectAttr(qComboBox[1]+'.outputHair['+str(len(hairNum))+']', hairfollicle+'.currentPosition', f=1)
                cmds.connectAttr(hairfollicle+'.outHair', qComboBox[1]+'.inputHair['+str(len(hairNum))+']', f=1)
            cmds.rename(cmds.rebuildCurve(c, ch=1, rpo=0, rt=0, end=1, kr=0, kcp=0, kep=1, kt=0, 
                        s=cmds.getAttr(c + ".controlPoints", size=1) + 5, d=3, tol=0.01)[0], c + '_toFX')
            cmds.duplicate(c, rr=1, n=c + '_onlyCtrl')
            cmds.duplicate(c + '_toFX', rr=1, n=c + '_Blend')
            cmds.connectAttr(cmds.listRelatives(c + '_toFX', s=1)[0] + '.worldSpace[0]', 
                            cmds.listRelatives(c + '_onlyCtrl',s=1)[0] + '.create', f=1)
            cmds.parent(c + '_toFX', cmds.listRelatives(hairfollicle, p=1))
            cmds.connectAttr(cmds.listRelatives(c + '_toFX', s=1, type='nurbsCurve')[0] + '.local', hairfollicle + '.startPosition', f=1)
            cmds.connectAttr(c + '_toFX.worldMatrix[0]', hairfollicle+'.startPositionMatrix', f=1)
            cmds.connectAttr(hairfollicle + '.outCurve', cmds.duplicate(c, rr=1, n=c + '_OutFX')[0] + 'Shape.create', f=1)
            cmds.blendShape(c + '_OutFX', c + '_onlyCtrl', c + '_Blend', n=c + '_curveBS')
            cmds.connectAttr(qComboBox[1] + '.ctrlMode', c + '_curveBS.' + c + '_OutFX')
            cmds.connectAttr(self.reNode + ".outputX", c + '_curveBS.' + c + '_onlyCtrl')
        ApplePieA_Dynamic().Ready_GetNode('HairSystem')
        ApplePieA_Dynamic().Ready_GetNode('Nucleus')
        cmds.undoInfo(cck=1)

pTCIKui = Showwindow()
pTCIKui.show()
