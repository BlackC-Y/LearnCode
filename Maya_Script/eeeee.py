from __future__ import print_function
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
import maya.cmds as cmds
import maya.mel as mm
import random,threading,time

class Ui_tcsWin(object):
    def setupUi(self, tcsWin):
        tcsWin.setObjectName("tcsWin")
        tcsWin.resize(200, 300)
        self.NewSButton = QPushButton(tcsWin)
        self.NewSButton.setGeometry(QRect(100, 100, 75, 25))
        self.NewSButton.setObjectName("NewSButton")
        self.StartButton = QPushButton(tcsWin)
        self.StartButton.setGeometry(QRect(100, 150, 75, 25))
        self.StartButton.setObjectName("StartButton")
        self.NewS = QLabel(tcsWin)
        self.NewS.setGeometry(QRect(10, 100, 70, 20))
        self.NewS.setObjectName("NewS")
        self.SaveWarning = QLabel(tcsWin)
        self.SaveWarning.setGeometry(QRect(80, 30, 50, 20))
        self.SaveWarning.setObjectName("SaveWarning")

        self.retranslateUi(tcsWin)
        QMetaObject.connectSlotsByName(tcsWin)

    def retranslateUi(self, tcsWin):
        tcsWin.setWindowTitle(QApplication.translate("tcsWin", "Form", None, -1))
        self.NewSButton.setText(QApplication.translate("tcsWin", "New Files", None, -1))
        self.StartButton.setText(QApplication.translate("tcsWin", "Play", None, -1))
        self.NewS.setText(QApplication.translate("tcsWin", "Create New Files>", None, -1))
        self.SaveWarning.setText(QApplication.translate("tcsWin", "Save Files", None, -1))
        
class Bwindow(Ui_tcsWin, QWidget):
    
    def __init__(self):
        super(Bwindow, self).__init__()
        self.setupUi(self)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowTitle("emmm")
        self.show()
        #self.timer = QBasicTimer()
        #self.timer.start(300,self)

        self.NewSButton.clicked.connect(lambda *args: cmds.file(f=1, new=1))
        self.StartButton.clicked.connect(lambda *args: tcsnake().loading())
        
    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Left:
            tcsnake.oxy = 0
            tcsnake.PaN = -1
        elif key == Qt.Key_Right:
            tcsnake.oxy = 0
            tcsnake.PaN = 1
        elif key == Qt.Key_Down:
            tcsnake.oxy = 1
            tcsnake.PaN = -1
        elif key == Qt.Key_Up:
            tcsnake.oxy = 1
            tcsnake.PaN = 1
        else:
            super(tcsnake, self).keyPressEvent(event)
        tcsnake().timetodo()

win = Bwindow()

