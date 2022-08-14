# -*- coding: UTF-8 -*-
from PySide2.QtWidgets import QWidget, QLineEdit
import shiboken2
from maya import cmds, mel
from maya import OpenMayaUI as OmUI
from maya.api import OpenMaya as om


class DisplayYes():

    def __init__(self):
        gCommandLine = mel.eval('$tmp = $gCommandLine')
        self.widget = shiboken2.wrapInstance(int(OmUI.MQtUtil.findControl(gCommandLine)), QWidget)

    def showMessage(self, message):
        self.widget.findChild(QLineEdit).setStyleSheet('background-color: #a1c17e; color:black;')
        cmds.select('time1', r=1)
        cmds.scriptJob(e=['SelectionChanged', lambda *args: self.resetLine()], ro=1)
        om.MGlobal.displayInfo(message)

    def resetLine(self):
        #cmds.deleteUI(self.gCommandLine.rsplit('|', 1)[0])
        #mel.eval('source "initCommandLine.mel"')
        self.widget.findChild(QLineEdit).setStyleSheet('')