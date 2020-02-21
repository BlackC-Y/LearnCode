from PySide2 import QtCore, QtGui, QtWidgets
import maya.cmds as cmds
import maya.mel as mm
import maya.OpenMayaUI as Omui
import shiboken2

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
    cmds.button('Next1Button', l="选模型的线", h=28,c=lambda*args: ApplePieA_pTCIK().SelectPolyCurve())   # 命令保护前缀lambda*args:
    cmds.flowLayout(columnSpacing=45)
    cmds.text(l="")
    cmds.text(l="调整曲线", h=28)
    cmds.button('reverseCurveButton', l="反转曲线", h=28, w=80,c=lambda*args: ApplePieA_pTCIK().reverseCurve())
    cmds.setParent('..')  # 返回上一界面布局
    cmds.button('createCluAndCtrlButton', l="创建簇和控制器", h=28,c=lambda*args: ApplePieA_pTCIK().createCluAndCtrl())
    #cmds.button('CurveToolsButton', l="曲线工具(可选)", h=28,c=lambda*args: ApplePieA_pTCIK().CurveTools())
    cmds.button('parentConButton', l="约束控制", h=28,c=lambda*args: ApplePieA_pTCIK().parentConstraintCurve())
    cmds.flowLayout(columnSpacing=25)
    cmds.button('ParentButton', l="控制器层级化", h=28,w=110,c=lambda*args: ApplePieA_pTCIK().CurveParent(''))
    cmds.button('ReParentButton', l="解开层级", h=28,w=110,c=lambda*args: ApplePieA_pTCIK().CurveParent('reverse'))
    cmds.setParent('..')  # 返回上一界面布局
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
def password():
    import time
    if cmds.promptDialog(title='password', button=['OK', 'Cancel'], defaultButton='OK', cancelButton='Cancel', dismissString='Cancel') == 'OK':
        if not cmds.promptDialog(query=True, text=True) == str(time.localtime()[1])+str(time.localtime()[2])+str(time.localtime()[3])+str(time.localtime()[4]):
            cmds.error('')
    else:
        cmds.error('')
