# -*- coding: UTF-8 -*-
'''Roadmap:
'''
from maya import cmds, mel
from maya import OpenMayaUI as OmUI
from maya.api import OpenMaya as om
#from PySide2.QtCore import Qt
#from PySide2.QtGui import QPalette
from PySide2.QtWidgets import QPushButton
import shiboken2

from MyToolBox.scripts.CtrlTool import MZ_CtrllTool
from MyToolBox.scripts.cur2IK_FX import cur2IKFX_ToolUi
from MyToolBox.scripts.DataSaveUi import DataSaveUi
from MyToolBox.scripts.PSDshape import PSD_PoseUi
from MyToolBox.scripts.WeightTool import PointWeightTool_BbBB, WeightCheckTool_BbBB, WeightSL_BbBB, softSelectWeightTool_BbBB, CopyWeightTool_BbBB, WeightUtils_BbBB
from MyToolBox.scripts.MirrorDriverKey import MirrorDriverKey
from MyToolBox.scripts.OtherTools import otherTools
from MyToolBox.scripts.ngSk2Weight import ngSk2Weight_BbBB, ngSmooth_BbBB, ngUtils_BbBB
from MyToolBox.scripts.ModelTool import SymmetryTool_BbBB, BlendShapeTool_BbBB, ModelUtils_BbBB
from MyToolBox.scripts.Utils import QtStyle, Functions


