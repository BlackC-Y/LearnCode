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
from MyToolBox.scripts.WeightTool import PointWeightTool_BbBB, WeightCheckTool_BbBB, WeightSL_BbBB, softSelectWeightTool_BbBB, CopyWeightTool_BbBB
from MyToolBox.scripts.MirrorDriverKey import MirrorDriverKey
from MyToolBox.scripts.OtherTools import otherTools, FixError, cRivet
from MyToolBox.scripts.ngSk2Weight import ngSk2Weight_BbBB, ngSmooth_BbBB
from MyToolBox.scripts.ModelTool import SymmetryTool_BbBB, BlendShapeTool_BbBB, ModelUtils_BbBB
from MyToolBox.scripts.Utils import QtStyle


class MayaToolsBox_BbBB():

    def ToolUi(self):
        ToolUi = 'MaYaToolsBox_BbBB'
        if cmds.window(ToolUi, q=1, ex=1):
            cmds.deleteUI(ToolUi)
        cmds.window(ToolUi, t=u'Maya工具箱', rtf=1, mb=1, tlb=1, bgc=QtStyle.backgroundColor)
        cmds.rowLayout(nc=3, rat=([2, 'both', 20], [3, 'both', 5]), h=450, adj=3)

        cmds.columnLayout(cat=('left', 1), rs=70)
        cmds.iconTextRadioCollection()
        cmds.iconTextRadioButton(st='iconAndTextVertical', i1='toolSettings.png', w=60, h=60, l=u'工具列表', sl=1, 
                            onc=lambda *args: switchPage('Tool'))
        cmds.iconTextRadioButton(st='iconAndTextVertical', i1='paintTextureDeformer.png', w=60, h=60, l=u'权重工具',
                            onc=lambda *args: switchPage('WeightTool'))
        cmds.iconTextRadioButton(st='iconAndTextVertical', i1='polyCube.png', w=60, h=60, l=u'模型工具',
                            onc=lambda *args: switchPage('ModelTool'))
        cmds.setParent('..')
        cmds.separator(style='single', hlc=QtStyle.backgroundColor)
        cmds.columnLayout(cat=('both', 2), cw=450)

        #工具列表页
        cmds.rowLayout('%s_ToolPage' %ToolUi, nc=2, cw2=(220, 220), ct2=('both', 'both'), rat=((1, 'both', 2), (2, 'both', 2)))
        cmds.columnLayout(cat=('both', 2), adj=2)
        cmds.text(l=u'————  运行工具  ————', h=52)
        cmds.scrollLayout(cr=1, h=380)
        cmds.columnLayout('%sT_oolList' %ToolUi, cat=('both', 2), rs=5, adj=1)
        _ToolButtonList = [cmds.button(l=u'Rivet', ann=u'Rivet铆钉', h=28, c=lambda *args: cRivet("follicle")),
                           cmds.button(l=u'传递UV', ann=u'传递UV \n选择UV模型+要传递的模型', c=lambda *args: otherTools().TransferUV()),
                           cmds.button(l=u'ngRelax', ann=u'ngRelax权重', c=lambda *args: ngSmooth_BbBB().doIt()),
                           cmds.button(l=u'修型骨骼xu', ann=u'创建修型骨骼(高自定义) \n选择要修型的骨骼', c=lambda *args: otherTools().xiuxingJoint()),
                           cmds.button(l=u'修型骨骼Hang', ann=u'创建修型骨骼(航少版) \n选择要修型的骨骼', c=lambda *args: otherTools().xiuxingJointHang()),
                           cmds.button(l=u'创建Locator', ann=u'在选择物体的位置创建Locator', c=lambda *args: otherTools().createLocator()),
                           cmds.button(l=u'检查模型对称', ann=u'特殊轴向和精度 请找对称工具', c=lambda *args: ModelUtils_BbBB.checkSymmetry()),
                           cmds.button(l=u'从模型提取曲线', ann=u'批量提取曲线 - 仅适用于单片模型', c=lambda *args: otherTools().polytoCurve()),
        ]
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.setParent('..')

        cmds.columnLayout(cat=('both', 2), adj=2)
        cmds.text(l=u'————  界面工具  ————', h=52)
        cmds.scrollLayout(cr=1, h=380)
        cmds.columnLayout('%s_UIToolList' %ToolUi, cat=('both', 2), rs=5, adj=1)
        _ToolButtonList += [cmds.button(l=u'PSD修型', ann=u'基于Maya空间姿势的修型面板', c=lambda *args: PSD_PoseUi().ToolUi()),
                            cmds.button(l=u'曲面毛囊', ann=u'在surface曲面上创建毛囊和骨骼', c=lambda *args: otherTools().createFollicleOnsurface_ToolUi()),
                            cmds.button(l=u'控制器Pro', ann=u'权哥 控制器工具', c=lambda *args: MZ_CtrllTool().ToolUi()),
                            cmds.button(l=u'点权重工具', ann=u'点权重调整', c=lambda *args: PointWeightTool_BbBB().ToolUi()),
                            cmds.button(l=u'ng2权重工具', ann=u'基于ng2的权重计算工具', c=lambda *args: ngSk2Weight_BbBB().ToolUi()),
                            cmds.button(l=u'权重检查工具', ann=u'权重影响值/精度 检查和清理', c=lambda *args: WeightCheckTool_BbBB().ToolUi()),
                            cmds.button(l=u'拷贝权重工具', ann=u'在任意模型、组件间传权重', c=lambda *args: CopyWeightTool_BbBB().ToolUi()),
                            cmds.button(l=u'数据临时储存', ann=u'临时储存 物体、位置、蒙皮骨骼、物体颜色', c=lambda *args: DataSaveUi().ToolUi()),
                            cmds.button(l=u'模型对称工具', ann=u'翻转 镜像模型', c=lambda *args: SymmetryTool_BbBB().ToolUi()),
                            cmds.button(l=u'动力学曲线IK', ann=u'动力学曲线IK', c=lambda *args: cur2IKFX_ToolUi()),
                            cmds.button(l=u'镜像驱动关键帧', ann=u'依次选择 做好的驱动者，做好的被驱动者\n没做的驱动者, 没做的被驱动者', c=lambda *args: MirrorDriverKey().ToolUi()),
                            cmds.button(l=u'解决Maya报错问题', ann=u'解决报错的清单界面', c=lambda *args: FixError().ToolUi()),
        ]
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.setParent('..')

        #权重工具页
        cmds.columnLayout('%s_WeightToolPage' %ToolUi, cat=('both', 2), cw=450, adj=1, rs=5, vis=0)
        cmds.scrollLayout(cr=1, h=380)
        cmds.frameLayout(cll=1, cl=1, mw=5, l=u'拷权重工具')
        CopyWeightTool_BbBB().ToolUi(1)
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.frameLayout(cll=1, cl=1, mw=5, l=u'权重检查工具')
        WeightCheckTool_BbBB().ToolUi(1)
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.frameLayout(cll=1, cl=1, mw=5, l=u'ng2权重工具')
        ngSk2Weight_BbBB().ToolUi(1)
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.rowLayout(nc=2, cw2=(215, 215), ct2=('both', 'both'), rat=((1, 'both', 2), (2, 'both', 2)))
        _ToolButtonList.append(cmds.button(l=u'存权重', c=lambda *args: WeightSL_BbBB().SLcheck('Save')))
        _ToolButtonList.append(cmds.button(l=u'取权重', c=lambda *args: WeightSL_BbBB().SLcheck('Load')))
        cmds.setParent('..')
        _ToolButtonList.append(cmds.button(l=u'点权重工具', ann=u'点权重调整', c=lambda *args: PointWeightTool_BbBB().ToolUi()))
        cmds.setParent('..')
        cmds.setParent('..')

        #模型工具页
        cmds.columnLayout('%s_ModelToolPage' %ToolUi, cat=('both', 2), cw=450, adj=1, rs=5, vis=0)
        cmds.scrollLayout(cr=1, h=380)
        cmds.frameLayout(cll=1, cl=1, mw=5, l=u'模型对称工具')
        SymmetryTool_BbBB().ToolUi(1)
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.frameLayout(cll=1, cl=1, mw=5, l=u'重设Bs形状')
        BlendShapeTool_BbBB.reSetBsTargetUi(1)
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.frameLayout(cll=1, cl=1, mw=5, l=u'提取Bs形状')
        BlendShapeTool_BbBB.ExBsModelToolUi(1)
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.frameLayout(cll=1, cl=1, mw=5, l=u'检查完全相同模型')
        BlendShapeTool_BbBB.checkSameModelToolUi(1)
        cmds.setParent('..')
        cmds.setParent('..')

        cmds.setParent('..')
        cmds.setParent('..')

        for i in _ToolButtonList:
            shiboken2.wrapInstance(int(OmUI.MQtUtil.findControl(i)), QPushButton).setStyleSheet(QtStyle.QButton())

        cmds.showWindow(ToolUi)

        def switchPage(strIn):
            if strIn == "Tool":
                cmds.columnLayout('%s_WeightToolPage' %ToolUi, e=1, vis=0)
                cmds.columnLayout('%s_ModelToolPage' %ToolUi, e=1, vis=0)
                cmds.rowLayout('%s_ToolPage' %ToolUi, e=1, vis=1)
            elif strIn == "WeightTool":
                cmds.columnLayout('%s_ModelToolPage' %ToolUi, e=1, vis=0)
                cmds.rowLayout('%s_ToolPage' %ToolUi, e=1, vis=0)
                cmds.columnLayout('%s_WeightToolPage' %ToolUi, e=1, vis=1)
            elif strIn == "ModelTool":
                cmds.columnLayout('%s_WeightToolPage' %ToolUi, e=1, vis=0)
                cmds.rowLayout('%s_ToolPage' %ToolUi, e=1, vis=0)
                cmds.columnLayout('%s_ModelToolPage' %ToolUi, e=1, vis=1)

            
#MayaToolsBox_BbBB().ToolUi()
