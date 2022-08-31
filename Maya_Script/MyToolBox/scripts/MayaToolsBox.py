# -*- coding: UTF-8 -*-
'''Roadmap:
'''
from maya import cmds, mel
from maya.api import OpenMaya as om
from .CopyWeightTool import *
from .CtrlTool import *
from .cur2IK_FX import *
from .DataSaveUi import *
from .PSDshape import *
from .WeightTool import *
from .MirrorDriverKey import *
from .OtherTools import *
from .ngSk2Weight import *


class MayaToolsBox_BbBB():

    def ToolUi(self):
        self.Info = [
            [u'Rivet', u'Rivet铆钉', 'cRivet("follicle")'],
            [u'传递UV', u'传递UV \n选择UV模型+要传递的模型', 'otherTools().TransferUV()'],
            [u'ngRelax', u'ngRelax权重', 'ngSmooth_BbBB().doIt()'],
            [u'修型骨骼xu', u'创建修型骨骼(高自定义) \n选择要修型的骨骼', 'otherTools().xiuxingJoint()'],
            [u'修型骨骼Hang', u'创建修型骨骼(航少版) \n选择要修型的骨骼', 'otherTools().xiuxingJointHang()'],
            [u'创建Locator', u'在选择物体的位置创建Locator', 'otherTools().createLocator()'],
            [u'从模型提取曲线', u'批量提取曲线 - 仅适用于单片模型', 'otherTools().polytoCurve()'],
            [u'---工具类型分割线---', u'上方是命令式工具 点击运行\n下方是界面工具 点击出界面', 'pass'],
            [u'PSD修型', u'PSD修型', 'PSD_PoseUi().ToolUi()'],
            [u'曲面毛囊', u'在surface曲面上创建毛囊和骨骼', 'otherTools().createFollicleOnsurface_ToolUi()'],
            [u'控制器Pro', u'权哥 控制器生成', 'MZ_CtrllTool().ToolUi()'],
            [u'调权重工具', u'点权重调整 \nSave/Load权重', 'WeightTool_BbBB().ToolUi()'],
            [u'权重检查工具', u'权重影响值/精度 检查和清理', 'WeightCheckTool_BbBB().ToolUi()'],
            [u'拷贝权重工具', u'拷贝权重工具', 'CopyWeightTool().ToolUi()'],
            [u'数据临时储存', u'临时储存物体或位置', 'DataSaveUi().ToolUi()'],
            [u'动力学曲线 IK', u'动力学曲线 IK', 'cur2IKFX_ToolUi()'],
            [u'半自动权重工具', u'基于ng2的权重计算工具', 'ngSk2Weight_BbBB().ToolUi()'],
            [u'镜像驱动关键帧', u'依次选择 做好的驱动者，做好的被驱动者\n没做的驱动者, 没做的被驱动者', 'MirrorDriverKey().ToolUi()'],
            [u'解决Maya报错问题', u'解决报错的清单界面', 'FixError().ToolUi()']
        ]
        #self.Info = sorted(Info, key=lambda item: item[0])

        ToolUi = 'MaYaToolsBox'
        if cmds.window(ToolUi, q=1, ex=1):
            cmds.deleteUI(ToolUi)
        cmds.window(ToolUi, t=ToolUi, rtf=1, mb=1, tlb=1, wh=(230, 500))
        cmds.columnLayout('MainCL', cat=('both', 2), rs=2, cw=220, adj=1)
        cmds.textScrollList('ToolList', ams=0, h=250, sc=lambda *args:self.changeToolInfo(), fn='fixedWidthFont')
        cmds.columnLayout('EditCL', cat=('both', 2), rs=2, cw=220, adj=1)
        cmds.setParent('..')
        cmds.text('detailText', p='EditCL', h=100, fn='fixedWidthFont', l=u'说明:')
        cmds.button(l=u'执行', c=lambda *args: self.doProc(), ann=u'执行选择的工具')
        for i in self.Info:
            cmds.textScrollList('ToolList', e=1, a=i[0])
        cmds.showWindow(ToolUi)

    def changeToolInfo(self):
        slitem = cmds.textScrollList('ToolList', q=1, si=1)[0]
        for i in self.Info:
            if slitem == i[0]:
                cmds.text('detailText', e=1, l=i[1])

    def doProc(self):
        slitem = cmds.textScrollList('ToolList', q=1, si=1)
        if slitem:
            slitem = slitem[0]
        for i in self.Info:
            if slitem == i[0]:
                cmd = i[2]
                exec(cmd)


#MayaToolsBox_BbBB().ToolUi()