class MayaToolsBox_BbBB():

    def ToolUi(self):
        ToolUi = 'MaYaToolsBox_BbBB'
        if cmds.window(ToolUi, q=1, ex=1):
            cmds.deleteUI(ToolUi)

        def getTheme():
            theme = Functions.readSetting('Global', 'theme')
            _theme = [0 for i in range(3)]
            if theme == 'black':
                _theme[0] = 1
            elif theme == "pink":
                _theme[1] = 1
            elif theme == 'eyegreen':
                _theme[2] = 1
            return _theme
        _theme = getTheme()
        
        cmds.window(ToolUi, t=u'Maya工具箱', rtf=1, mb=1, mxb=0, bgc=QtStyle.backgroundMayaColor())
        cmds.rowLayout(nc=2, rat=([1, 'both', 0], [2, 'both', 5]), h=460, adj=3)
        fn = 'fixedWidthFont'
        cmds.columnLayout(cat=('left', 5), cw=80, w=78, rs=60, bgc=QtStyle.accentMayaColor())
        cmds.text(l=u'菜单', al='center', h=20, w=70, fn=fn)
        cmds.popupMenu(button=1)
        cmds.menuItem(subMenu=1, label=u'主题')
        cmds.radioMenuItemCollection()
        cmds.menuItem(rb=_theme[0], label=u'默认黑', c=lambda *args: Functions.editSetting("Global", "theme", "black"))
        cmds.menuItem(rb=_theme[1], label=u'猛男粉', c=lambda *args: Functions.editSetting("Global", "theme", "pink"))
        cmds.menuItem(rb=_theme[2], label=u'护眼绿', c=lambda *args: Functions.editSetting("Global", "theme", "eyegreen"))
        #cmds.menuItem(l=u'', c=lambda *args: '')
        cmds.iconTextRadioCollection()
        cmds.iconTextRadioButton(st='iconAndTextVertical', i1='toolSettings.png', w=75, h=70, l=u'工具列表', sl=1, fn=fn, hlc=QtStyle.backgroundMayaColor(), 
                            onc=lambda *args: switchPage('Tool'))
        cmds.iconTextRadioButton(st='iconAndTextVertical', i1='paintTextureDeformer.png', w=75, h=70, l=u'权重工具', fn=fn, hlc=QtStyle.backgroundMayaColor(),
                            onc=lambda *args: switchPage('WeightTool'))
        cmds.iconTextRadioButton(st='iconAndTextVertical', i1='polyCube.png', w=75, h=70, l=u'模型工具', fn=fn, hlc=QtStyle.backgroundMayaColor(),
                            onc=lambda *args: switchPage('ModelTool'))
        cmds.setParent('..')
        #cmds.separator(style='single', hlc=QtStyle.backgroundColor())
        cmds.columnLayout(cat=('both', 2), cw=450)

        #工具列表页
        cmds.rowLayout('%s_ToolPage' %ToolUi, nc=2, cw2=(220, 220), ct2=('both', 'both'), rat=((1, 'both', 2), (2, 'both', 2)))
        cmds.columnLayout(cat=('both', 2), adj=2)
        cmds.text(l=u'————  运行工具  ————', fn=fn, h=52)
        cmds.scrollLayout(cr=1, h=380)
        cmds.columnLayout('%sT_oolList' %ToolUi, cat=('both', 2), rs=4, adj=1)
        _ToolButtonList = [cmds.button(l=u'Rivet', ann=u'Rivet铆钉', c=lambda *args: otherTools.cRivet("follicle")),
                           cmds.button(l=u'传递UV', ann=u'传递UV \n选择UV模型+要传递的模型', c=lambda *args: otherTools.TransferUV()),
                           cmds.button(l=u'修型反算', ann=u'先选源模型，再选修好型的 \n源模型应该在当时提取修型的位置', c=lambda *args: ModelUtils_BbBB.invertShape_Bs()),
                           cmds.button(l=u'修型骨骼xu', ann=u'创建修型骨骼(高自定义) \n选择要修型的骨骼', c=lambda *args: otherTools.xiuxingJoint()),
                           cmds.button(l=u'修型骨骼Hang', ann=u'创建修型骨骼(航少版) \n选择要修型的骨骼', c=lambda *args: otherTools.xiuxingJointHang()),
                           cmds.button(l=u'移除未知插件', ann=u'加快文件打开速度', c=lambda *args: otherTools.removeUnknownPlugin()),
                           cmds.button(l=u'创建Locator', ann=u'在选择物体的位置创建Locator', c=lambda *args: otherTools.createLocator()),
                           cmds.button(l=u'检查模型对称', ann=u'特殊轴向和精度 请找对称工具', c=lambda *args: ModelUtils_BbBB.checkSymmetry()),
                           cmds.button(l=u'从模型提取曲线', ann=u'批量提取曲线 - 仅适用于单片模型', c=lambda *args: otherTools.polytoCurve()),
                           cmds.button(l=u'重置骨骼蒙皮位置', ann=u'当骨骼出现位置变化后，可以将当前位置设为蒙皮位置', c=lambda *args: WeightUtils_BbBB.resetSkinPose()),
                           cmds.button(l=u'选择的物体 被最后选的物体约束', ann=u''),
        ]
        cmds.popupMenu(button=1)
        cmds.menuItem(l=u'父子', c=lambda *args: otherTools.constraintFromLast(0))
        cmds.menuItem(l=u'点', c=lambda *args: otherTools.constraintFromLast(1))
        cmds.menuItem(l=u'旋转', c=lambda *args: otherTools.constraintFromLast(2))
        cmds.menuItem(l=u'缩放', c=lambda *args: otherTools.constraintFromLast(3))
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.setParent('..')

        cmds.columnLayout(cat=('both', 2), adj=2)
        cmds.text(l=u'————  界面工具  ————', fn=fn, h=52)
        cmds.scrollLayout(cr=1, h=380)
        cmds.columnLayout('%s_UIToolList' %ToolUi, cat=('both', 2), rs=4, adj=1)
        _ToolButtonList += [cmds.button(l=u'PSD修型', ann=u'基于Maya空间姿势的修型面板', c=lambda *args: PSD_PoseUi().ToolUi()),
                            cmds.button(l=u'曲面毛囊', ann=u'在surface曲面上创建毛囊和骨骼', c=lambda *args: otherTools.createFollicleOnsurface_ToolUi()),
                            cmds.button(l=u'控制器Pro', ann=u'权哥 控制器工具', c=lambda *args: MZ_CtrllTool().ToolUi()),
                            cmds.button(l=u'数据临时储存', ann=u'临时储存 物体、位置、蒙皮骨骼、物体颜色', c=lambda *args: DataSaveUi().ToolUi()),
                            cmds.button(l=u'动力学曲线IK', ann=u'动力学曲线IK', c=lambda *args: cur2IKFX_ToolUi()),
                            cmds.button(l=u'IKFK无缝切换', ann=u'IKFK无缝切换', c=lambda *args: otherTools.IkFkSeamlessSwitch_ToolUi()),
                            cmds.button(l=u'AdvBuildPose', ann=u'管理Adv的BuildPose功能', c=lambda *args: 'print(u"敬请期待")'),
                            cmds.button(l=u'镜像驱动关键帧', ann=u'依次选择 做好的驱动者，做好的被驱动者\n没做的驱动者, 没做的被驱动者', c=lambda *args: MirrorDriverKey().ToolUi()),
                            cmds.button(l=u'解决Maya错误问题', ann=u'解决错误的清单', c=lambda *args: otherTools.FixError_ToolUi()),         
        ]
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.setParent('..')

        #权重工具页
        cmds.scrollLayout('%s_WeightToolPage' %ToolUi, cr=1, h=380, vis=0)
        cmds.columnLayout(cat=('both', 2), cw=450, adj=1, rs=3)
        cmds.frameLayout(cll=1, cl=1, mw=5, fn=fn, l=u'拷权重工具', bgc=QtStyle.accentMayaColor())
        CopyWeightTool_BbBB().ToolUi(1)
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.frameLayout(cll=1, cl=1, mw=5, fn=fn, l=u'权重检查工具', bgc=QtStyle.accentMayaColor())
        WeightCheckTool_BbBB().ToolUi(1)
        cmds.setParent('..')
        cmds.setParent('..')
        if ngUtils_BbBB.pluginCheck():
            cmds.frameLayout(cll=1, cl=1, mw=5, fn=fn, l=u'ng2权重工具', bgc=QtStyle.accentMayaColor())
            ngSk2Weight_BbBB().ToolUi(1)
            cmds.setParent('..')
            cmds.setParent('..')
        _ToolButtonList.append(cmds.button(l=u'点权重工具', ann=u'点权重调整', c=lambda *args: PointWeightTool_BbBB().ToolUi()))
        _ToolButtonList.append(cmds.button(l=u'软选择权重工具', ann=u'通过软选择创建\调整权重', c=lambda *args: softSelectWeightTool_BbBB().ToolUi()))
        _ToolButtonList.append(cmds.button(l=u'强度1                                              Ng-Relax权重                                              30强度', 
                                           ann=u'鼠标中键点击按钮 从左到右强度不同', dgc=lambda *args: ngSmooth_BbBB().doIt(int(args[1]/14.5)+1), c=lambda *args: ngSmooth_BbBB().doIt()))
        cmds.rowLayout(nc=2, cw2=(215, 215), ct2=('both', 'both'), rat=((1, 'both', 2), (2, 'both', 2)))
        _ToolButtonList.append(cmds.button(l=u'存权重', c=lambda *args: WeightSL_BbBB().SLcheck('Save')))
        _ToolButtonList.append(cmds.button(l=u'取权重', c=lambda *args: WeightSL_BbBB().SLcheck('Load')))
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.setParent('..')
        
        #模型工具页
        cmds.scrollLayout('%s_ModelToolPage' %ToolUi, cr=1, h=380, vis=0)
        cmds.columnLayout(cat=('both', 2), cw=450, adj=1, rs=3)
        cmds.frameLayout(cll=1, cl=1, mw=5, fn=fn, l=u'模型对称工具', bgc=QtStyle.accentMayaColor())
        SymmetryTool_BbBB().ToolUi(1)
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.frameLayout(cll=1, cl=1, mw=5, fn=fn, l=u'重设_重建Bs目标', bgc=QtStyle.accentMayaColor())
        BlendShapeTool_BbBB.reBsTargetUi(1)
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.frameLayout(cll=1, cl=1, mw=5, fn=fn, l=u'提取Bs模型', bgc=QtStyle.accentMayaColor())
        BlendShapeTool_BbBB.ExBsModelToolUi(1)
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.frameLayout(cll=1, cl=1, mw=5, fn=fn, l=u'连接Bs控制', bgc=QtStyle.accentMayaColor())
        BlendShapeTool_BbBB.connectBSToolUi(1)
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.frameLayout(cll=1, cl=1, mw=5, fn=fn, l=u'检查完全相同模型', bgc=QtStyle.accentMayaColor())
        BlendShapeTool_BbBB.checkSameModelToolUi(1)
        cmds.setParent('..')
        cmds.setParent('..')

        cmds.setParent('..')
        cmds.setParent('..')

        for i in _ToolButtonList:
            shiboken2.wrapInstance(int(OmUI.MQtUtil.findControl(i)), QPushButton).setStyleSheet(QtStyle.QButtonStyle())

        cmds.showWindow(ToolUi)

        def switchPage(strIn):
            if strIn == "Tool":
                cmds.scrollLayout('%s_WeightToolPage' %ToolUi, e=1, vis=0)
                cmds.scrollLayout('%s_ModelToolPage' %ToolUi, e=1, vis=0)
                cmds.rowLayout('%s_ToolPage' %ToolUi, e=1, vis=1)
            elif strIn == "WeightTool":
                cmds.scrollLayout('%s_ModelToolPage' %ToolUi, e=1, vis=0)
                cmds.rowLayout('%s_ToolPage' %ToolUi, e=1, vis=0)
                cmds.scrollLayout('%s_WeightToolPage' %ToolUi, e=1, vis=1)
            elif strIn == "ModelTool":
                cmds.scrollLayout('%s_WeightToolPage' %ToolUi, e=1, vis=0)
                cmds.rowLayout('%s_ToolPage' %ToolUi, e=1, vis=0)
                cmds.scrollLayout('%s_ModelToolPage' %ToolUi, e=1, vis=1)


#MayaToolsBox_BbBB().ToolUi()
