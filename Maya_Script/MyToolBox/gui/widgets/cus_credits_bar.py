# -*- coding: UTF-8 -*-
from MyToolBox.qt_core import *


# PY CREDITS BAR AND VERSION
class cusCredits(QWidget):
    def __init__(self,
        information,
        version,
        bg_two,
        font_family,
        text_size,
        text_description_color,
        radius = 8,
        padding = 10
    ):
        super().__init__()

        # PROPERTIES
        self._information = information
        self._version = version
        self._bg_two = bg_two
        self._font_family = font_family
        self._text_size = text_size
        self._text_description_color = text_description_color
        self._radius = radius
        self._padding = padding

        # SETUP UI
        self.setup_ui()

    def setup_ui(self):
        # ADD LAYOUT
        self.widget_layout = QHBoxLayout(self)
        self.widget_layout.setContentsMargins(0,0,0,0)

        # BG STYLE
        style = f"""
        #bg_frame {{
            border-radius: {self._radius}px;
            background-color: {self._bg_two};
        }}
        .QLabel {{
            font: {self._text_size}pt "{self._font_family}";
            color: {self._text_description_color};
            padding-left: {self._padding}px;
            padding-right: {self._padding}px;
        }}
        """

        # BG FRAME
        self.bg_frame = QFrame()
        self.bg_frame.setObjectName("bg_frame")
        self.bg_frame.setStyleSheet(style)

        # ADD TO LAYOUT
        self.widget_layout.addWidget(self.bg_frame)

        # ADD BG LAYOUT
        self.bg_layout = QHBoxLayout(self.bg_frame)
        self.bg_layout.setContentsMargins(0,0,0,0)

        # ADD information TEXT
        self.information_label = QLabel(self._information)
        self.information_label.setAlignment(Qt.AlignVCenter)

        # ADD VERSION TEXT
        self.version_label = QLabel(self._version)
        self.version_label.setAlignment(Qt.AlignVCenter)

        # SEPARATOR
        self.separator = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        # ADD TO LAYOUT
        self.bg_layout.addWidget(self.information_label)
        self.bg_layout.addSpacerItem(self.separator)
        self.bg_layout.addWidget(self.version_label)
