# -*- coding: UTF-8 -*-
from MyToolBox.qt_core import *


style = '''
QPushButton {{
	border: none;
    padding-left: 10px;
    padding-right: 5px;
    font: "{_font}";
    color: {_color};
	border-radius: {_radius};	
	background-color: {_bg_color};
}}
QPushButton:hover {{
	background-color: {_bg_color_hover};
}}
QPushButton:pressed {{	
	background-color: {_bg_color_pressed};
}}
'''


class cusPushButton(QPushButton):
    def __init__(self, 
        text,
        radius,
        color,
        bg_color,
        bg_color_hover,
        bg_color_pressed,
        parent = None,
        app_parent = None,
        dark_one = "#1b1e23",
        text_foreground = "#8a95aa",
        top_margin = 40,
        font = 'Segoe UI',
        tooltip_text = '',
        context_color = "#568af2",
        minHeight = 0
    ):
        super().__init__()

        # SET PARAMETRES
        self.setText(text)
        if parent != None:
            self.setParent(parent)
        #self.setCursor(Qt.PointingHandCursor)

        self._parent = parent
        self._top_margin = top_margin

        # TOOLTIP
        self._tooltip_text = tooltip_text
        if self._tooltip_text:
            self._tooltip = _ToolTip(
                font,
                app_parent,
                tooltip_text,
                dark_one,
                context_color,
                text_foreground
            )
            self._tooltip.hide()

        # SET STYLESHEET
        custom_style = style.format(
            _font = font,
            _color = color,
            _radius = radius,
            _bg_color = bg_color,
            _bg_color_hover = bg_color_hover,
            _bg_color_pressed = bg_color_pressed
        )
        self.setStyleSheet(custom_style)

        if minHeight:
            self.setMinimumHeight(minHeight)

    # MOUSE OVER
    # Event triggered when the mouse is over the BTN
    # ///////////////////////////////////////////////////////////////
    def enterEvent(self, event):
        if self._tooltip_text:
            self.move_tooltip()
            self._tooltip.show()

    # MOUSE LEAVE
    # Event fired when the mouse leaves the BTN
    # ///////////////////////////////////////////////////////////////
    def leaveEvent(self, event):
        if self._tooltip_text:
            self.move_tooltip()
            self._tooltip.hide()

        # MOVE TOOLTIP
    # ///////////////////////////////////////////////////////////////
    def move_tooltip(self):
        if self._tooltip_text:
            # GET MAIN WINDOW PARENT
            gp = self.mapToGlobal(QPoint(0, 0))

            # SET WIDGET TO GET POSTION
            # Return absolute position of widget inside app
            pos = self._parent.mapFromGlobal(gp)

            # FORMAT POSITION
            # Adjust tooltip position with offset
            pos_x = (pos.x() - (self._tooltip.width() // 2)) + (self.width() // 2)
            pos_y = pos.y() - self._top_margin

            # SET POSITION TO WIDGET
            # Move tooltip position
            self._tooltip.move(pos_x, pos_y)


class _ToolTip(QLabel):
    # TOOLTIP / LABEL StyleSheet
    style_tooltip = """ 
    QLabel {{		
        background-color: {_dark_one};	
        color: {_text_foreground};
        padding-left: 10px;
        padding-right: 10px;
        border-radius: 17px;
        border: 0px solid transparent;
        border-left: 3px solid {_context_color};
        font: 800 9pt "{_font}";
    }}
    """

    def __init__(self,
        font,
        parent, 
        tooltip,
        dark_one,
        context_color,
        text_foreground
    ):
        QLabel.__init__(self)

        # LABEL SETUP
        style = self.style_tooltip.format(
            _dark_one = dark_one,
            _context_color = context_color,
            _text_foreground = text_foreground,
            _font = font
        )
        self.setObjectName(u"label_tooltip")
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet(style)
        self.setMinimumHeight(22)
        self.setParent(parent)
        self.setText(tooltip)
        self.adjustSize()
        self.setFixedHeight(self.height() + 12)

        # SET DROP SHADOW
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(30)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 80))
        self.setGraphicsEffect(self.shadow)