password()
'''

ui_variable = {}
class Ui_ApplePieA(object):

    def setupUi(self, ApplePieA):
        try:
            win.close()
            #QtGui.QWidgetAction.deleteWidget("ApplePieA")
        except:
            pass
        ApplePieA.setObjectName("ApplePieA")
        #ApplePieA.resize(260, 500)
        ApplePieA.setFixedSize(260,500)
        self.tabWidget = QtWidgets.QTabWidget(ApplePieA)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 260, 480))
        self.tabWidget.setObjectName("tabWidget")
        self.child1 = QtWidgets.QWidget()
        self.child1.setObjectName("child1")
        self.verticalLayoutAWidget = QtWidgets.QWidget(self.child1)
        self.verticalLayoutAWidget.setGeometry(QtCore.QRect(5, 5, 245, 350))
        self.verticalLayoutAWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayoutA = QtWidgets.QVBoxLayout(self.verticalLayoutAWidget)
        self.verticalLayoutA.setSpacing(3)
        self.verticalLayoutA.setContentsMargins(0, 0, 0, 0)
        #self.verticalLayoutA.minimumSize(28)
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
        #self.CurveNameWar.setAlignment(QtCore.Qt.AlignCenter)
        #self.CurveNameWar.setStyleSheet("color:yellow")
        #self.CurveNameWar.setMaximumSize(QtCore.QSize(245, 20))
        #self.CurveNameWar.setObjectName("CurveNameWar")
        #self.verticalLayoutA.addWidget(self.CurveNameWar)
        self.horizontalLayoutC = QtWidgets.QHBoxLayout()
        self.horizontalLayoutC.setObjectName("horizontalLayout")
        self.SelectPolyCurve = QtWidgets.QPushButton(self.verticalLayoutAWidget)
        self.SelectPolyCurve.setObjectName("SelectPolyCurve")
        self.SelectPolyCurve.clicked.connect(lambda *args: ApplePieA_pTCIK().SelectPolyCurve())
        self.horizontalLayoutC.addWidget(self.SelectPolyCurve)
        self.reverseCurve = QtWidgets.QPushButton(self.verticalLayoutAWidget)
        self.reverseCurve.setObjectName("reverseCurve")
        self.reverseCurve.clicked.connect(lambda *args: ApplePieA_pTCIK().reverseCurve())
        self.horizontalLayoutC.addWidget(self.reverseCurve)
        self.verticalLayoutA.addLayout(self.horizontalLayoutC)
        self.lineA = QtWidgets.QFrame(self.verticalLayoutAWidget)
        self.lineA.setFrameShape(QtWidgets.QFrame.HLine)
        self.lineA.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.lineA.setObjectName("line")
        self.verticalLayoutA.addWidget(self.lineA)
        self.CreateCtrl = QtWidgets.QPushButton(self.verticalLayoutAWidget)
        self.CreateCtrl.setObjectName("CreateCtrl")
        self.CreateCtrl.clicked.connect(lambda *args: ApplePieA_pTCIK().createCtrl())
        self.verticalLayoutA.addWidget(self.CreateCtrl)
        self.horizontalLayout0 = QtWidgets.QHBoxLayout()
        self.horizontalLayout0.setObjectName("horizontalLayout")
        ui_variable['selectboxA'] = self.selectboxA = QtWidgets.QCheckBox(self.verticalLayoutAWidget)
        self.selectboxA.setMaximumSize(QtCore.QSize(100, 20))
        self.selectboxA.setObjectName("selectboxA")
        self.selectboxA.setChecked(True)
        self.horizontalLayout0.addWidget(self.selectboxA)
        ui_variable['selectboxB'] = self.selectboxB = QtWidgets.QCheckBox(self.verticalLayoutAWidget)
        self.selectboxB.setMaximumSize(QtCore.QSize(100, 20))
        self.selectboxB.setObjectName("selectboxB")
        self.horizontalLayout0.addWidget(self.selectboxB)
        self.verticalLayoutA.addLayout(self.horizontalLayout0)
        self.selectboxGrp = QtWidgets.QButtonGroup(self.verticalLayoutAWidget)
        self.selectboxGrp.addButton(self.selectboxA,11)
        self.selectboxGrp.addButton(self.selectboxB,12)
        #self.parentCon = QtWidgets.QPushButton(self.verticalLayoutAWidget)
        #self.parentCon.setObjectName("parentCon")
        #self.parentCon.clicked.connect(lambda *args: ApplePieA_pTCIK().parentConstraintCurve())
        #self.verticalLayoutA.addWidget(self.parentCon)
        #self.CtrlParent = QtWidgets.QPushButton(self.verticalLayoutAWidget)
        #self.CtrlParent.setObjectName("CtrlParent")
        #self.CtrlParent.clicked.connect(lambda *args: ApplePieA_pTCIK().CurveParent(''))
        #self.verticalLayoutA.addWidget(self.CtrlParent)
        #self.CtrlReParent = QtWidgets.QPushButton(self.verticalLayoutAWidget)
        #self.CtrlReParent.setObjectName("CtrlReParent")
        #self.CtrlReParent.clicked.connect(lambda *args: ApplePieA_pTCIK().CurveParent('reverse'))
        #self.verticalLayoutA.addWidget(self.CtrlReParent)
        self.horizontalLayoutD = QtWidgets.QHBoxLayout()
        self.horizontalLayoutD.setObjectName("horizontalLayout")
        self.JointIntText = QtWidgets.QLabel(self.verticalLayoutAWidget)
        self.JointIntText.setMaximumSize(QtCore.QSize(50, 20))
        self.JointIntText.setObjectName("JointIntText")
        self.horizontalLayoutD.addWidget(self.JointIntText)
        ui_variable['JointInt'] = self.JointInt = QtWidgets.QLineEdit(self.verticalLayoutAWidget)
        self.JointInt.setMaximumSize(QtCore.QSize(100, 20))
        self.JointInt.setObjectName("JointInt")
        self.horizontalLayoutD.addWidget(self.JointInt)
        self.verticalLayoutA.addLayout(self.horizontalLayoutD)
        self.BuildIK = QtWidgets.QPushButton(self.verticalLayoutAWidget)
        self.BuildIK.setObjectName("BuildIK")
        self.BuildIK.clicked.connect(lambda *args: ApplePieA_pTCIK().CurveToIK())
        self.BuildIK.installEventFilter(self)
        self.verticalLayoutA.addWidget(self.BuildIK)
        self.PoseEdit = QtWidgets.QPushButton(self.child1)
        self.PoseEdit.setGeometry(QtCore.QRect(180, 430, 80, 28))
        self.PoseEdit.setObjectName("PoseEdit")
        self.PoseEdit.clicked.connect(lambda *args: poseEdit().PoseCheck())
        self.tabWidget.addTab(self.child1, "")

        self.child2 = QtWidgets.QWidget()
        self.child2.setObjectName("child2")
        self.verticalLayoutBWidget = QtWidgets.QWidget(self.child2)
        self.verticalLayoutBWidget.setGeometry(QtCore.QRect(5, 5, 245, 200))
        self.verticalLayoutBWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayoutB = QtWidgets.QVBoxLayout(self.verticalLayoutBWidget)
        self.verticalLayoutB.setSpacing(5)
        self.verticalLayoutB.setContentsMargins(0, 0, 0, 0)
        self.verticalLayoutB.setObjectName("verticalLayout")
        #self.horizontalLayoutE = QtWidgets.QHBoxLayout()
        #self.horizontalLayoutE.setObjectName("horizontalLayout")
        #self.horizontalLayoutE.setSpacing(3)
        self.CShape = QtWidgets.QPushButton(self.verticalLayoutBWidget)
        self.CShape.setObjectName("CShape")
        self.CShape.clicked.connect(lambda *args: ApplePieA_pTCIK().cShape())
        self.verticalLayoutB.addWidget(self.CShape)
        #self.Tangent = QtWidgets.QPushButton(self.verticalLayoutBWidget)
        #self.Tangent.setObjectName("Tangent")
        #self.Tangent.clicked.connect(lambda *args: ApplePieA_pTCIK().Tangent())
        #self.horizontalLayoutE.addWidget(self.Tangent)
        #self.verticalLayoutB.addLayout(self.horizontalLayoutE)
        #self.SelCurveCtel = QtWidgets.QPushButton(self.verticalLayoutBWidget)
        #self.SelCurveCtel.setObjectName("SelCurveCtel")
        #self.SelCurveCtel.clicked.connect(lambda *args: ApplePieA_pTCIK().SelCurve())
        #self.verticalLayoutB.addWidget(self.SelCurveCtel)
        self.horizontalLayoutF = QtWidgets.QHBoxLayout()
        self.horizontalLayoutF.setObjectName("horizontalLayout")
        self.horizontalLayoutF.setSpacing(3)
        self.RotX = QtWidgets.QPushButton(self.verticalLayoutBWidget)
        self.RotX.setObjectName("RotX")
        self.RotX.clicked.connect(lambda *args: ApplePieA_pTCIK().RSCurve('RX'))
        self.horizontalLayoutF.addWidget(self.RotX)
        self.RotY = QtWidgets.QPushButton(self.verticalLayoutBWidget)
        self.RotY.setObjectName("RotY")
        self.RotY.clicked.connect(lambda *args: ApplePieA_pTCIK().RSCurve('RY'))
        self.horizontalLayoutF.addWidget(self.RotY)
        self.RotZ = QtWidgets.QPushButton(self.verticalLayoutBWidget)
        self.RotZ.setObjectName("RotZ")
        self.RotZ.clicked.connect(lambda *args: ApplePieA_pTCIK().RSCurve('RZ'))
        self.horizontalLayoutF.addWidget(self.RotZ)
        self.verticalLayoutB.addLayout(self.horizontalLayoutF)
        self.horizontalLayoutG = QtWidgets.QHBoxLayout()
        self.horizontalLayoutG.setObjectName("horizontalLayout")
        self.horizontalLayoutG.setSpacing(3)
        self.ScaleAdd = QtWidgets.QPushButton(self.verticalLayoutBWidget)
        self.ScaleAdd.setObjectName("ScaleAdd")
        self.ScaleAdd.clicked.connect(lambda *args: ApplePieA_pTCIK().RSCurve('SA'))
        self.horizontalLayoutG.addWidget(self.ScaleAdd)
        self.ScaleSub = QtWidgets.QPushButton(self.verticalLayoutBWidget)
        self.ScaleSub.setObjectName("ScaleSub")
        self.ScaleSub.clicked.connect(lambda *args: ApplePieA_pTCIK().RSCurve('SS'))
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
        self.SColorInt.valueChanged.connect(lambda*args: ApplePieA_pTCIK().SColor())
        self.SColorInt.setObjectName("SColorInt")
        self.horizontalLayoutH.addWidget(self.SColorInt)
        self.verticalLayoutB.addLayout(self.horizontalLayoutH)
        self.ChangeColor = QtWidgets.QPushButton(self.verticalLayoutBWidget)
        self.ChangeColor.setObjectName("ChangeColor")
        self.ChangeColor.clicked.connect(lambda *args: ApplePieA_pTCIK().ChangeCurveColor())
        self.verticalLayoutB.addWidget(self.ChangeColor)
        self.tabWidget.addTab(self.child2, "")

        self.child3 = QtWidgets.QWidget()
        self.child3.setObjectName("child3")
        self.getCurveText = QtWidgets.QLabel(self.child3)
        self.getCurveText.setGeometry(QtCore.QRect(15, 10, 55, 20))
        self.getCurveText.setObjectName("getCurveText")
        ui_variable['getCurveGrp'] = self.getCurveGrp = QtWidgets.QLineEdit(self.child3)
        self.getCurveGrp.setGeometry(QtCore.QRect(77, 10, 90, 20))
        self.getCurveGrp.setReadOnly(True)
        self.getCurveGrp.setObjectName("getCurveGrp")
        self.getCurve = QtWidgets.QPushButton(self.child3)
        self.getCurve.setGeometry(QtCore.QRect(175, 10, 60, 20))
        self.getCurve.setObjectName("getCurve")
        self.getCurve.clicked.connect(lambda *args: ApplePieA_Dynamic().Ready_selectCurve())
        self.HairSystemText = QtWidgets.QLabel(self.child3)
        self.HairSystemText.setGeometry(QtCore.QRect(15, 60, 55, 20))
        self.HairSystemText.setObjectName("HairSystemText")
        ui_variable['SelectHairSystem'] = self.SelectHairSystem = QtWidgets.QComboBox(self.child3)
        self.SelectHairSystem.setGeometry(QtCore.QRect(77, 60, 110, 20))
        self.SelectHairSystem.setObjectName("SelectHairSystem")
        self.SelectHairSystem.installEventFilter(self)
        self.SelectHairSystem.currentTextChanged.connect(lambda *args: ApplePieA_Dynamic().Acondition('HairSystem'))
        self.FollicleText = QtWidgets.QLabel(self.child3)
        self.FollicleText.setGeometry(QtCore.QRect(15, 85, 55, 20))
        self.FollicleText.setObjectName("FollicleText")
        self.FollicleText.setVisible(False)
        ui_variable['SelectFollicle'] = self.SelectFollicle = QtWidgets.QComboBox(self.child3)
        self.SelectFollicle.setGeometry(QtCore.QRect(77, 85, 110, 20))
        self.SelectFollicle.setObjectName("SelectFollicle")
        self.SelectFollicle.installEventFilter(self)
        self.SelectFollicle.setVisible(False)
        self.NucleusText = QtWidgets.QLabel(self.child3)
        self.NucleusText.setGeometry(QtCore.QRect(15, 110, 55, 20))
        self.NucleusText.setObjectName("NucleusText")
        self.NucleusText.setVisible(False)
        ui_variable['SelectNucleus'] = self.SelectNucleus = QtWidgets.QComboBox(self.child3)
        self.SelectNucleus.setGeometry(QtCore.QRect(77, 110, 110, 20))
        self.SelectNucleus.setObjectName("SelectNucleus")
        self.SelectNucleus.installEventFilter(self)
        self.SelectNucleus.setVisible(False)
        self.SelectNucleus.currentTextChanged.connect(lambda *args: ApplePieA_Dynamic().Acondition('Nucleus'))
        self.CreateFX = QtWidgets.QPushButton(self.child3)
        self.CreateFX.setGeometry(QtCore.QRect(5, 150, 245, 28))
        self.CreateFX.setObjectName("CreateFX")
        self.CreateFX.clicked.connect(lambda *args: ApplePieA_Dynamic().FXCurve())
        self.tabWidget.addTab(self.child3, "")

        ui_variable['Statusbar'] = self.Statusbar = QtWidgets.QStatusBar(ApplePieA)
        self.Statusbar.setStyleSheet("color:yellow")
        self.Statusbar.setGeometry(QtCore.QRect(0, 475, 260, 28))
        self.Statusbar.setObjectName("Statusbar")

        self.retranslateUi(ApplePieA)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(ApplePieA)
        ApplePieA_Dynamic().Ready_GetNode('HairSystem')
        ApplePieA_Dynamic().Ready_GetNode('Follicle')
        ApplePieA_Dynamic().Ready_GetNode('Nucleus')

    def retranslateUi(self, ApplePieA):
        ApplePieA.setWindowTitle(u"ApplePieA")
        self.RebuildIntText.setText(u"重建段数")
        self.RebuildInt.setPlaceholderText(u"重建段数")
        self.CurveNameText.setText(u"曲线名")
        self.CurveName.setPlaceholderText(u"曲线名")
        self.SelectPolyCurve.setText(u"选模型的线")
        self.reverseCurve.setText(u"反转曲线")
        self.CreateCtrl.setText(u"创建控制")
        self.selectboxA.setText(u"层级化控制器")
        self.selectboxB.setText(u"解层级化")
        #self.parentCon.setText(u"约束控制")
        #self.CtrlParent.setText(u"控制器层级化")
        #self.CtrlReParent.setText(u"解层级化")
        self.JointIntText.setText(u"骨骼段数")
        self.BuildIK.setText(u"建立IK")
        self.PoseEdit.setText(u"PoseEdit")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.child1), u"本体")

        self.CShape.setText(u"换个形状")
        #self.Tangent.setText(u"切线约束")
        #self.SelCurveCtel.setText(u"选择当前曲线的控制器")
        self.RotX.setText(u"RotX")
        self.RotY.setText(u"RotY")
        self.RotZ.setText(u"RotZ")
        self.ScaleAdd.setText(u"放大曲线")
        self.ScaleSub.setText(u"缩小曲线")
        self.ChangeColor.setText(u"改变颜色")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.child2), u"曲线DLC")

        self.getCurveText.setText(u"曲线名")
        self.getCurve.setText(u"获取曲线")
        self.HairSystemText.setText(u"HairSystem")
        self.FollicleText.setText(u"Follicle")
        self.NucleusText.setText(u"Nucleus")
        self.CreateFX.setText(u"创建动力学曲线")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.child3), u"动力学曲线")

    def eventFilter(self, object, event):
        if object == self.SelectHairSystem:
            if event.type() == QtCore.QEvent.MouseButtonPress:
                ApplePieA_Dynamic().Ready_GetNode('HairSystem')
            if event.type() == QtCore.QEvent.MouseButtonDblClick:
                if event.button() == QtCore.Qt.RightButton:
                    self.FollicleText.setVisible(True)
                    self.SelectFollicle.setVisible(True)
                    self.NucleusText.setVisible(True)
                    self.SelectNucleus.setVisible(True)
            return super(Ui_ApplePieA, self).eventFilter(object, event)
        elif object == self.SelectFollicle:
            if event.type() == QtCore.QEvent.MouseButtonPress:
                ApplePieA_Dynamic().Ready_GetNode('Follicle')
            return super(Ui_ApplePieA, self).eventFilter(object, event)
        elif object == self.SelectNucleus:
            if event.type() == QtCore.QEvent.MouseButtonPress:
                ApplePieA_Dynamic().Ready_GetNode('Nucleus')
            return super(Ui_ApplePieA, self).eventFilter(object, event)
        elif object == self.BuildIK:
            if event.type() == QtCore.QEvent.MouseButtonDblClick:
                if event.button() == QtCore.Qt.RightButton:
                    oneBuildIK().getNum()
            return super(Ui_ApplePieA, self).eventFilter(object, event)
        
class Showwindow(Ui_ApplePieA, QtWidgets.QWidget):
    
    def __init__(self):
        super(Showwindow, self).__init__()
        self.setupUi(self)
        self.setParent(shiboken2.wrapInstance(long(Omui.MQtUtil.mainWindow()), QtWidgets.QMainWindow))
        self.setWindowFlags(QtCore.Qt.Window)
        #self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)   #置顶
        self.setWindowTitle('v1.99')
        self.show()
        #ui_variable['Statusbar'].showMessage(u"插件所有操作都不能撤回.出错删掉重做")

class ApplePieA_pTCIK(object):

    curveShape = 0

    def __init__(self):
        self.Curvename = ui_variable['CurveName'].text()
        self.curSample = [
                [((-.5 ,.5 ,.5 ),(-.5 ,.5 ,-.5 ),(.5 ,.5 ,-.5 ),(.5 ,.5 ,.5 ),(-.5 ,.5 ,.5 ),(-.5 ,-.5 ,.5 ),(-.5 ,-.5 ,-.5 ),(-.5 ,.5 ,-.5 ),(-.5 ,.5 ,.5 ),(-.5 ,-.5 ,.5 ),(.5 ,-.5 ,.5 ),(.5 ,.5 ,.5 ),(.5 ,.5 ,-.5 ),(.5 ,-.5 ,-.5 ),(.5 ,-.5 ,.5 ),(.5 ,-.5 ,-.5 ),(-.5 ,-.5 ,-.5)),(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16)],
                [((0,1,0),(0,0.92388,0.382683),(0,0.707107,0.707107),(0,0.382683,0.92388),(0,0,1),(0,-0.382683,0.92388),(0,-0.707107,0.707107),(0,-0.92388,0.382683),(0,-1,0),(0,-0.92388,-0.382683),(0,-0.707107,-0.707107),(0,-0.382683,-0.92388),(0,0,-1),(0,0.382683,-0.92388),(0,0.707107,-0.707107),(0,0.92388,-0.382683),(0,1,0),(0.382683,0.92388,0),(0.707107,0.707107,0),(0.92388,0.382683,0),(1,0,0),(0.92388,-0.382683,0),(0.707107,-0.707107,0),(0.382683,-0.92388,0),(0,-1,0),(-0.382683,-0.92388,0),(-0.707107,-0.707107,0),(-0.92388,-0.382683,0),(-1,0,0),(-0.92388,0.382683,0),(-0.707107,0.707107,0),(-0.382683,0.92388,0),(0,1,0),(0,0.92388,-0.382683),(0,0.707107,-0.707107),(0,0.382683,-0.92388),(0,0,-1),(-0.382683,0,-0.92388),(-0.707107,0,-0.707107),(-0.92388,0,-0.382683),(-1,0,0),(-0.92388,0,0.382683),(-0.707107,0,0.707107),(-0.382683,0,0.92388),(0,0,1),(0.382683,0,0.92388),(0.707107,0,0.707107),(0.92388,0,0.382683),(1,0,0),(0.92388,0,-0.382683),(0.707107,0,-0.707107),(0.382683,0,-0.92388),(0,0,-1)),(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52)],
                [((-1.6,-6.4,0),(-1.6,-1.6,0),(-6.4,-1.6,0),(-6.4,1.6,0),(-1.6,1.6,0),(-1.6,6.4,0),(1.6,6.4,0),(1.6,1.6,0),(6.4,1.6,0),(6.4,-1.6,0),(1.6,-1.6,0),(1.6,-6.4,0),(-1.6,-6.4,0)),(0,4.8,9.6,12.8,17.6,22.4,25.6,30.4,35.2,38.4,43.2,48,51.2)],
                        ]
        try:
            cmds.delete('__temp_Cur')
        except:
            pass

    def SelectPolyCurve(self):
        ReBNum = ui_variable['RebuildInt'].text()
        if not ReBNum:
            ui_variable['Statusbar'].showMessage(u"//没填重建段数")
            cmds.error()
        if not self.Curvename:
            ui_variable['Statusbar'].showMessage(u"//没填曲线名")
            cmds.error()

        #ReBNum = cmds.intFieldGrp('RebuildIntFieldGrp', q=True, v1=True)
        polyEdgeN = cmds.ls(sl=True)
        Namelist = cmds.ls()
        # bothName = cmp(Curvename,Namelist);  #对比名称
        if self.Curvename in Namelist:
            ui_variable['Statusbar'].showMessage(u"//名称冲突")
            cmds.error()
        '''     #列表对比
		for A in L1:
			if A in L2:
				******
		'''
        cmds.undoInfo(ock=1)
        if cmds.confirmDialog( title='Confirm', message='尝试居中对齐?', button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' ) == 'Yes':
            cmds.polyToCurve(ch=0,form=2,degree=3,n='__temp_cur')
            cmds.select (polyEdgeN,r=1)
            mm.eval("PolySelectConvert 3;")
            selv = cmds.ls (sl=1,fl=1)
            for v in range(len(selv)):
                cmds.select (selv[v],r=1)
                mm.eval("PolySelectConvert 2;")
                cmds.select (polyEdgeN,d=1)
                mm.eval("performSelContiguousEdges 0;")
                cmds.cluster(n='__temp_clu')
            cl = cmds.ls('__temp_clu*Handle')
            node_p = {}
            for c in range(len(cl)):
                temp_node = cmds.createNode ('nearestPointOnCurve',n='__temp_node')
                cmds.connectAttr ('__temp_cur.worldSpace[0]',temp_node+'.inputCurve')
                if c == 0:
                    cmds.connectAttr ('__temp_cluHandleShape.origin',temp_node+'.inPosition')
                else:
                    cmds.connectAttr ('__temp_clu'+str(c)+'HandleShape.origin',temp_node+'.inPosition')
                node_p[c] = cmds.getAttr (temp_node+'.parameter')
            node_p_list = sorted(node_p.items(),key=lambda item:item[1])
            tcws = [[0 for y in range(3)] for x in range(len(selv))]
            for v in range(len(selv)):
                if node_p_list[v][0] == 0:
                    c = ''
                else:
                    c = node_p_list[v][0]
                tcws[v][0] = cmds.getAttr ('__temp_clu'+str(c)+'HandleShape.originX')
                tcws[v][1] = cmds.getAttr ('__temp_clu'+str(c)+'HandleShape.originY')
                tcws[v][2] = cmds.getAttr ('__temp_clu'+str(c)+'HandleShape.originZ')
            cmds.curve (p=tcws,n=self.Curvename)
            reshape = cmds.listRelatives(self.Curvename,s=1)
            cmds.rename(reshape,self.Curvename+'Shape')
            cmds.delete ('__temp_*')
        else:
            cmds.select(polyEdgeN, r=True)
            pTCname = cmds.polyToCurve(ch=0,form=2, degree=3)
            cmds.rename(pTCname[0], self.Curvename)
        cmds.rebuildCurve(self.Curvename, ch=0, rpo=1, rt=0, end=1,kr=0, kcp=0, kep=1, kt=0, s=int(ReBNum), d=3, tol=0.01)
        cvSize = cmds.getAttr((self.Curvename+".controlPoints"), size=1)  # 获取曲线控制点数量
        cmds.delete(self.Curvename+'.cv[1]',self.Curvename+'.cv['+str(cvSize-2)+']')
        cmds.setAttr((self.Curvename+".dispCV"), 1)
        cmds.undoInfo(cck=1)
        
    def checkCurve(self):
        curlist = cmds.ls(sl=1)
        for i in curlist:
            if not cmds.listRelatives(i,s=1,type='nurbsCurve'):
                ui_variable['Statusbar'].showMessage(u'//有非曲线物体')
                cmds.error('有非曲线物体')
        return curlist

    def reverseCurve(self):
        cmds.undoInfo(ock=1)
        getlist = self.checkCurve()
        for i in getlist:
            cmds.reverseCurve(i, ch=0, rpo=1)
        cmds.undoInfo(cck=1)
        
    def createCtrl(self):
        cmds.undoInfo(ock=1)
        getlist = self.checkCurve()
        for i in getlist:
            cmds.setAttr(i+".dispCV", 0)
            cmds.select(i, r=1)
            cmds.DeleteHistory()
            curve = cmds.listRelatives(s=1, type="nurbsCurve")[0]
            numCVs = cmds.getAttr((curve+".controlPoints"), size=1)
            for nu in range(numCVs):
                createClu = cmds.cluster((curve + ".cv[" + str(nu) + "]"), n=(i + "_clu"), rel=1)
                print (createClu)
                createCur = cmds.circle(ch=0, n=(createClu[1] + "_Ctrl"))
                print (createCur)
                SDKgroup = cmds.group(n=(createCur[0]+"_SDK"))
                ctrlgroup = cmds.group(n=(createCur[0]+"_grp"))
                cmds.connectAttr((createClu[1]+"Shape"+".originX"), (ctrlgroup+".tx"), f=1)
                cmds.connectAttr((createClu[1]+"Shape"+".originY"), (ctrlgroup+".ty"), f=1)
                cmds.connectAttr((createClu[1]+"Shape"+".originZ"), (ctrlgroup+".tz"), f=1)
                cmds.disconnectAttr((createClu[1]+"Shape"+".originX"), (ctrlgroup+".tx"))
                cmds.disconnectAttr((createClu[1]+"Shape"+".originY"), (ctrlgroup+".ty"))
                cmds.disconnectAttr((createClu[1]+"Shape"+".originZ"), (ctrlgroup+".tz"))
                cmds.select(cl=1)
        cmds.undoInfo(cck=1)
    
    def Tangent(self):
        getlist = self.checkCurve()
        for i in getlist:
            cvSize = cmds.getAttr((i+".controlPoints"), size=1)  # 获取曲线控制点数量
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
        for i in getlist:
            cvSize = cmds.getAttr((i+".controlPoints"), size=1)
            for r in range(cvSize):
                if r == 0:
                    cmds.parentConstraint(i+"_cluHandle_Ctrl",i+"_cluHandle",mo=1)
                else:
                    cmds.parentConstraint(i+"_clu"+str(r)+"Handle_Ctrl",i+"_clu"+str(r)+"Handle",mo=1)

    def CurveParent(self,mode):
        clun = cmds.ls(self.Curvename+'_clu*Handle')
        if mode == 'reverse':
            wot = cmds.listRelatives(self.Curvename+"_cluHandle_Ctrl_grp",p=1)
            if wot == None:
                cmds.parent (self.Curvename+"_clu*Handle_Ctrl_grp",w=1)
            else:
                cmds.parent (self.Curvename+"_clu*Handle_Ctrl_grp",wot)
        else:
            for p in range(1,len(clun),1):
                if p == 1:
                    cmds.parent((self.Curvename+"_clu1Handle_Ctrl_grp"),(self.Curvename+"_cluHandle_Ctrl"))
                else:
                    cmds.parent((self.Curvename+"_clu"+str(p)+"Handle_Ctrl_grp"),(self.Curvename+"_clu"+str(p-1)+"Handle_Ctrl"))

    def cShape(self):
        if ApplePieA_pTCIK.curveShape == 4:
            ApplePieA_pTCIK.curveShape = 0
        getlist = self.checkCurve()
        cmds.undoInfo(ock=1)
        if ApplePieA_pTCIK.curveShape == 3:
            cmds.circle(n='__temp_Shape')
        else:
            cmds.curve(d=1, p=self.curSample[ApplePieA_pTCIK.curveShape][0], k=self.curSample[ApplePieA_pTCIK.curveShape][1], n='__temp_Shape')
        for i in getlist:
            cmds.connectAttr('__temp_Shape.worldSpace[0]', cmds.listRelatives(i,s=1,type="nurbsCurve")[0] + '.create', f=1)
        ApplePieA_pTCIK.curveShape += 1
        cmds.setAttr('__temp_Shape.visibility', 0)
        cmds.select(getlist,r=1)
        cmds.undoInfo(cck=1)
        
    def SColor(self):
        ColorInt = int(ui_variable['SColorInt'].value())
        #ColorInt = cmds.intSliderGrp('SColorIntSliderGrp', q=1, v=1)
        ColorIndex = [i*255 for i in cmds.colorIndex(ColorInt, q=1)]
        ui_variable['SColorview'].setStyleSheet('background-color:rgb(%s,%s,%s)'%(ColorIndex[0],ColorIndex[1],ColorIndex[2]))
        #cmds.canvas('CCanvas', e=1, rgbValue=(ColorIndex[0], ColorIndex[1], ColorIndex[2]))
    '''
    def SelCurve(self):
        if ui_variable['selectboxA'].isChecked():
            Sel = cmds.ls(sl=1)
            if Sel:
                self.Curvename = Sel[0]
            cmds.select(self.Curvename+"_clu*Handle_Ctrl")
        else:
            pass
    '''
    def RSCurve(self, mode):
        curves = cmds.listRelatives(s=1, type="nurbsCurve")  # 获取选择曲线
        if not curves:
            ui_variable['Statusbar'].showMessage(u"//未选择曲线")
            cmds.error()
        selCurve = cmds.ls(sl=1)
        cmds.select(cl=True)
        for c in selCurve:
            cmds.select(c + ".controlPoints[*]", add=1)
        if mode == 'RX':
            cmds.rotate(90, 0, 0, r=1, ocp=1, os=1, xc='edge', xn=1, fo=1)
        if mode == 'RY':
            cmds.rotate(0, 90, 0, r=1, ocp=1, os=1, xc='edge', xn=1, fo=1)
        if mode == 'RZ':
            cmds.rotate(0, 0, 90, r=1, ocp=1, os=1, xc='edge', xn=1, fo=1)
        if mode == 'SA':
            cmds.scale(1.2, 1.2, 1.2, r=1)
        if mode == 'SS':
            cmds.scale(.8, .8, .8, r=1)

        cmds.select(cl=True)
        for C in selCurve:
            cmds.select(C, add=1)

    def ChangeCurveColor(self):
        ColorNum = int(ui_variable['SColorInt'].value())
        #ColorNum = cmds.colorIndexSliderGrp(curveColorIntFieldGrp,q=1,v=1)   #获取颜色滑条
        #ColorNum = cmds.intSliderGrp('SColorIntSliderGrp', q=1, v=1)  # 获取单行滑条
        selCurve = cmds.ls(sl=1)
        for n in range(0, len(selCurve), 1):
            CurShape = cmds.listRelatives(selCurve[n], children=1, s=1)  # 颜色需要给予Shape
            cmds.setAttr((CurShape[0]+".overrideEnabled"), 1)
            cmds.setAttr((CurShape[0]+".overrideColor"), ColorNum)  # 颜色滑条时需要($ColorNum-1)

    def CurveToIK(self):   #张老师哒 (╯‵□′)╯︵┻━┻
        JointNum = int(ui_variable['JointInt'].text())
        #JointNum = cmds.intFieldGrp('IKJointIntFieldGrp',q=True,v1=True)
        Atype = 0
        sel = [0 for y in range(2)]
        sel[0] = self.Curvename
        sel[1] = cmds.listRelatives(self.Curvename,s=1)[0]
        if sel == 1:
            Atype = 3   #选择数为1输出3
        else:
            Atype = 2   #否则输出2
        j = int(JointNum)+1
        qw = sel[0]   #sel[0]应该为曲线节点
        cmds.duplicate(sel[0],rr=1,n=(self.Curvename+"_dupCurve"))
        startTime = cmds.timerX()   #计时
        mz_dd = []
        mz_Loc = []
        for i in range(0,j,1):
            A = cmds.createNode('motionPath',n=self.Curvename+"_MP"+str(i))
            cmds.setAttr ((A+".fractionMode"),1)
            cmds.setAttr ((A+".follow"),1)
            cmds.setAttr ((A+".frontAxis"),0)
            cmds.setAttr ((A+".upAxis"),1)
            cmds.setAttr ((A+".worldUpType"),Atype)
            
            B = cmds.spaceLocator(p=(0,0,0),n=self.Curvename+"_Loc"+str(i))
            qwe = cmds.pickWalk(qw,d='down')
            cmds.connectAttr((qwe[0]+".worldSpace[0]"),(A+".geometryPath"),f=1)   #连接曲线Shape和路径动画
            
            if cmds.objExists(sel[0]+".V"+str(i)) == 0:
                cmds.addAttr(sel[0],ln=("V"+str(i)),at='double',min=0,max=1,dv=0)   #添加属性 -ln属性名 -at类型 最大最小值
                cmds.setAttr((sel[0]+".V"+str(i)),e=1,keyable=True)   #打开属性的可编辑

            cmds.connectAttr((sel[0]+".V"+str(i)),(A+".uValue"),f=1)  #连接曲线的V*属性 到路径动画的U值
            cmds.connectAttr((A+".allCoordinates"),(B[0]+".translate"),f=1)   #路径动画的xxx属性(在路径动画上的世界位置) 到locater的位移
            cmds.connectAttr((A+".rotate"),(B[0]+".rotate"),f=1)
            if Atype == 2:
                cmds.pathAnimation(A,e=1,wuo=sel[1])
            q = 1.0*(i)/int(JointNum)
            cmds.setAttr(sel[0]+".V"+str(i),q)
            mz_dd.append(A)
            mz_Loc.append(B[0])
        totalTime = cmds.timerX(startTime=startTime)
        #print (totalTime) 
        cmds.select(cl=1)
        Qv = cmds.xform(mz_Loc[0],q=1,ws=1,t=1)
        yt = cmds.joint(p=(Qv[0] ,Qv[1] ,Qv[2]),n=self.Curvename+"_Jot0")
        mz_jot = []
        mz_jot.append(yt)
        startTime1 = cmds.timerX()
        for i in range(1,len(mz_Loc),1):
            Qv = cmds.xform(mz_Loc[i],q=1,ws=1,t=1)
            yt = cmds.joint(p=(Qv[0] ,Qv[1] ,Qv[2]),n=(self.Curvename+"_Jot"+str(i)))
            io = i-1
            cmds.joint(self.Curvename+"_Jot"+str(io) ,e=1, zso=1 , oj='xyz')
            mz_jot.append(yt)
        cmds.select(cl=1)
        cmds.setAttr((mz_jot[len(mz_jot)-1]+".jointOrientX"),0)
        cmds.setAttr((mz_jot[len(mz_jot)-1]+".jointOrientY"),0)
        cmds.setAttr((mz_jot[len(mz_jot)-1]+".jointOrientY"),0)
        totalTime1 = cmds.timerX(startTime=startTime1)
        #print (totalTime1)
        if cmds.objExists(sel[0]+".AutoLe") == 0:
			cmds.addAttr(sel[0],ln="AutoLe",at='double',min=0,max=1,dv=0)
			cmds.setAttr(sel[0]+".AutoLe",e=1,keyable=1)
        if cmds.objExists(sel[0]+".scaleAttr") == 0:
			cmds.addAttr(sel[0],ln="scaleAttr",at='double',dv=1)
			cmds.setAttr(sel[0]+".scaleAttr",e=1,keyable=1)
        startTime2 = cmds.timerX()
        for i in range(1,len(mz_dd),1):
            mz_dB = cmds.createNode( 'distanceBetween',n=(mz_dd[i]+"_dB"))

            cmds.connectAttr((mz_dd[i-1]+".allCoordinates"),(mz_dd[i]+"_dB.point1"),f=1)
            cmds.connectAttr( (mz_dd[i]+".allCoordinates"),(mz_dd[i]+"_dB.point2"),f=1)
            gh=cmds.getAttr ((mz_dd[i]+"_dB.distance"))

            cmds.createNode( 'multiplyDivide',n=(mz_dd[i]+"_dB_MPA"))
            cmds.connectAttr((mz_dd[i]+"_dB.distance"),(mz_dd[i]+"_dB_MPA.input1X"), f=1)
            cmds.connectAttr( (sel[0]+".scaleAttr"), (mz_dd[i]+"_dB_MPA.input2X"), f=1)
            cmds.setAttr((mz_dd[i]+"_dB_MPA.operation"),2)

            cmds.createNode('blendColors',n=(mz_dd[i]+"_blendC"))
            cmds.connectAttr((sel[0]+".AutoLe"),(mz_dd[i]+"_blendC.blender"), f=1)
            cmds.connectAttr((mz_dd[i]+"_dB_MPA.outputX"),(mz_dd[i]+"_blendC.color1R"), f=1)
            cmds.setAttr((mz_dd[i]+"_blendC.color2R"),gh)
            cmds.connectAttr( (mz_dd[i]+"_blendC.outputR"),(mz_jot[i]+".translateX"), f=1)
        totalTime2 = cmds.timerX(startTime=startTime2)
        #print (totalTime2)
        cmds.ikHandle(sol='ikSplineSolver',ccv=0,startJoint=mz_jot[0],endEffector=mz_jot[len(mz_jot)-1],curve=sel[0],n=(self.Curvename+"_SplineIkHandle"))
        cmds.select (sel[0])
        cmds.delete(mz_Loc)
        self.doFinish()

    def doFinish(self):
        if '_OutFX' in self.Curvename:
            editname = self.Curvename.rsplit('_',1)[0]
            cmds.group(editname, editname + '_clu*Handle', editname + '_cluHandle_Ctrl_grp',
                        editname + '_toFX', self.Curvename, self.Curvename + '_dupCurve',
                        self.Curvename + '_Jot0', self.Curvename + '_SplineIkHandle', n=editname + '_grp')
            cmds.hide(editname + '_clu*Handle', self.Curvename + '_dupCurve', self.Curvename + '_SplineIkHandle')
            if cmds.ls('buildPose') and cmds.ls('DeformationSystem'):
                cmds.setAttr('buildPose.udAttr',cmds.getAttr('buildPose.udAttr')+'/*addItem*/xform -os -t 0 0 0 -ro 0 0 0 \"'+editname+'_clu*Handle_Ctrl\";',type='string')

        else:
            cmds.group(self.Curvename, self.Curvename + '_clu*Handle', self.Curvename + '_cluHandle_Ctrl_grp', self.Curvename + '_dupCurve',
                        self.Curvename + '_Jot0', self.Curvename + '_SplineIkHandle', n=self.Curvename + '_grp')
            cmds.hide(self.Curvename + '_clu*Handle', self.Curvename + '_dupCurve', self.Curvename + '_SplineIkHandle')
            if cmds.ls('buildPose') and cmds.ls('DeformationSystem'):
                cmds.setAttr('buildPose.udAttr',cmds.getAttr('buildPose.udAttr')+'/*addItem*/xform -os -t 0 0 0 -ro 0 0 0 \"'+self.Curvename+'_clu*Handle_Ctrl\";',type='string')

class ApplePieA_Dynamic(object):

    def __init__(self):
        #super(ApplePieA_Dynamic, self).__init__()
        pass

    def Ready_selectCurve(self):
        curves = cmds.ls(sl=1)
        if not curves:
            ui_variable['Statusbar'].showMessage(u"//请选一根曲线")
            cmds.error()
        elif len(curves) > 1:
            ui_variable['Statusbar'].showMessage(u"//请选一根曲线")
            cmds.error()
        if not cmds.listRelatives(s=1, type='nurbsCurve'):
            ui_variable['Statusbar'].showMessage(u"//请选一根曲线")
            cmds.error()
        ui_variable['getCurveGrp'].setText(curves[0])
        #cmds.textFieldGrp('FXCurveNameTextFieldGrp',e=1,tx=curves[0])

    def Acondition(self, mode):
        if mode == 'Nucleus':
            if ui_variable['SelectNucleus'].currentText() == 'Create New':
                ui_variable['SelectHairSystem'].setEnabled(False)
                ui_variable['SelectFollicle'].setEnabled(False)
            else:
                ui_variable['SelectHairSystem'].setEnabled(True)
                ui_variable['SelectFollicle'].setEnabled(True)
        elif mode == 'HairSystem':
            if ui_variable['SelectHairSystem'].currentText() == 'Create New':
                ui_variable['SelectFollicle'].setEnabled(False)
            else:
                ui_variable['SelectFollicle'].setEnabled(True)

    def Ready_GetNode(self, mode):
        if mode == 'HairSystem':
            ui_variable['SelectHairSystem'].clear()
            #MenuItem = cmds.optionMenu(pTCIK.HairSystemMenu+'|OptionMenu',q=1,ill=1)
            #if MenuItem:
            #   for i in MenuItem:
            #        cmds.deleteUI(i)
            #cmds.menuItem(parent=(pTCIK.HairSystemMenu+'|OptionMenu'),label='CreateNew')
            hairsystemitem = cmds.listRelatives(cmds.ls(type='hairSystem'),p=1)
            if hairsystemitem:
                for i in hairsystemitem:
                    ui_variable['SelectHairSystem'].addItem(i)
                    #cmds.menuItem(parent=(pTCIK.HairSystemMenu+'|OptionMenu'),label=i)
            ui_variable['SelectHairSystem'].addItem('Create New')
        elif mode == 'Follicle':
            ui_variable['SelectFollicle'].clear()
            ui_variable['SelectFollicle'].addItem('Create New')
            follicleitem = cmds.listRelatives(cmds.ls(type='follicle'),p=1)
            if follicleitem:
                for i in follicleitem:
                    ui_variable['SelectFollicle'].addItem(i)
            #ui_variable['SelectFollicle'].setCurrentIndex(-1)
        elif mode == 'Nucleus':
            ui_variable['SelectNucleus'].clear()
            nucleusitem = cmds.ls(type='nucleus')
            if nucleusitem:
                for i in nucleusitem:
                    ui_variable['SelectNucleus'].addItem(i)
            ui_variable['SelectNucleus'].addItem('Create New')
            ui_variable['SelectNucleus'].setCurrentIndex(-1)

    def ifdef(self):
        self.qComboBox = {}
        self.qComboBox['HairSystem'] = ui_variable['SelectHairSystem'].currentText()
        self.qComboBox['Follicle'] = ui_variable['SelectFollicle'].currentText()
        self.qComboBox['Nucleus']= ui_variable['SelectNucleus'].currentText()
        Anucleus = cmds.ls(type="nucleus")
        Afollicle = cmds.ls(type="follicle")
        AhairSystem = cmds.ls(type="hairSystem")
        if self.qComboBox['Nucleus'] == 'Create New' or not Anucleus:
            self.qComboBox['Nucleus'] = cmds.createNode('nucleus')
            cmds.connectAttr('time1.outTime',self.qComboBox['Nucleus']+".currentTime")
            if cmds.upAxis(q=1,axis=1) == "z":
                cmds.setAttr(self.qComboBox['Nucleus'] + ".gravityDirection", 0, 0, -1)
        if not self.qComboBox['Nucleus']:
            if len(Anucleus) == 1:
                self.qComboBox['Nucleus'] = Anucleus[0]
            elif len(Anucleus) > 1:
                ui_variable['SelectNucleus'].setVisible(True)
                ui_variable['Statusbar'].showMessage(u"//检测到多个解算器，请选择要使用的解算器")
                cmds.error()
        if self.qComboBox['Follicle'] == 'Create New' or not Afollicle:
            self.qComboBox['Follicle'] = cmds.createNode('follicle')
        elif self.qComboBox['Follicle'] != 'Create New':
            self.qComboBox['Follicle'] = cmds.listRelatives(self.qComboBox['Follicle'], s=1)
        if self.qComboBox['HairSystem'] == 'Create New' or not AhairSystem:
            self.qComboBox['HairSystem'] = cmds.createNode('hairSystem')
        elif self.qComboBox['HairSystem'] != 'Create New':
            self.qComboBox['HairSystem'] = cmds.listRelatives(self.qComboBox['HairSystem'], s=1)[0]
        cmds.setAttr(self.qComboBox['Follicle'] + ".pointLock", 1)
        cmds.setAttr(self.qComboBox['Follicle'] + ".restPose", 1)
        cmds.setAttr(self.qComboBox['Follicle'] + ".startDirection", 1)
        cmds.setAttr(self.qComboBox['Follicle'] + ".degree", 3)
        if not cmds.connectionInfo(self.qComboBox['HairSystem']+".nextState",sfd=1):
            mm.eval("addActiveToNSystem(\"" + cmds.listRelatives(self.qComboBox['HairSystem'], p=1)[0] +"\",\""+ self.qComboBox['Nucleus']+"\");")
            cmds.connectAttr('time1.outTime', self.qComboBox['HairSystem'] + '.currentTime', f=1)
            cmds.connectAttr(self.qComboBox['Nucleus'] + '.startFrame', self.qComboBox['HairSystem'] + '.startFrame', f=1)
        if not cmds.connectionInfo(self.qComboBox['Follicle'] + ".currentPosition", sfd=1):
            follicleNum = cmds.listRelatives(cmds.listRelatives(self.qComboBox['HairSystem'], p=1)[0], c=1, type='transform')
            if not follicleNum:
                cmds.connectAttr(self.qComboBox['HairSystem']+'.outputHair[0]',self.qComboBox['Follicle']+'.currentPosition',f=1)
                cmds.connectAttr(self.qComboBox['Follicle']+'.outHair',self.qComboBox['HairSystem']+'.inputHair[0]',f=1)
            else:
                cmds.connectAttr(self.qComboBox['HairSystem']+'.outputHair['+str(len(follicleNum))+']',self.qComboBox['Follicle']+'.currentPosition',f=1)
                cmds.connectAttr(self.qComboBox['Follicle']+'.outHair',self.qComboBox['HairSystem']+'.inputHair['+str(len(follicleNum))+']',f=1)
        if not cmds.listRelatives(cmds.listRelatives(self.qComboBox['HairSystem'], p=1)[0], p=1):
            cmds.parent(cmds.listRelatives(self.qComboBox['HairSystem'], p=1)[0],self.qComboBox['Nucleus'])
        if not cmds.listRelatives(cmds.listRelatives(self.qComboBox['Follicle'], p=1), p=1) == cmds.listRelatives(self.qComboBox['HairSystem'], p=1)[0]:
            cmds.parent(cmds.listRelatives(self.qComboBox['Follicle'], p=1), cmds.listRelatives(self.qComboBox['HairSystem'], p=1)[0])
            
    def FXCurve(self):
        self.ifdef()
        ApplePieA_Dynamic().Ready_GetNode('HairSystem')
        ApplePieA_Dynamic().Ready_GetNode('Follicle')
        ApplePieA_Dynamic().Ready_GetNode('Nucleus')
        curve = ui_variable['getCurveGrp'].text()
        #print (self.qComboBox['HairSystem'])
        #print (self.qComboBox['Follicle'])
        #print (self.qComboBox['Nucleus'])
        recurve = cmds.rebuildCurve(curve, ch=1, rpo=0, rt=0, end=1, kr=0, kcp=0, kep=1, kt=0, s=cmds.getAttr(curve+".controlPoints", size=1)+3, d=3, tol=0.01)
        cmds.rename(recurve[0], curve + '_toFX')
        #cmds.parent(curve + '_toFX', cmds.listRelatives(self.qComboBox['Follicle'], p=1))
        cmds.connectAttr(cmds.listRelatives(curve + '_toFX', s=1, type='nurbsCurve')[0]+'.local', self.qComboBox['Follicle']+'.startPosition', f=1)
        cmds.connectAttr(curve + '_toFX.worldMatrix[0]', self.qComboBox['Follicle']+'.startPositionMatrix',f=1)
        cmds.circle(n=curve + '_OutFX')
        cmds.connectAttr(self.qComboBox['Follicle'] + '.outCurve', curve + '_OutFXShape.create', f=1)
        ui_variable['CurveName'].setText(curve + '_OutFX')
        ui_variable['getCurveGrp'].clear()

class poseEdit(object):
    def __init__(self):
        pass

    def PoseCheck(self):
        if not cmds.ls('buildPose.udAttr'):
            ui_variable['Statusbar'].showMessage(u"//无Pose系统")
            cmds.error("无Pose系统")
        self.buildposeText = cmds.getAttr('buildPose.udAttr')
        splitbuild = self.buildposeText.split('/*addItem*/')
        del splitbuild[0]
        splitText = [splitbuild[i].split('xform -os -t 0 0 0 -ro 0 0 0 ')[1] for i in range(len(splitbuild))]
        uiPose = 'ListA'
        try:
            cmds.deleteUI(uiPose)
        except:
            pass
        cmds.window(uiPose, t=('List'))
        cmds.columnLayout(rowSpacing=5)
        cmds.textScrollList('textList', numberOfRows=20,showIndexedItem=4)
        cmds.button('Add', l="Add", h=28,w=100,c=lambda*args: self.PoseEdit('add'))
        cmds.button('Delete', l="Delete", h=28,w=100,c=lambda*args: self.PoseEdit('delete'))
        cmds.showWindow(uiPose)
        ls = cmds.ls(type='transform')
        for i in splitText:
            if '_clu*Handle_Ctrl' in i:
                self.editi = (i.split('_clu*Handle_Ctrl\";')[0]).split('\"', 1)[1]
            else:
                self.editi = (i.split('\"',1)[1]).rsplit('\"',1)[0]
            if self.editi in ls:
                cmds.textScrollList('textList', e=1, append=i)
            else:
                cmds.textScrollList('textList', e=1, append=i + '  //NeedDelete//')

    def PoseEdit(self, mode):
        if mode == 'delete':
            poseSplit = self.buildposeText.split('/*addItem*/xform -os -t 0 0 0 -ro 0 0 0 ' + cmds.textScrollList('textList', q=1, selectItem=1)[0].split(';')[0] + ';')
            cmds.setAttr('buildPose.udAttr', poseSplit[0] + poseSplit[1],type='string')
            cmds.textScrollList('textList', e=1, rii=cmds.textScrollList('textList', q=1, sii=1)[0])
        elif mode == 'add':
            if cmds.promptDialog(title='addPose', button=['OK', 'Cancel'], defaultButton='OK', cancelButton='Cancel', dismissString='Cancel') == 'OK':
                inputText = cmds.promptDialog(query=True, text=True)
                lsinput = cmds.ls(inputText)
                if not lsinput:
                    cmds.error('无此物体')
                elif len(lsinput) >= 2:
                    cmds.error('有重复物体')
                cmds.setAttr('buildPose.udAttr', cmds.getAttr('buildPose.udAttr') + '/*addItem*/xform -os -t 0 0 0 -ro 0 0 0 \"' + inputText + '\";', type='string')

class oneBuildIK(object):
    def __init__(self):
        pass
    
    def getNum(self):
        uioneBuild = 'oneA'
        try:
            cmds.deleteUI(uioneBuild)
        except:
            pass
        cmds.window(uioneBuild, t=('Create'))
        cmds.columnLayout(rowSpacing=5)
        #cmds.button('oneBuildIK', l="一键生成", h=28,w=150,c=lambda*args: pass)
        cmds.window(uioneBuild, e=True, wh=(150, 100))
        cmds.showWindow(uioneBuild)
        
        #选模型上的线——>指定段数——>指定系列曲线名——>指定段数——>创建控制——>切线约束——>约束控制——>可选层级——>动力学曲线截取——>生成动力学——>生成IK
        #选线——>指定段数——>创建控制——>切线约束——>约束控制——>可选层级——>动力学曲线截取——>生成动力学——>生成IK
        
    def oneBuild(self):
        pass
win = Showwindow()
win.show()