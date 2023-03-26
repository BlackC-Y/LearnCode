# -*- coding: UTF-8 -*-
from MyToolBox.qt_core import *
from MyToolBox.gui.core.functions import Functions
from MyToolBox.gui.core.json_settings import Settings
from MyToolBox.gui.core.json_themes import Themes

from MyToolBox.gui.widgets import *
from MyToolBox.gui.widgets.columns.ui_right_column import Ui_RightColumn
from MyToolBox.gui.widgets.cus_credits_bar import cusCredits


class UI_MainWindow(object):
    def setup_ui(self, parent):
        if not parent.objectName():
            parent.setObjectName("MainWindow")

        # LOAD SETTINGS
        # ///////////////////////////////////////////////////////////////
        settings = Settings()
        self.settings = settings.items

        # LOAD THEME COLOR
        # ///////////////////////////////////////////////////////////////
        themes = Themes()
        self.themes = themes.items

        # SET INITIAL PARAMETERS
        parent.resize(self.settings["startup_size"][0], self.settings["startup_size"][1])
        parent.setMinimumSize(self.settings["minimum_size"][0], self.settings["minimum_size"][1])

        # SET CENTRAL WIDGET
        # Add central widget to app
        # ///////////////////////////////////////////////////////////////
        self.central_widget = QWidget()
        self.central_widget.setStyleSheet(f'''
            font: {self.settings["font"]["text_size"]}pt "{self.settings["font_family"]}";
            color: {self.themes["app_color"]["text_foreground"]};
        ''')
        self.central_widget_layout = QVBoxLayout(self.central_widget)
        if self.settings["custom_title_bar"]:
            self.central_widget_layout.setContentsMargins(10,10,10,10)
        else:
            self.central_widget_layout.setContentsMargins(0,0,0,0)
        
        # LOAD PY WINDOW CUSTOM WIDGET
        # Add inside cusWindow "layout" all Widgets
        # ///////////////////////////////////////////////////////////////
        self.window = cusWindow(
            parent,
            bg_color = self.themes["app_color"]["bg_one"],
            border_color = self.themes["app_color"]["bg_two"],
            text_color = self.themes["app_color"]["text_foreground"]
        )
        
        # If disable custom title bar
        if not self.settings["custom_title_bar"]:
            self.window.set_stylesheet(border_radius = 0, border_size = 0)
        
        # ADD PY WINDOW TO CENTRAL WIDGET
        self.central_widget_layout.addWidget(self.window)

        # ADD FRAME LEFT MENU
        # Add here the custom left menu bar
        # ///////////////////////////////////////////////////////////////
        left_menu_margin = self.settings["left_menu_content_margins"]
        left_menu_minimum = self.settings["left_menu_size"]["minimum"]
        self.left_menu_frame = QFrame()
        self.left_menu_frame.setMaximumSize(left_menu_minimum + (left_menu_margin * 2), 17280)
        self.left_menu_frame.setMinimumSize(left_menu_minimum + (left_menu_margin * 2), 0)

        # LEFT MENU LAYOUT
        self.left_menu_layout = QHBoxLayout(self.left_menu_frame)
        self.left_menu_layout.setContentsMargins(
            left_menu_margin,
            left_menu_margin,
            left_menu_margin,
            left_menu_margin
        )

        # ADD LEFT MENU
        # Add custom left menu here
        # ///////////////////////////////////////////////////////////////
        self.left_menu = cusLeftMenu(
            parent = self.left_menu_frame,
            app_parent = self.central_widget, # For tooltip parent
            dark_one = self.themes["app_color"]["dark_one"],
            dark_three = self.themes["app_color"]["dark_three"],
            dark_four = self.themes["app_color"]["dark_four"],
            bg_one = self.themes["app_color"]["bg_one"],
            icon_color = self.themes["app_color"]["icon_color"],
            icon_color_hover = self.themes["app_color"]["icon_hover"],
            icon_color_pressed = self.themes["app_color"]["icon_pressed"],
            icon_color_active = self.themes["app_color"]["icon_active"],
            context_color = self.themes["app_color"]["context_color"],
            text_foreground = self.themes["app_color"]["text_foreground"],
            text_active = self.themes["app_color"]["text_active"],
            minimum_width = self.settings["left_menu_size"]["minimum"],
            maximum_width = self.settings["left_menu_size"]["maximum"],
        )
        self.left_menu_layout.addWidget(self.left_menu)

        # ADD LEFT COLUMN
        # Add here the left column with Stacked Widgets
        # ///////////////////////////////////////////////////////////////
        self.left_column_frame = QFrame()
        self.left_column_frame.setMaximumWidth(self.settings["left_column_size"]["minimum"])
        self.left_column_frame.setMinimumWidth(self.settings["left_column_size"]["minimum"])
        self.left_column_frame.setStyleSheet("background: %s" %self.themes['app_color']['bg_two'])

        # ADD LAYOUT TO LEFT COLUMN
        self.left_column_layout = QVBoxLayout(self.left_column_frame)
        self.left_column_layout.setContentsMargins(0,0,0,0)

        # ADD CUSTOM LEFT MENU WIDGET
        self.left_column = cusLeftColumn(
            parent,
            app_parent = self.central_widget,
            text_title = "Settings Left Frame",
            text_title_size = self.settings["font"]["title_size"],
            text_title_color = self.themes['app_color']['text_foreground'],
            icon_path = Functions.set_svg_icon("icon_settings.svg"),
            dark_one = self.themes['app_color']['dark_one'],
            bg_color = self.themes['app_color']['bg_three'],
            btn_color = self.themes['app_color']['bg_three'],
            btn_color_hover = self.themes['app_color']['bg_two'],
            btn_color_pressed = self.themes['app_color']['bg_one'],
            icon_color = self.themes['app_color']['icon_color'],
            icon_color_hover = self.themes['app_color']['icon_hover'],
            context_color = self.themes['app_color']['context_color'],
            icon_color_pressed = self.themes['app_color']['icon_pressed'],
            icon_close_path = Functions.set_svg_icon("icon_close.svg")
        )
        self.left_column_layout.addWidget(self.left_column)

        # ADD RIGHT WIDGETS
        # Add here the right widgets
        # ///////////////////////////////////////////////////////////////
        self.right_app_frame = QFrame()

        # ADD RIGHT APP LAYOUT
        self.right_app_layout = QVBoxLayout(self.right_app_frame)
        self.right_app_layout.setContentsMargins(3,3,3,3)
        self.right_app_layout.setSpacing(6)

        # ADD TITLE BAR FRAME
        # ///////////////////////////////////////////////////////////////
        self.title_bar_frame = QFrame()
        self.title_bar_frame.setMinimumHeight(40)
        self.title_bar_frame.setMaximumHeight(40)
        self.title_bar_layout = QVBoxLayout(self.title_bar_frame)
        self.title_bar_layout.setContentsMargins(0,0,0,0)
        
        # ADD CUSTOM TITLE BAR TO LAYOUT
        self.title_bar = cusTitleBar(
            parent,
            logo_width = 100,
            app_parent = self.central_widget,
            logo_image = "logo_top_100x22.svg",
            bg_color = self.themes["app_color"]["bg_two"],
            div_color = self.themes["app_color"]["bg_three"],
            btn_bg_color = self.themes["app_color"]["bg_two"],
            btn_bg_color_hover = self.themes["app_color"]["bg_three"],
            btn_bg_color_pressed = self.themes["app_color"]["bg_one"],
            icon_color = self.themes["app_color"]["icon_color"],
            icon_color_hover = self.themes["app_color"]["icon_hover"],
            icon_color_pressed = self.themes["app_color"]["icon_pressed"],
            icon_color_active = self.themes["app_color"]["icon_active"],
            context_color = self.themes["app_color"]["context_color"],
            dark_one = self.themes["app_color"]["dark_one"],
            text_foreground = self.themes["app_color"]["text_foreground"],
            radius = 8,
            font_family = self.settings["font_family"],
            title_size = self.settings["font"]["title_size"],
            is_custom_title_bar = self.settings["custom_title_bar"]
        )
        self.title_bar_layout.addWidget(self.title_bar)

        # ADD CONTENT AREA
        # ///////////////////////////////////////////////////////////////
        self.content_area_frame = QFrame()

        # CREATE LAYOUT
        self.content_area_layout = QHBoxLayout(self.content_area_frame)
        self.content_area_layout.setContentsMargins(0,0,0,0)
        self.content_area_layout.setSpacing(0)

        # LEFT CONTENT
        self.content_area_left_frame = QFrame()

        # IMPORT MAIN PAGES TO CONTENT AREA
        self.load_pages = Ui_MainPages()
        self.load_pages.setupUi(self.content_area_left_frame)

        # RIGHT BAR
        self.right_column_frame = QFrame()
        self.right_column_frame.setMinimumWidth(self.settings["right_column_size"]["minimum"])
        self.right_column_frame.setMaximumWidth(self.settings["right_column_size"]["minimum"])

        # IMPORT RIGHT COLUMN
        # ///////////////////////////////////////////////////////////////
        self.content_area_right_layout = QVBoxLayout(self.right_column_frame)
        self.content_area_right_layout.setContentsMargins(5,5,5,5)
        self.content_area_right_layout.setSpacing(0)

        # RIGHT BG
        self.content_area_right_bg_frame = QFrame()
        self.content_area_right_bg_frame.setObjectName("content_area_right_bg_frame")
        self.content_area_right_bg_frame.setStyleSheet(f'''
        #content_area_right_bg_frame {{
            border-radius: 8px;
            background-color: {self.themes["app_color"]["bg_two"]};
        }}
        ''')

        # ADD BG
        self.content_area_right_layout.addWidget(self.content_area_right_bg_frame)

        # ADD RIGHT PAGES TO RIGHT COLUMN
        self.right_column = Ui_RightColumn()
        self.right_column.setupUi(self.content_area_right_bg_frame)

        # ADD TO LAYOUTS
        self.content_area_layout.addWidget(self.content_area_left_frame)
        self.content_area_layout.addWidget(self.right_column_frame)

        # CREDITS / BOTTOM APP FRAME
        # ///////////////////////////////////////////////////////////////
        self.credits_frame = QFrame()
        self.credits_frame.setMinimumHeight(26)
        self.credits_frame.setMaximumHeight(26)

        # CREATE LAYOUT
        self.credits_layout = QVBoxLayout(self.credits_frame)
        self.credits_layout.setContentsMargins(0,0,0,0)

        # ADD CUSTOM WIDGET CREDITS
        self.credits = cusCredits(
            bg_two = self.themes["app_color"]["bg_two"],
            information = self.settings["information"],
            version = self.settings["version"],
            font_family = self.settings["font_family"],
            text_size = self.settings["font"]["text_size"],
            text_description_color = self.themes["app_color"]["text_description"]
        )

        #  ADD TO LAYOUT
        self.credits_layout.addWidget(self.credits)

        # ADD WIDGETS TO RIGHT LAYOUT
        # ///////////////////////////////////////////////////////////////
        self.right_app_layout.addWidget(self.title_bar_frame)
        self.right_app_layout.addWidget(self.content_area_frame)
        self.right_app_layout.addWidget(self.credits_frame)
        
        # ADD WIDGETS TO "cusWindow"
        # Add here your custom widgets or default widgets
        # ///////////////////////////////////////////////////////////////
        self.window.layout.addWidget(self.left_menu_frame)
        self.window.layout.addWidget(self.left_column_frame)
        self.window.layout.addWidget(self.right_app_frame)

        # ADD CENTRAL WIDGET AND SET CONTENT MARGINS
        # ///////////////////////////////////////////////////////////////
        parent.setCentralWidget(self.central_widget)


