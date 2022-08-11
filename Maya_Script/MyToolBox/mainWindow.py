# -*- coding: UTF-8 -*-
import sys
import os

from .qt_core import *

from .gui.core.functions import Functions
from .gui.core.json_settings import Settings
from .gui.core.json_themes import Themes
from .gui.core.addfont import install_font

from .gui.windows import *
from .gui.widgets import *

# ADJUST QT FONT DPI FOR HIGHT SCALE AN 4K MONITOR
# ///////////////////////////////////////////////////////////////
#os.environ["QT_FONT_DPI"] = "96"
# IF IS 4K MONITOR ENABLE 'os.environ["QT_SCALE_FACTOR"] = "2"'
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

# 安装字体
if Functions.check_font("sarasa-gothic-sc-regular.ttf"):   #查询字体存在
    install_font(Functions.set_font("sarasa-gothic-sc-regular.ttf"), u"更纱黑体 SC")

runInMaya = 1
if runInMaya:
    from maya import OpenMayaUI as OmUI
    from maya.api import OpenMaya as om
    import shiboken2
    from .scripts.CopyWeightTool import *
    from .scripts.CtrlTool import *
    from .scripts.cur2IK_FX import *
    from .scripts.DataSaveUi import *
    from .scripts.PSDshape import *
    from .scripts.Rivet import *
    from .scripts.WeightTool import *
    from .scripts.MirrorDriverKey import *
    from .scripts.OtherTools import *

