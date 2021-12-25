# -*- coding: UTF-8 -*-
from maya import cmds, mel


class MirrorDriverKey():

    #Verision = 1.0
    def Ui(self):
        ToolUi = 'MirrorDriverKey'
        if cmds.window(ToolUi, q=1, ex=1):
            cmds.deleteUI(ToolUi)
        cmds.window(ToolUi, t=ToolUi, rtf=1, mb=1, mxb=0, wh=(300, 85))
        cmds.columnLayout(cat=('both', 2), rs=2, cw=430, adj=0)
        def _selectText(name=''):
            sl = cmds.ls(sl=1)
            if not name:
                if len(sl) == 4:
                    cmds.textFieldGrp('sourceDriverText', e=1, tx=sl[0])
                    cmds.textFieldGrp('sourceDrivenText', e=1, tx=sl[1])
                    cmds.textFieldGrp('targeDriverText', e=1, tx=sl[2])
                    cmds.textFieldGrp('targeDrivenText', e=1, tx=sl[3])
                else:
                    print(u'当前选择了%s个物体' %len(sl))
            else:
                if len(sl) == 1:
                    cmds.textFieldButtonGrp(name, e=1, tx=sl[0])
                else:
                    print(u'当前选择了%s个物体' %len(sl))

        cmds.columnLayout('singleSelectCL', cat=('both', 2), rs=2, cw=450, adj=0, vis=0)
        cmds.rowLayout(nc=2)
        cmds.textFieldButtonGrp('sourceDriverTextB', l=u'源驱动者', bl='Select', ed=0, cw3=[55, 100, 30], bc=lambda *args: _selectText('sourceDriverTextB'))
        cmds.textFieldButtonGrp('sourceDrivenTextB', l=u'源被驱动者', bl='Select', ed=0, cw3=[65, 100, 30], bc=lambda *args: _selectText('sourceDrivenTextB'))
        cmds.setParent('..')
        cmds.rowLayout(nc=2)
        cmds.textFieldButtonGrp('targeDriverTextB', l=u'目标驱动者', bl='Select', ed=0, cw3=[55, 100, 30], bc=lambda *args: _selectText('targeDriverTextB'))
        cmds.textFieldButtonGrp('targeDrivenTextB', l=u'目标被驱动者', bl='Select', ed=0, cw3=[65, 100, 30], bc=lambda *args: _selectText('targeDrivenTextB'))
        cmds.setParent('..')
        cmds.setParent('..')
        
        cmds.rowLayout('MultipleSelectRL', nc=2, vis=1)
        cmds.columnLayout(cat=('both', 2), rs=2, cw=372, adj=0)
        cmds.rowLayout(nc=2)
        cmds.textFieldGrp('sourceDriverText', l=u'源驱动者', ed=0, cw2=[55, 120])
        cmds.textFieldGrp('sourceDrivenText', l=u'源被驱动者', ed=0, cw2=[65, 120])
        cmds.setParent('..')
        cmds.rowLayout(nc=2)
        cmds.textFieldGrp('targeDriverText', l=u'目标驱动者', ed=0, cw2=[55, 120])
        cmds.textFieldGrp('targeDrivenText', l=u'目标被驱动者', ed=0, cw2=[65, 120])
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.button(l='Select', w=45, h=50, c=lambda *args: _selectText())
        cmds.setParent('..')

        cmds.separator(height=5, style='in')
        cmds.popupMenu()
        cmds.menuItem(l=u'切换布局', c=lambda *args: self.changeLayout())
        cmds.rowLayout(nc=2)
        cmds.radioButtonGrp('tDriverMirrorRadioB', l=u'驱动者位移:', la2=[u'正常', u'镜像'], nrb=2, cw3=[70, 45, 45], sl=2)
        cmds.radioButtonGrp('rDriverMirrorRadioB', l=u'驱动者旋转:', la2=[u'正常', u'镜像'], nrb=2, cw3=[70, 45, 45], sl=1)
        cmds.setParent('..')
        cmds.rowLayout(nc=2)
        cmds.radioButtonGrp('tDrivenMirrorRadioB', l=u'被驱动者位移:', la2=[u'正常', u'镜像'], nrb=2, cw3=[70, 45, 45], sl=2)
        cmds.radioButtonGrp('rDrivenMirrorRadioB', l=u'被驱动者旋转:', la2=[u'正常', u'镜像'], nrb=2, cw3=[70, 45, 45], sl=1)
        cmds.setParent('..')

        cmds.button(l='Run', w=255, c=lambda *args: self.runProc())
        cmds.showWindow(ToolUi)

    def changeLayout(self):
        if cmds.columnLayout('singleSelectCL', q=1, vis=1):
            cmds.columnLayout('singleSelectCL', e=1, vis=0)
            cmds.rowLayout('MultipleSelectRL', e=1, vis=1)
        else:
            cmds.rowLayout('MultipleSelectRL', e=1, vis=0)
            cmds.columnLayout('singleSelectCL', e=1, vis=1)
            
    def runProc(self):
        if cmds.columnLayout('singleSelectCL', q=1, vis=1):
            sDriver = cmds.textFieldButtonGrp('sourceDriverTextB', q=1, tx=1)
            sDriven = cmds.textFieldButtonGrp('sourceDrivenTextB', q=1, tx=1)
            tDriver = cmds.textFieldButtonGrp('targeDriverTextB', q=1, tx=1)
            tDriven = cmds.textFieldButtonGrp('targeDrivenTextB', q=1, tx=1)
        else:
            sDriver = cmds.textFieldGrp('sourceDriverText', q=1, tx=1)
            sDriven = cmds.textFieldGrp('sourceDrivenText', q=1, tx=1)
            tDriver = cmds.textFieldGrp('targeDriverText', q=1, tx=1)
            tDriven = cmds.textFieldGrp('targeDrivenText', q=1, tx=1)
        if not sDriver or not sDriven or not tDriver or not tDriven:
            return
        tDriverMirror = 1 if cmds.radioButtonGrp('tDriverMirrorRadioB', q=1, sl=1) == 1 else -1
        rDriverMirror = 1 if cmds.radioButtonGrp('rDriverMirrorRadioB', q=1, sl=1) == 1 else -1
        tDrivenMirror = 1 if cmds.radioButtonGrp('tDrivenMirrorRadioB', q=1, sl=1) == 1 else -1
        rDrivenMirror = 1 if cmds.radioButtonGrp('rDrivenMirrorRadioB', q=1, sl=1) == 1 else -1

        drivenAttr = cmds.setDrivenKeyframe(sDriven, q=1, dn=1)   #全部受驱动属性
        for i in drivenAttr:
            driverAttr = cmds.setDrivenKeyframe(i, q=1, cd=1)
            time = cmds.keyframe(i, q=1, fc=1)
            value = cmds.keyframe(i, q=1, vc=1)
            if driverAttr and time:
                splitDriver = driverAttr[0].split('.', 1)
                if splitDriver[0] == sDriver:
                    splitDriven = i.split('.', 1)
                    
                    mirrorT = mirrorV = 1
                    if 'translate' in splitDriver[1]:   #驱动者镜像
                        mirrorT = tDriverMirror
                    elif 'rotate' in splitDriver[1]:
                        mirrorT = rDriverMirror

                    if 'translate' in splitDriven[1]:   #被驱动者镜像
                        mirrorV = tDrivenMirror
                    elif 'rotate' in splitDriven[1]:
                        mirrorV = rDrivenMirror

                    newtDriver = '%s.%s' %(tDriver, splitDriver[1])
                    newtDriven = '%s.%s' %(tDriven, splitDriven[1])
                    for i in range(len(time)):
                        cmds.setDrivenKeyframe(newtDriven, cd=newtDriver, dv=time[i] * mirrorT, v=value[i]* mirrorV)

        """
        acUL = cmds.listConnections(sDriven, t='animCurveUL')
        if acUL:
            for i in range(len(acUL)):
                topNode = cmds.listConnections('%s.input' %acUL[i], c=1)
                if topNode and cmds.nodeType(topNode[1]) == 'unitConversion':
                    topNode = cmds.listConnections('%s.input' %topNode[0], c=1)
        acUA = cmds.listConnections(sDriven, t='animCurveUA')
        cmds.listConnections('locator1_rotateY', c=1, t='animCurveUA')
        """

#MirrorDriverKey().Ui()