class Ui_MainPages(object):
    def setupUi(self, MainPages):
        if not MainPages.objectName():
            MainPages.setObjectName(u"MainPages")
        MainPages.resize(860, 600)
        self.main_pages_layout = QVBoxLayout(MainPages)
        self.main_pages_layout.setSpacing(0)
        self.main_pages_layout.setObjectName(u"main_pages_layout")
        self.main_pages_layout.setContentsMargins(5, 5, 5, 5)
        self.pages = QStackedWidget(MainPages)
        self.pages.setObjectName(u"pages")
        self.page_1 = QWidget()
        self.page_1.setObjectName(u"page_1")
        self.page_1.setStyleSheet(u"font-size: 8pt")
        self.page_1_HLayout = QHBoxLayout(self.page_1)
        self.page_1_HLayout.setSpacing(60)
        self.page_1_HLayout.setContentsMargins(30, 10, 30, 10)
        self.left_tool_layout = QVBoxLayout()
        self.left_tool_layout.setSpacing(5)
        self.left_tool_layout.setContentsMargins(0,0,0,0)
        self.left_scrollArea = QScrollArea(self.page_1)
        self.left_scrollArea.setWidgetResizable(True)
        self.left_scrollArea.setStyleSheet(u"background: transparent;")
        self.left_scrollArea.setFrameShape(QFrame.NoFrame)
        self.left_scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.left_scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.left_scrollAreaWidgetContents = QWidget()
        self.left_scrollArea_VLayout = QVBoxLayout(self.left_scrollAreaWidgetContents)
        self.left_scrollArea_VLayout.setSpacing(5)
        self.left_scrollArea.setWidget(self.left_scrollAreaWidgetContents)
        self.right_tool_layout = QVBoxLayout()
        self.right_tool_layout.setSpacing(5)
        self.right_tool_layout.setContentsMargins(0,0,0,0)
        self.right_scrollArea = QScrollArea(self.page_1)
        self.right_scrollArea.setWidgetResizable(True)
        self.right_scrollArea.setStyleSheet(u"background: transparent;")
        self.right_scrollArea.setFrameShape(QFrame.NoFrame)
        self.right_scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.right_scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.right_scrollAreaWidgetContents = QWidget()
        self.right_scrollArea_VLayout = QVBoxLayout(self.right_scrollAreaWidgetContents)
        self.right_scrollArea_VLayout.setSpacing(5)
        self.right_scrollArea.setWidget(self.right_scrollAreaWidgetContents)
        
        self.page_1_HLayout.addLayout(self.left_tool_layout)
        self.page_1_HLayout.addLayout(self.right_tool_layout)

        self.pages.addWidget(self.page_1)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.page_2_layout = QVBoxLayout(self.page_2)
        self.page_2_layout.setSpacing(5)
        self.page_2_layout.setObjectName(u"page_2_layout")
        self.page_2_layout.setContentsMargins(5, 5, 5, 5)
        self.scroll_area = QScrollArea(self.page_2)
        self.scroll_area.setObjectName(u"scroll_area")
        self.scroll_area.setStyleSheet(u"background: transparent;")
        self.scroll_area.setFrameShape(QFrame.NoFrame)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setWidgetResizable(True)
        self.contents = QWidget()
        self.contents.setObjectName(u"contents")
        self.contents.setGeometry(QRect(0, 0, 840, 580))
        self.contents.setStyleSheet(u"background: transparent;")
        self.verticalLayout = QVBoxLayout(self.contents)
        self.verticalLayout.setSpacing(15)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        
        self.scroll_area.setWidget(self.contents)
        self.page_2_layout.addWidget(self.scroll_area)
        self.pages.addWidget(self.page_2)

        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.page_3.setStyleSheet(u"QFrame {font-size: 8pt;}")
        self.page_3_layout = QVBoxLayout(self.page_3)
        self.page_3_layout.setObjectName(u"page_3_layout")
        self.empty_page_label = QLabel(self.page_3)
        self.empty_page_label.setObjectName(u"empty_page_label")
        self.empty_page_label.setAlignment(Qt.AlignCenter)
        self.page_3_layout.addWidget(self.empty_page_label)
        self.pages.addWidget(self.page_3)

        self.main_pages_layout.addWidget(self.pages)

        MainPages.setWindowTitle(QCoreApplication.translate("MainPages", u"Form", None))
        self.pages.setCurrentIndex(0)
        QMetaObject.connectSlotsByName(MainPages)
