# -*- coding: UTF-8 -*-
from MyToolBox.qt_core import *


class cusLableLine(QWidget):

    def __init__(self, directionStyle, color, Text, HW=20):
        super(cusLableLine, self).__init__()

        if directionStyle[0] == 'H':
            Ly = QHBoxLayout(self)
            Ly.setContentsMargins(5,0,5,0)
            Label = QLabel()
            Label.setMinimumHeight(HW)
            frame_line = QFrame()
            frame_line.setMaximumHeight(1)
            frame_line.setMinimumHeight(1)
            if directionStyle[1] == 'C':
                frame_line2 = QFrame()
                frame_line2.setStyleSheet("background: {};".format(color))
                frame_line2.setMaximumHeight(1)
                frame_line2.setMinimumHeight(1)
        elif directionStyle[0] == 'V':
            Ly = QVBoxLayout(self)
            Ly.setContentsMargins(0,5,0,5)
            Label = _VLabel()
            Label.setMinimumWidth(HW)
            frame_line = QFrame()
            frame_line.setMaximumWidth(1)
            frame_line.setMinimumWidth(1)
            if directionStyle[1] == 'C':
                frame_line2 = QFrame()
                frame_line2.setStyleSheet("background: {};".format(color))
                frame_line2.setMaximumWidth(1)
                frame_line2.setMinimumWidth(1)
        
        Ly.setSizeConstraint(QLayout.SetMinAndMaxSize)
        if directionStyle[1] == 'C':
            Ly.addWidget(frame_line)
            Ly.addWidget(Label)
            Ly.addWidget(frame_line2)
        elif directionStyle[1] == 'L':
            Ly.addWidget(Label)
            Ly.addWidget(frame_line)
        elif directionStyle[1] == 'R':
            Ly.addWidget(frame_line)
            Ly.addWidget(Label)
        Label.setStyleSheet("color: {};".format(color))
        Label.setAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
        Label.setText(Text)
        frame_line.setStyleSheet("background: {};".format(color))


class _VLabel(QLabel):
    
    def __init__(self):
        super(_VLabel, self).__init__()

    def initPainter(self, painter):
        painter.translate(self.width() / 2, self.height() / 2)
        painter.rotate(90)
        painter.translate(-self.width() / 2, -self.height() / 2)