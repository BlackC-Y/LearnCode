# -*- coding: UTF-8 -*-
from MyToolBox.qt_core import *
from MyToolBox.gui.core.json_settings import Settings
from MyToolBox.gui.widgets.columns.ui_left_column import Ui_LeftColumn

from .cus_left_button import *


class cusLeftColumn(QWidget):
    # SIGNALS
    clicked = Signal(object)
    released = Signal(object)

    def __init__(self,
        parent,
        app_parent,
        text_title,
        text_title_size,
        text_title_color,
        dark_one,
        bg_color,
        btn_color,
        btn_color_hover,
        btn_color_pressed,
        icon_path,
        icon_color,
        icon_color_hover,
        icon_color_pressed,
        context_color,
        icon_close_path,
        radius = 8
	):
        super().__init__()

        # PARAMETERS
        self._parent = parent
        self._app_parent = app_parent
        self._text_title = text_title
        self._text_title_size = text_title_size
        self._text_title_color = text_title_color
        self._icon_path = icon_path
        self._dark_one = dark_one
        self._bg_color = bg_color
        self._btn_color = btn_color
        self._btn_color_hover = btn_color_hover
        self._btn_color_pressed = btn_color_pressed
        self._icon_color = icon_color
        self._icon_color_hover = icon_color_hover
        self._icon_color_pressed = icon_color_pressed
        self._context_color = context_color
        self._icon_close_path = icon_close_path
        self._radius = radius

        # SETUP UI
        self.setup_ui()

        # ADD LEFT COLUMN TO BG FRAME
        self.menus = Ui_LeftColumn()
        self.menus.setupUi(self.content_frame)

        # CONNECT SIGNALS
        self.btn_close.clicked.connect(self.btn_clicked)
        self.btn_close.released.connect(self.btn_released)

    # TITLE LEFT COLUMN EMIT SIGNALS
    # ///////////////////////////////////////////////////////////////
    def btn_clicked(self):
        self.clicked.emit(self.btn_close)
    
    def btn_released(self):
        self.released.emit(self.btn_close)

    # WIDGETS
    # ///////////////////////////////////////////////////////////////
    def setup_ui(self):
        settings = Settings()
        self.settings = settings.items

        # BASE LAYOUT
        self.base_layout = QVBoxLayout(self)
        self.base_layout.setContentsMargins(0,0,0,0)
        self.base_layout.setSpacing(0)

        # TITLE FRAME
        # ///////////////////////////////////////////////////////////////
        self.title_frame = QFrame()
        self.title_frame.setMaximumHeight(47)
        self.title_frame.setMinimumHeight(47)

        # TITLE BASE LAYOUT 
        self.title_base_layout = QVBoxLayout(self.title_frame)
        self.title_base_layout.setContentsMargins(5,3,5,3)

        # TITLE BG
        self.title_bg_frame = QFrame()
        self.title_bg_frame.setObjectName("title_bg_frame")
        self.title_bg_frame.setStyleSheet(f'''
        #title_bg_frame {{
            background-color: {self._bg_color};
            border-radius: {self._radius}px;
        }}
        ''')

        # LAYOUT TITLE BG
        self.title_bg_layout = QHBoxLayout(self.title_bg_frame)
        self.title_bg_layout.setContentsMargins(5,5,5,5)
        self.title_bg_layout.setSpacing(3)

        # ICON
        self.icon_frame = QFrame()
        self.icon_frame.setFixedSize(30,30)
        self.icon_frame.setStyleSheet("background: none;")
        self.icon_layout = QVBoxLayout(self.icon_frame)
        self.icon_layout.setContentsMargins(0,0,0,0)
        self.icon_layout.setSpacing(5)
        self.icon = cusIcon(self._icon_path, self._icon_color)
        self.icon_layout.addWidget(self.icon, Qt.AlignCenter, Qt.AlignCenter)

        # LABEL
        self.title_label = QLabel(self._text_title)
        self.title_label.setObjectName("title_label")
        self.title_label.setStyleSheet(f'''
        #title_label {{
            font-size: {self._text_title_size}pt;
            color: {self._text_title_color};
            padding-bottom: 2px;
            background: none;
        }}
        ''')

        # BTN FRAME
        self.btn_frame = QFrame()
        self.btn_frame.setFixedSize(30,30)
        self.btn_frame.setStyleSheet("background: none;")
        # CLOSE BUTTON
        self.btn_close = cusLeftButton(
            self._parent,
            self._app_parent,
            tooltip_text = "Hide",
            dark_one = self._dark_one,
            bg_color = self._btn_color,
            bg_color_hover = self._btn_color_hover,
            bg_color_pressed = self._btn_color_pressed,
            icon_color = self._icon_color,
            icon_color_hover = self._icon_color_hover,
            icon_color_pressed = self._icon_color_pressed,
            icon_color_active = self._icon_color_pressed,
            context_color = self._context_color,
            text_foreground = self._text_title_color,
            icon_path = self._icon_close_path,
            radius = 4,
            font = self.settings["font_family"]
        )
        self.btn_close.setParent(self.btn_frame)
        self.btn_close.setObjectName("btn_close_left_column")

        # ADD TO TITLE LAYOUT
        self.title_bg_layout.addWidget(self.icon_frame)
        self.title_bg_layout.addWidget(self.title_label)
        self.title_bg_layout.addWidget(self.btn_frame)

        # ADD TITLE BG TO LAYOUT
        self.title_base_layout.addWidget(self.title_bg_frame)

        # CONTENT FRAME
        # ///////////////////////////////////////////////////////////////
        self.content_frame = QFrame()
        self.content_frame.setStyleSheet("background: none")

        # ADD TO LAYOUT
        # ///////////////////////////////////////////////////////////////
        self.base_layout.addWidget(self.title_frame)
        self.base_layout.addWidget(self.content_frame)


class cusIcon(QWidget):
    
    def __init__(self, icon_path, icon_color):
        super().__init__()

        # PROPERTIES
        self._icon_path = icon_path
        self._icon_color = icon_color

        # SETUP UI
        self.setup_ui()

    def setup_ui(self):
        # LAYOUT
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0,0,0,0)

        # LABEL
        self.icon = QLabel()
        self.icon.setAlignment(Qt.AlignCenter)
        
        # PAINTER
        self.set_icon(self._icon_path, self._icon_color)

        # ADD TO LAYOUT
        self.layout.addWidget(self.icon)

    def set_icon(self, icon_path, icon_color = None):
        # GET COLOR
        color = ""
        if icon_color != None:
            color = icon_color
        else:
            color = self._icon_color

        # PAINTER / PIXMAP
        icon = QPixmap(icon_path)
        painter = QPainter(icon)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.fillRect(icon.rect(), color)       
        painter.end()

        # SET PIXMAP
        self.icon.setPixmap(icon)