class tcsnake(object):

    oxy = 1
    PaN = 1
    timeroot = 0.0

    def __init__(self):
        super(tcsnake, self).__init__()
        #self.t = time.time()
        self.HeadN = 'Head'
        # cmds.ToggleGrid()

    def loading(self):
        cmds.camera(o=1, ow=60, p=(0, 0, 1000), n='GCamera')
        cmds.setAttr("GCameraShape2.ow", l=1)
        mm.eval("lookThroughModelPanel GCamera1 modelPanel4")
        cmds.setAttr("hardwareRenderingGlobals.multiSampleEnable", 0)

        C = [[1,0,0],[1,1,0],[0,1,0],[0,1,1],[0,0,1],[1,0,1],[1,1,1],[0,0,0]]
        for i in range(1, 9, 1):
            lam_M = cmds.createNode('lambert', n='color'+str(i))
            cmds.sets(renderable=1, nss=1, empty=1, name=(lam_M+'SG'))
            cmds.connectAttr((lam_M+'.outColor'),(lam_M+'SG.surfaceShader'), f=1)
            cmds.setAttr((lam_M+".color"), C[i-1][0], C[i-1][1], C[i-1][2], type='double3')
        
        self.dieWall()
        self.CHead()
        self.Cfood()
        #self.time_root()
        #cmds.timer(s=1,n='snaketime')
        #self.timer = QBasicTimer()
        #self.timer.start(300,self)
    
    def dieWall(self):
        for i in range(2):
            if i == 0:
                for i in range(-30,31,2):
                    _wall = cmds.polyCube(n='_wallA')
                    self.setAttt(_wall[0],1,13)
                    self.setAttt(_wall[0],0,i)
                    self.colorshape(_wall[0], 8)
                for i in range(-13,14,2):
                    _wall = cmds.polyCube(n='_wallC')
                    self.setAttt(_wall[0],1,i)
                    self.setAttt(_wall[0],0,-30)
                    self.colorshape(_wall[0], 8)
            else:
                for i in range(-30,31,2):
                    _wall = cmds.polyCube(n='_wallB')
                    self.setAttt(_wall[0],1,-13)
                    self.setAttt(_wall[0],0,i)
                    self.colorshape(_wall[0], 8)
                for i in range(-13,14,2):
                    _wall = cmds.polyCube(n='_wallD')
                    self.setAttt(_wall[0],1,i)
                    self.setAttt(_wall[0],0,30)
                    self.colorshape(_wall[0], 8)
        cmds.group("_wall*",n='dieWall_grp')
    
    def time_root(self):
        self.timer = cmds.timer(n='snaketime',lap=1)
        print (self.timer)

    def timerEvent(self):
        tcsnake.timeroot += 1.0
        _root = tcsnake.timeroot / 6.0
        _introot = str(_root).split('.')[1]
        if (int(_introot) == 0):
            self.timetodo()
        else:
            pass

    def setAttt(self, poly, mode, value):
        if str(mode) == '0':
            mode = '.tx'
        elif str(mode) == '1':
            mode = '.ty'
        cmds.setAttr(poly + mode, int(value))

    def colorshape(self, poly, color):
        if color == '':
            color = random.randint(1, 6)
        cmds.sets(poly, e=1, forceElement=('color'+str(color)+'SG'))

    def CHead(self):
        cmds.polyCube(n='Head')
        self.colorshape('Head', 7)
        self.CBody(-1,0)

    def CBody(self,Tx, Ty):
        BodyA = cmds.polyCube(n='body')
        cmds.displaySmoothness(BodyA[0], divisionsU=3, divisionsV=3, pointsWire=16, pointsShaded=4, polygonObject=3)
        cmds.setAttr(BodyA[0]+'.tx', Tx)
        cmds.setAttr(BodyA[0] + '.ty', Ty)
        cmds.select(cl=1)

    def Cfood(self):
        cmds.polyCube(n='SFood')
        self.colorshape('SFood', 1)
        cmds.displaySmoothness('SFood', divisionsU=3, divisionsV=3, pointsWire=16, pointsShaded=4, polygonObject=3)
        self.setAttt('SFood',1,(random.randint(-12,12)))
        self.setAttt('SFood',0,(random.randint(-29,29)))

    def timetodo(self):
        HeadT = cmds.xform('Head', q=1, ws=1, t=1)
        bodyN = len(cmds.ls('body*', typ='transform'))
        bodyT = [[0 for y in range(3)] for x in range(bodyN)]
        for i in range(bodyN-1, -1, -1):
            if i == 0:
                bodyT[0] = cmds.xform('body', q=1, ws=1, t=1)
            else:
                bodyT[i] = cmds.xform('body' + str(i), q=1, ws=1, t=1)
        for o in range(bodyN-1, 0, -1):
            self.setAttt('body' + str(o), 0, bodyT[o-1][0])
            self.setAttt('body' + str(o), 1, bodyT[o-1][1])
        self.setAttt('body', 0, HeadT[0])
        self.setAttt('body', 1, HeadT[1])
        value = 0
        if tcsnake.oxy == 0:
            value = HeadT[0] + tcsnake.PaN
        elif tcsnake.oxy == 1:
            value = HeadT[1] + tcsnake.PaN
        self.setAttt('Head', tcsnake.oxy, value)

        HeadTA = cmds.xform('Head', q=1, ws=1, t=1)
        if HeadTA[1] == 22 or HeadTA[1] == -22 or HeadTA[0] == 50 or HeadTA[0] == -50:
            self.over()
        FoodT = cmds.xform('SFood',q=1,ws=1,t=1)
        if HeadTA == FoodT:
            cmds.delete('SFood')
            self.Cfood()
            self.CBody(bodyT[bodyN-1][0], bodyT[bodyN-1][1])
        for ch in range(bodyN-1):
            if HeadTA == bodyT[ch]:
                self.over()

    def over(self):
        print ('Die')