# MAIN WINDOW
class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__(shiboken2.wrapInstance(int(OmUI.MQtUtil.mainWindow()), QMainWindow))
        #super().__init__()

        # SETUP MAIN WINDOw
        # Load widgets from "uis\ui_main.py"
        self.ui = UI_MainWindow()
        self.ui.setup_ui(self)


        settings = Settings()
        self.settings = settings.items

        themes = Themes()
        self.themes = themes.items

        # SETUP MAIN WINDOW
        self.hide_grips = True # Show/Hide resize grips
        SetupMainWindow.setup_gui(self)
        
        self.myWidget()
        # SHOW MAIN WINDOW
        self.show()

    # LEFT MENU BTN IS CLICKED
    # Run function when btn is clicked
    # Check funtion by object name / btn_id
    def btn_clicked(self):
        # GET BT CLICKED
        btn = SetupMainWindow.setup_btns(self)

        # Remove Selection If Clicked By "btn_close_left_column"
        if btn.objectName() != "btn_settings":
            self.ui.left_menu.deselect_all_tab()

        # Get Title Bar Btn And Reset Active         
        #top_settings = MainFunctions.get_title_bar_btn(self, "btn_top_settings")
        #top_settings.set_active(False)

        # LEFT MENU
        if btn.objectName() == "btn_home":
            self.ui.left_menu.select_only_one(btn.objectName())   # Select Menu
            MainFunctions.set_page(self, self.ui.load_pages.page_1)

        if btn.objectName() == "btn_widgets":
            self.ui.left_menu.select_only_one(btn.objectName())
            MainFunctions.set_page(self, self.ui.load_pages.page_2)

        if btn.objectName() == "btn_add_user":
            self.ui.left_menu.select_only_one(btn.objectName())   # Select Menu
            MainFunctions.set_page(self, self.ui.load_pages.page_3)

        # BOTTOM INFORMATION
        if btn.objectName() == "btn_info":
            # CHECK IF LEFT COLUMN IS VISIBLE
            if not MainFunctions.left_column_is_visible(self):
                self.ui.left_menu.select_only_one_tab(btn.objectName())

                # Show / Hide
                MainFunctions.toggle_left_column(self)
                self.ui.left_menu.select_only_one_tab(btn.objectName())
            else:
                if btn.objectName() == "btn_close_left_column":
                    self.ui.left_menu.deselect_all_tab()
                    # Show / Hide
                    MainFunctions.toggle_left_column(self)
                
                self.ui.left_menu.select_only_one_tab(btn.objectName())

            # Change Left Column Menu
            if btn.objectName() != "btn_close_left_column":
                MainFunctions.set_left_column_menu(
                    self, 
                    menu = self.ui.left_column.menus.menu_2,
                    title = "Info tab",
                    icon_path = Functions.set_svg_icon("icon_info.svg")
                )

        # SETTINGS LEFT
        if btn.objectName() == "btn_settings" or btn.objectName() == "btn_close_left_column":
            # CHECK IF LEFT COLUMN IS VISIBLE
            if not MainFunctions.left_column_is_visible(self):
                # Show / Hide
                MainFunctions.toggle_left_column(self)
                self.ui.left_menu.select_only_one_tab(btn.objectName())
            else:
                if btn.objectName() == "btn_close_left_column":
                    self.ui.left_menu.deselect_all_tab()
                    # Show / Hide
                    MainFunctions.toggle_left_column(self)
                self.ui.left_menu.select_only_one_tab(btn.objectName())

            # Change Left Column Menu
            if btn.objectName() != "btn_close_left_column":
                MainFunctions.set_left_column_menu(
                    self, 
                    menu = self.ui.left_column.menus.menu_1,
                    title = "Settings Left Column",
                    icon_path = Functions.set_svg_icon("icon_settings.svg")
                )
        
        # TITLE BAR MENU
    
        
        # SETTINGS TITLE BAR
        if btn.objectName() == "btn_top_settings":
            # Toogle Active
            if not MainFunctions.right_column_is_visible(self):
                btn.set_active(True)

                # Show / Hide
                MainFunctions.toggle_right_column(self)
            else:
                btn.set_active(False)

                # Show / Hide
                MainFunctions.toggle_right_column(self)

            # Get Left Menu Btn            
            top_settings = MainFunctions.get_left_menu_btn(self, "btn_settings")
            top_settings.set_active_tab(False)            

        # DEBUG
        #print(f"Button {btn.objectName()}, clicked!")

    # LEFT MENU BTN IS RELEASED
    # Run function when btn is released
    # Check funtion by object name / btn_id

    def btn_released(self):
        # GET BT CLICKED
        btn = SetupMainWindow.setup_btns(self)

        # DEBUG
        #print(f"Button {btn.objectName()}, released!")

    # RESIZE EVENT
    def resizeEvent(self, event):
        SetupMainWindow.resize_grips(self)

    # MOUSE CLICK EVENTS
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPos()

    def myWidget(self):
        self.leftTool_lableLine = cusLableLine('HC', self.themes["app_color"]["text_foreground"], u'运行工具', 35)
        self.toolButton_L1 = cusPushButton(
            text=u"创建Locator",
            radius=4,
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"],
            parent = self,
            app_parent = self.ui.central_widget,
            font = self.settings["font_family"],
            minHeight=28,
            tooltip_text = u'在选择物体的位置创建Locator'
        )
        self.toolButton_L2 = cusPushButton(
            text=u"从模型提取曲线",
            radius=4,
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"],
            parent = self,
            app_parent = self.ui.central_widget,
            font = self.settings["font_family"],
            minHeight=28,
            tooltip_text = u'选择模型 批量提取曲线(仅适用于单片模型)'
        )
        self.toolButton_L3 = cusPushButton(
            text=u"修型骨骼Hang",
            radius=4,
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"],
            parent = self,
            app_parent = self.ui.central_widget,
            font = self.settings["font_family"],
            minHeight=28,
            tooltip_text = u'选择要修型的骨骼(航少版)'
        )
        self.toolButton_L4 = cusPushButton(
            text=u"修型骨骼Xu",
            radius=4,
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"],
            parent = self,
            app_parent = self.ui.central_widget,
            font = self.settings["font_family"],
            minHeight=28,
            tooltip_text = u'选择要修型的骨骼(自定义)'
        )
        self.toolButton_L5 = cusPushButton(
            text=u"传递UV",
            radius=4,
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"],
            parent = self,
            app_parent = self.ui.central_widget,
            font = self.settings["font_family"],
            minHeight=28,
            tooltip_text = u'选择UV模型 + 要传递的模型'
        )
        self.toolButton_L6 = cusPushButton(
            text=u"ngRelax",
            radius=4,
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"],
            parent = self,
            app_parent = self.ui.central_widget,
            font = self.settings["font_family"],
            minHeight=28,
            tooltip_text = u'ngRelax'
        )
        self.toolButton_L7 = cusPushButton(
            text=u"Rivet",
            radius=4,
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"],
            parent = self,
            app_parent = self.ui.central_widget,
            font = self.settings["font_family"],
            minHeight=28,
            tooltip_text = u'Rivet铆钉'
        )
        self.toolButton_L8 = cusPushButton(
            text=u"解决look爆红",
            radius=4,
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"],
            parent = self,
            app_parent = self.ui.central_widget,
            font = self.settings["font_family"],
            minHeight=28,
            tooltip_text = u'解决在大纲选择物体时Maya爆红"look"的问题'
        )
        
        self.toolButton_L1.clicked.connect(lambda *args: otherTools().createLocator())
        self.toolButton_L2.clicked.connect(lambda *args: otherTools().polytoCurve())
        self.toolButton_L3.clicked.connect(lambda *args: otherTools().xiuxingJointHang())
        self.toolButton_L4.clicked.connect(lambda *args: otherTools().xiuxingJoin())
        self.toolButton_L5.clicked.connect(lambda *args: otherTools().TransferUV())
        self.toolButton_L6.clicked.connect(lambda *args: otherTools().doPlugin("ngRelax"))
        self.toolButton_L7.clicked.connect(lambda *args: cRivet("follicle"))
        self.toolButton_L8.clicked.connect(lambda *args: otherTools().FixRedlook())
        
        self.ui.load_pages.left_tool_layout.addWidget(self.leftTool_lableLine)
        self.ui.load_pages.left_tool_layout.addWidget(self.toolButton_L7)
        self.ui.load_pages.left_tool_layout.addWidget(self.toolButton_L5)
        self.ui.load_pages.left_tool_layout.addWidget(self.toolButton_L6)
        self.ui.load_pages.left_tool_layout.addWidget(self.toolButton_L4)
        self.ui.load_pages.left_tool_layout.addWidget(self.toolButton_L3)
        self.ui.load_pages.left_tool_layout.addWidget(self.toolButton_L1)
        self.ui.load_pages.left_tool_layout.addWidget(self.toolButton_L8)
        self.ui.load_pages.left_tool_layout.addWidget(self.toolButton_L2)
        self.left_VSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.ui.load_pages.left_tool_layout.addItem(self.left_VSpacer)

        # Right
        self.rightTool_lableLine = cusLableLine('HC', self.themes["app_color"]["text_foreground"], u'界面工具', 35)
        self.toolButton_R1 = cusPushButton(
            text=u"曲面毛囊",
            radius=4,
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"],
            parent = self,
            app_parent = self.ui.central_widget,
            font = self.settings["font_family"],
            minHeight=28,
            tooltip_text = u'在surface曲面上创建毛囊和骨骼'
        )
        self.toolButton_R2 = cusPushButton(
            text=u"拷权重工具",
            radius=4,
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"],
            parent = self,
            app_parent = self.ui.central_widget,
            font = self.settings["font_family"],
            minHeight=28,
            tooltip_text = u'在任意模型、组件间传权重'
        )
        self.toolButton_R3 = cusPushButton(
            text=u"动力学曲线 IK",
            radius=4,
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"],
            parent = self,
            app_parent = self.ui.central_widget,
            font = self.settings["font_family"],
            minHeight=28,
            tooltip_text = u'动力学曲线 IK'
        )
        self.toolButton_R4 = cusPushButton(
            text=u"数据临时储存",
            radius=4,
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"],
            parent = self,
            app_parent = self.ui.central_widget,
            font = self.settings["font_family"],
            minHeight=28,
            tooltip_text = u'临时储存 物体、位置、蒙皮骨骼、物体颜色'
        )
        self.toolButton_R5 = cusPushButton(
            text=u"PSD修型",
            radius=4,
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"],
            parent = self,
            app_parent = self.ui.central_widget,
            font = self.settings["font_family"],
            minHeight=28,
            tooltip_text = u'基于Maya Pose功能的修型'
        )
        self.toolButton_R6 = cusPushButton(
            text=u"控制器Pro",
            radius=4,
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"],
            parent = self,
            app_parent = self.ui.central_widget,
            font = self.settings["font_family"],
            minHeight=28,
            tooltip_text = u'控制器工具'
        )
        self.toolButton_R7 = cusPushButton(
            text=u"镜像驱动关键帧",
            radius=4,
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"],
            parent = self,
            app_parent = self.ui.central_widget,
            font = self.settings["font_family"],
            minHeight=28,
            tooltip_text = u'依次选择 做好的驱动者, 做好的被驱动者\n没做的驱动者, 没做的被驱动者'
        )
        self.toolButton_R8 = cusPushButton(
            text=u"调权重工具",
            radius=4,
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"],
            parent = self,
            app_parent = self.ui.central_widget,
            font = self.settings["font_family"],
            minHeight=28,
            tooltip_text = u'点权重调整 - Save/Load权重'
        )
        self.toolButton_R9 = cusPushButton(
            text=u"权重检查工具",
            radius=4,
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"],
            parent = self,
            app_parent = self.ui.central_widget,
            font = self.settings["font_family"],
            minHeight=28,
            tooltip_text = u'权重影响值/精度 检查和清理'
        )
        self.toolButton_R1.clicked.connect(lambda *args: otherTools().createFollicleOnsurface_ToolUi())
        self.toolButton_R2.clicked.connect(lambda *args: CopyWeightTool().ToolUi())
        self.toolButton_R3.clicked.connect(lambda *args: cur2IKFX_Tool())
        self.toolButton_R4.clicked.connect(lambda *args: DataSaveUi().ToolUi())
        self.toolButton_R5.clicked.connect(lambda *args: PSD_PoseUi().ToolUi())
        self.toolButton_R6.clicked.connect(lambda *args: MZ_CtrllTool().ToolUi())
        self.toolButton_R7.clicked.connect(lambda *args: MirrorDriverKey().ToolUi())
        self.toolButton_R8.clicked.connect(lambda *args: WeightTool_BbBB().ToolUi())
        self.toolButton_R9.clicked.connect(lambda *args: WeightCheckTool_BbBB().ToolUi())

        self.ui.load_pages.right_tool_layout.addWidget(self.rightTool_lableLine)
        self.ui.load_pages.right_tool_layout.addWidget(self.toolButton_R5)
        self.ui.load_pages.right_tool_layout.addWidget(self.toolButton_R1)
        self.ui.load_pages.right_tool_layout.addWidget(self.toolButton_R6)
        self.ui.load_pages.right_tool_layout.addWidget(self.toolButton_R8)
        self.ui.load_pages.right_tool_layout.addWidget(self.toolButton_R9)
        self.ui.load_pages.right_tool_layout.addWidget(self.toolButton_R2)
        self.ui.load_pages.right_tool_layout.addWidget(self.toolButton_R4)
        self.ui.load_pages.right_tool_layout.addWidget(self.toolButton_R3)
        self.ui.load_pages.right_tool_layout.addWidget(self.toolButton_R7)
        self.right_VSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.ui.load_pages.right_tool_layout.addItem(self.right_VSpacer)
"""
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    window = MainWindow()
    sys.exit(app.exec_())
"""