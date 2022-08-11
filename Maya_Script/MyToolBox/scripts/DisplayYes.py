from PySide2.QtWidgets import *
import shiboken2
from maya import cmds, mel
from maya import OpenMayaUI as OmUI
from maya.api import OpenMaya as om


class DisplayYes():

    def __init__(self):
        gCommandLine = mel.eval('$tmp = $gCommandLine')
        self.widget = shiboken2.wrapInstance(int(OmUI.MQtUtil.findControl(gCommandLine)), QWidget)

    def showMessage(self, message):
        self.widget.findChild(QLineEdit).setStyleSheet('background-color:rgb(223,246,221); color:black;')
        cmds.select('time1', r=1)
        cmds.scriptJob(e=['SelectionChanged', 'DisplayYes().resetLine()'], ro=1)
        om.MGlobal.displayInfo(message)

    def resetLine(self):
        #cmds.deleteUI(self.gCommandLine.rsplit('|', 1)[0])
        #mel.eval('source "initCommandLine.mel"')
        self.widget.findChild(QLineEdit).setStyleSheet('')