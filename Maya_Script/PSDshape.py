# -*- coding: UTF-8 -*-
from maya import cmds, mel
from maya.api import OpenMaya as om


class PSD_PoseUi_KitKat():

    __Verision = 0.8

    def ToolUi(self):
        ToolUi = 'PSD_Pose_KitKat'
        if cmds.window(ToolUi, q=1, ex=1):
            cmds.deleteUI(ToolUi)
        cmds.window(ToolUi, t='PSD_Pose', rtf=1, mb=1, mxb=0, wh=(250, 250))
        cmds.menu(l='Axis')
        cmds.radioMenuItemCollection()
        self.AxisItem = [
            cmds.menuItem(l='X', rb=1),
            cmds.menuItem(l='Y', rb=0),
            cmds.menuItem(l='Z', rb=0),
        ]
        cmds.menu(l='Setting')
        cmds.menuItem(l='MirrorName', c=lambda *args: cmds.columnLayout('MirrorName_Ly_KitKat', e=1, vis=1))
        cmds.menu(l='Help')
        cmds.menuItem(l='Help Doc', c=lambda *args: self.helpDoc())
        cmds.menu(l='             ', en=0)
        cmds.menu('loadobj_KitKat', l='| Load Object |')
        def _loadObj():
            lslist = cmds.ls(sl=1, o=1, typ='transform')
            if lslist:
                if cmds.listRelatives(lslist[0], s=1, typ='mesh'):
                    cmds.menu('loadobj_KitKat', e=1, l=lslist[0])
            else:
                cmds.menu('loadobj_KitKat', e=1, l='| Load Object |')
                if cmds.iconTextCheckBox('editPoseButton_KitKat', q=1, v=1):
                    cmds.iconTextButton('addPoseButton_KitKat', e=1, en=1)
                    cmds.iconTextButton('subPoseButton_KitKat', e=1, en=1)
                    cmds.iconTextCheckBox('editPoseButton_KitKat', e=1, v=0)
        cmds.menuItem(l='Load', c=lambda *args: _loadObj())
        cmds.columnLayout('FiristcL', cat=('both', 2), rs=2, cw=250)

        cmds.rowLayout(nc=3)
        _iconwh = 70
        cmds.iconTextButton('addPoseButton_KitKat', st='iconAndTextVertical', i='pi-add.png', w=_iconwh, h=_iconwh, l='Add', c=lambda *args: self.AddProc())
        cmds.popupMenu()
        cmds.menuItem(l='Mirror', c=lambda *args: self.mirrorPose())
        import tempfile
        with tempfile.NamedTemporaryFile('w+t', suffix='.xpm', delete=False) as tempfileA:
            tempfileA.write('/* XPM */\n  \
                static char *[] = {"20 20 68 1 ","  c None",". c #3A3A3A","X c #3A3A3B","o c #3E3D3F","O c #3E3D40","+ c #3E3E40","@ c #3F3E41","# c #414044", \
                "$ c #424146","% c #434247","& c #444248","* c #444349","= c #46444A","- c #46444B","; c #49474F",": c #4A4750","> c #4B4952",", c #4C4952", \
                "< c #595566","1 c #5A5567","2 c #5B5667","3 c #5B5668","4 c #5C5669","5 c #5C5769","6 c #5D576A","7 c #5D586B","8 c #5E596D","9 c #5F5A6E", \
                "0 c #625C72","q c #635C73","w c #635D73","e c #645D74","r c #645E74","t c #676078","y c #676079","u c #69627C","i c #746B8B","p c #756C8B", \
                "a c #756C8C","s c #776E8F","d c #786F90","f c #8B7EAA","g c #8B7FAB","h c #8F81AF","j c #8F82B0","k c #9083B2","l c #9385B5","z c gray74", \
                "x c #9B8CC1","c c #9C8DC2","v c #9D8DC3","b c #9F8FC6","n c #9F90C7","m c #A090C7","M c #A090C8","N c #A191C9","B c #A292CA","V c #A292CB", \
                "C c #A392CB","Z c #A493CC","A c #A494CD","S c #A695D0","D c #A796D2","F c #A998D3","G c #A998D4","H c #AA99D5","J c #AA99D6","K c #AE9CDB", \
                "                    ","   ..               ","  3CC<              "," .ZKKC.   .........."," .CKKm$.  .zzzzzzzz.", \
                "  <CC<s5  .zzzzzzzz.","   .$sKbo ..........","    .7nKi,lJJk5.    ","      oiS;3$#8cp.   ","       ,:u....#x3   ","      .l<.5AC3.8k.  ", \
                "      .J+.mKKC.+S.  ","      .JX$MKKm.+S.  ","      .rrd3ZC<.7h.  ","      .-DKa#..#x5   ","      .fKGr.#9ca.   ","      eKg-wDJk5.    ", \
                "     -cw......      ","     w-             ","                    "};')
            self.tempIco = tempfileA.name
        cmds.iconTextButton('subPoseButton_KitKat', st='iconAndTextVertical', i=self.tempIco, w=_iconwh, h=_iconwh, l='Delete',
                            c=lambda *args: self.DeleteProc())
        cmds.iconTextCheckBox('editPoseButton_KitKat', st='iconAndTextVertical', i='animPrefsWndIcon.png', w=_iconwh, h=_iconwh, l='Edit',
                              cc=lambda *args: self.EditCallBack())
        cmds.setParent('..')

        cmds.rowLayout(nc=3)
        cmds.columnLayout(cat=('both', 0), rs=1, cw=_iconwh)
        cmds.iconTextButton(st="textOnly", l='Bake', h=26, c=lambda *args: self.BakePoseCallBack())
        cmds.iconTextButton(st="textOnly", l='Remake', h=26, c=lambda *args: self.RemakeBs())
        cmds.setParent('..')
        cmds.iconTextButton(st='iconAndTextVertical', i='kinMirrorJoint_S.png', l='Filp Target', w=_iconwh, h=52, c=lambda *args: self.FilpTarget())
        cmds.popupMenu()
        cmds.radioMenuItemCollection()
        self.FilpAxisItem = [
            cmds.menuItem(l='X', rb=1),
            cmds.menuItem(l='Y', rb=0),
            cmds.menuItem(l='Z', rb=0),
        ]
        cmds.iconTextButton(st='iconAndTextVertical', i='substGeometry.png', l='Bake Cloth', w=_iconwh, h=52, c='')
        cmds.setParent('..')
        cmds.text('editTarget_KitKat', vis=0)
        cmds.text('SaveMirrorL_KitKat', l='_L', vis=0)
        cmds.text('SaveMirrorR_KitKat', l='_R', vis=0)
        
        cmds.columnLayout('MirrorName_Ly_KitKat', cat=('both', 2), rs=2, cw=120, vis=0)
        _L = cmds.textFieldGrp(l='L', tx=cmds.text('SaveMirrorL_KitKat', q=1, l=1), cw2=(15, 95))
        _R = cmds.textFieldGrp(l='R', tx=cmds.text('SaveMirrorR_KitKat', q=1, l=1), cw2=(15, 95))
        _B = cmds.button(l='Save', c=lambda *args: _saveMirror(_L, _R))
        def _saveMirror(_L, _R):
            if cmds.window(ToolUi, q=1, ex=1):
                cmds.text('SaveMirrorL_KitKat', e=1, l=cmds.textFieldGrp(_L, q=1, tx=1))
                cmds.text('SaveMirrorR_KitKat', e=1, l=cmds.textFieldGrp(_R, q=1, tx=1))
            cmds.columnLayout('MirrorName_Ly_KitKat', e=1, vis=0)
        cmds.setParent('..')
        
        cmds.showWindow(ToolUi)

    def helpDoc(self):
        if cmds.window('HelpDoc_KitKat', q=1, ex=1):
            cmds.deleteUI('HelpDoc_KitKat')
        cmds.window('HelpDoc_KitKat', t='Help Doc', rtf=1, mxb=0, wh=(500, 500))
        _iconwh = 60
        cmds.columnLayout(cat=('both', 2), rs=2, cw=500)

        cmds.rowLayout(nc=2)
        cmds.iconTextButton(st='iconAndTextVertical', i='pi-add.png', w=_iconwh, h=_iconwh, l='Add')
        cmds.popupMenu()
        cmds.menuItem(l='Mirror', c=lambda *args: self.mirrorPose())
        cmds.text(l=u'初始化PSD(首次添加): 选择 骨骼 + 控制器 \n 添加Pose: 选择骨骼/控制器 \n 右键菜单: Mirror功能, 可以镜像单个Pose或整个PSD节点', al='left')
        cmds.setParent('..')

        cmds.rowLayout(nc=2)
        cmds.iconTextButton(st='iconAndTextVertical', i=self.tempIco, w=_iconwh, h=_iconwh, l='Delete')
        cmds.text(l=u'选择一个PSD节点或多个Pose, 进行删除操作', al='left')
        cmds.setParent('..')

        cmds.rowLayout(nc=2)
        cmds.iconTextCheckBox(st='iconAndTextVertical', i='animPrefsWndIcon.png', w=_iconwh, h=_iconwh, l='Edit')
        cmds.text(l=u'未加载模型时: 选择单个Pose, 将跳转到选择的Pose \n 已加载模型时: 选择单个Pose, 调出当前修型开始编辑 \
                    \n 按钮点亮时: 将当前的修型模型，塞回指定的BS', al='left')
        cmds.setParent('..')

        cmds.showWindow('HelpDoc_KitKat')

    def EditCallBack(self, stEd=0, fhEd=0):
        if stEd:
            cmds.iconTextButton('addPoseButton_KitKat', e=1, en=0)
            cmds.iconTextButton('subPoseButton_KitKat', e=1, en=0)
            cmds.iconTextCheckBox('editPoseButton_KitKat', e=1, v=1)
            return
        if fhEd:
            cmds.iconTextButton('addPoseButton_KitKat', e=1, en=1)
            cmds.iconTextButton('subPoseButton_KitKat', e=1, en=1)
            cmds.iconTextCheckBox('editPoseButton_KitKat', e=1, v=0)
            return
        if not cmds.iconTextCheckBox('editPoseButton_KitKat', q=1, v=1):
            # 按钮为点亮状态
            self.EditCallBack(0, 1)
            self.transfer2Bs(cmds.text('editTarget_KitKat', q=1, l=1))
        else:
            if cmds.menu('loadobj_KitKat', q=1, l=1) == '| Load Object |':
                self.goToPose()
                cmds.iconTextCheckBox('editPoseButton_KitKat', e=1, v=0)
            else:
                if self.EditProc():   #调出bs, 开始编辑
                    self.EditCallBack(1)
                else:
                    self.EditCallBack(0, 1)

    def AddProc(self, Remake_Data=[]):
        sllist = cmds.ls(sl=1)
        loadobj = cmds.menu('loadobj_KitKat', q=1, l=1)
        if not sllist or loadobj == '| Load Object |':
            return
        _ConnectInfo = cmds.listConnections(sllist[0], d=0, t='joint')
        if cmds.nodeType(sllist[0]) == 'joint':
            _Joint = sllist[0]
        elif _ConnectInfo:
            if cmds.ls('%s.ctrlJnt_Psd' % sllist[0]):
                _Joint = cmds.listConnections('%s.ctrlJnt_Psd' % sllist[0], d=0, t='joint')[0]
        else:
            return
        if not cmds.listConnections(_Joint, s=0, sh=1, t='poseInterpolator'):
            if len(sllist) < 2:
                om.MGlobal.displayError('No Select Controller')
                return
            _poseI = cmds.poseInterpolator(_Joint, n='%s_poseInterpolator' % _Joint)[0]
            _poseIShape = cmds.listRelatives(_poseI, s=1, typ="poseInterpolator")[0]
            cmds.connectAttr('%s.rotate' % sllist[1], '%s.driver[0].driverController[0]' % _poseIShape, f=1)
            cmds.addAttr(_Joint, ln='Associated_Psd', at="message")
            cmds.connectAttr('%s.message' % _poseI, '%s.Associated_Psd' % _Joint, f=1)
            cmds.addAttr(sllist[1], ln='ctrlJnt_Psd', at="message")
            cmds.connectAttr('%s.message' % _Joint, '%s.ctrlJnt_Psd' % sllist[1], f=1)
            cmds.poseInterpolator(_poseIShape, e=1, ap="neutral")
            cmds.setAttr("%s.pose[%s].poseType" % (_poseIShape, cmds.poseInterpolator(_poseIShape, e=1, ap="neutralSwing")), 1)
            cmds.setAttr("%s.pose[%s].poseType" % (_poseIShape, cmds.poseInterpolator(_poseIShape, e=1, ap="neutralTwist")), 2)
            self.PoseAttr_add(cmds.group(n="%s_neutralPose" % _Joint, p=_poseI, em=1), 0, [_Joint, sllist[1], 'neutralPose', (0,0,0)])
            for n in range(3):
                if cmds.menuItem(self.AxisItem[n], q=1, rb=1):
                    break
            cmds.setAttr('%s.driver[0].driverTwistAxis' % _poseIShape, n)
            cmds.lockNode("%s_neutralPose" % _Joint, l=1)
            om.MGlobal.displayInfo('Create neutral Pose Finish!')
            return
        
        if Remake_Data:
            _Joint = Remake_Data[0]
            PoseName = Remake_Data[1]
            _Ctrl = Remake_Data[2]
            _jntRotate = Remake_Data[3]
            dupObj = Remake_Data[4]
        else:
            _rotateData = []
            _jntRotate = cmds.getAttr('%s.r' % _Joint)[0]
            for i in _jntRotate:
                i = round(i)
                if int('%d' %i) < 0:
                    _rotateData.append('n%d' % abs(i))
                else:
                    _rotateData.append('%d' %i)
            PoseName = '%s_%s_%s_%s' % (_Joint, _rotateData[0], _rotateData[1], _rotateData[2])
            if cmds.ls(PoseName):
                om.MGlobal.displayError('Pose already exists.')
                return
            for _Ctrl in cmds.listConnections('%s.message' % _Joint, t='transform'):
                if cmds.ls('%s.ctrlJnt_Psd' %_Ctrl):
                    break
            
            dupObj = cmds.duplicate(loadobj, n='%s_%s' % (loadobj, PoseName), rr=1)[0]
            _dupObjShape = cmds.listRelatives(dupObj, s=1)[0]
            cmds.setAttr('%s.overrideEnabled' % _dupObjShape, 1)
            cmds.setAttr('%s.overrideColor' % _dupObjShape, 20)
            
        _BsName = ''
        for i in cmds.listHistory(loadobj, il=1, pdo=1):
            if cmds.ls('%s.Use2Psd' % i):
                _BsName = i
                break
        if not _BsName:
            _BsName = cmds.blendShape(loadobj, n='Psd_BlendShape%s' % (len(cmds.ls('Psd_BlendShape*', typ='blendShape')) + 1))[0]
            cmds.blendShape(_BsName, e=1, automatic=1, g=loadobj)  # ?不明觉厉
            cmds.addAttr(_BsName, ln='Use2Psd', at='bool')

        lsCposeI = cmds.listConnections('%s.Associated_Psd' % _Joint, d=0, t='transform')[0]
        _lsCposeIShape = cmds.listRelatives(lsCposeI, s=1)[0]
        self.PoseAttr_add(cmds.group(n=PoseName, p=lsCposeI, em=1), 0, [_Joint, _Ctrl, PoseName, _jntRotate])
        cmds.lockNode(PoseName, l=1)
        cmds.addAttr(lsCposeI, ln=PoseName, at='double', min=0, max=1, dv=0)
        poseAttr = '%s.%s' % (lsCposeI, PoseName)

        _newBsId = cmds.getAttr('%s.w' % _BsName, mi=1)
        _newBsId = 0 if not _newBsId else _newBsId[-1] + 1
        cmds.blendShape(_BsName, e=1, tc=1, t=(loadobj, _newBsId, dupObj, 1), w=[_newBsId, 0]) #初始bs开关
        cmds.disconnectAttr('%s.worldMesh[0]' % dupObj, cmds.listConnections('%s.worldMesh[0]' % dupObj, p=1)[0])
        _newBsAttr = '%s.w[%s]' %(_BsName, _newBsId)
        cmds.aliasAttr(PoseName, _newBsAttr)
        _poseId = cmds.poseInterpolator(_lsCposeIShape, e=1, ap=PoseName)
        cmds.setAttr('%s.pose[%s].poseType' % (_lsCposeIShape, _poseId), 1) #Type默认Swing
        cmds.connectAttr('%s.output[%s]' % (_lsCposeIShape, _poseId), poseAttr, f=1)
        cmds.setDrivenKeyframe(_newBsAttr, cd=poseAttr, dv=0, v=0)
        cmds.setDrivenKeyframe(_newBsAttr, cd=poseAttr, dv=1, v=1)

        cmds.setAttr(poseAttr, e=1, cb=1, l=1)
        if not Remake_Data:
            self.PoseAttr_add(dupObj, 1, [_Joint, _Ctrl, PoseName, _jntRotate])
            cmds.select(dupObj, r=1)
            cmds.text('editTarget_KitKat', e=1, l=dupObj)
            cmds.setAttr('%s.v' % loadobj, 0)
            self.EditCallBack(1)
    
    def DeleteProc(self):
        sllist = cmds.ls(sl=1)
        if not sllist:
            return
        for a in sllist:
            if cmds.listRelatives(a, s=1, typ='poseInterpolator'):
                for b in cmds.listRelatives(a, c=1):
                    if cmds.ls('%s.isPose' % b):
                        self._deletePose(b)
                for j in cmds.listConnections('%s.message' % a, t='joint'):
                    if cmds.ls('%s.Associated_Psd' % j):
                        for c in cmds.listConnections('%s.message' % j):
                            if cmds.ls('%s.ctrlJnt_Psd' % c):
                                cmds.deleteAttr('%s.ctrlJnt_Psd' % c)
                                break
                        cmds.deleteAttr('%s.Associated_Psd' % j)
                        break
                cmds.delete(a)
            elif cmds.ls('%s.isPose' % a):
                self._deletePose(a)
                
    def _deletePose(self, name):
        cmds.lockNode(name, l=0)
        PoseName = cmds.getAttr('%s.PoseName' % name)
        if PoseName == 'neutralPose':
            cmds.delete(name)
            return
        a = cmds.listRelatives(name, p=1)[0]
        for c in cmds.listConnections('%s.%s' % (a, PoseName))[:-1]:
            if cmds.ls(c, typ='animCurveUU'):
                for d in cmds.listConnections('%s.output' % c):
                    if cmds.ls(d, typ='blendShape'):
                        for e in cmds.getAttr('%s.w' % d, mi=1):
                            if PoseName == cmds.aliasAttr('%s.w[%s]' % (d, e), q=1):
                                break
                        #_targetId = cmds.ls('%s.inputTarget[0].inputTargetGroup[*]' % d)[e].split('%s.inputTarget[0].inputTargetGroup[' % d)[1][:-1]
                        mel.eval('blendShapeDeleteTargetGroup %s %s' % (d, e))
        cmds.setAttr('%s.%s' % (a, PoseName), e=1, cb=1, l=0)
        cmds.deleteAttr(a, at=PoseName)
        cmds.poseInterpolator(cmds.listRelatives(a, s=1, typ='poseInterpolator')[0], e=1, dp=PoseName)
        cmds.delete(name)

    def EditProc(self):
        sllist = cmds.ls(sl=1)
        loadobj = cmds.menu('loadobj_KitKat', q=1, l=1)
        if not sllist or loadobj == '| Load Object |':
            return 0
        if cmds.ls('%s.isPose' % sllist[0]):
            self.goToPose(sllist[0])
            dupObj = self.extractPose(sllist[0])
            cmds.text('editTarget_KitKat', e=1, l=dupObj)
            cmds.select(dupObj, r=1)
            cmds.setAttr('%s.v' % loadobj, 0)
            return 1
        elif cmds.ls('%s.isEditMesh' % sllist[0]):
            cmds.text('editTarget_KitKat', e=1, l=sllist[0])
            return 1
        else:
            return 0
        
    def PoseAttr_add(self, transName, _type, _Data_):
        cmds.addAttr(transName, ln='JointName', dt="string")
        cmds.setAttr('%s.JointName' % transName, _Data_[0], typ='string')
        cmds.addAttr(transName, ln='CtrlName', dt="string")
        cmds.setAttr('%s.CtrlName' % transName, _Data_[1], typ='string')
        cmds.addAttr(transName, ln='PoseName', dt="string")
        cmds.setAttr('%s.PoseName' % transName, _Data_[2], typ='string')
        cmds.addAttr(transName, ln="JointRotate", at='double3')
        cmds.addAttr(transName, ln="JointRotateX", at='double', dv=_Data_[3][0], p="JointRotate")
        cmds.addAttr(transName, ln="JointRotateY", at='double', dv=_Data_[3][1], p="JointRotate")
        cmds.addAttr(transName, ln="JointRotateZ", at='double', dv=_Data_[3][2], p="JointRotate")
        if not _type:
            cmds.addAttr(transName, ln='isPose', at="bool")
        elif _type == 1:
            cmds.addAttr(transName, ln='isEditMesh', at="bool")
            for i in ['.tx', '.ty', '.tz', '.rx', '.ry', '.rz', '.sx', '.sy', '.sz']:
                cmds.setAttr('%s%s' % (transName, i), l=0)
            
    def transfer2Bs(self, name):
        if not cmds.ls('%s.isEditMesh' % name):
            om.MGlobal.displayError('Object not exists.')
            return
        loadobj = cmds.menu('loadobj_KitKat', q=1, l=1)
        for i in cmds.listHistory(loadobj, il=1, pdo=1):
            if cmds.ls('%s.Use2Psd' % i):
                _BsName = i
        PoseName = cmds.getAttr('%s.PoseName' % name)
        _bsList = cmds.listAttr('%s.w[*]' % _BsName)
        for i in cmds.getAttr('%s.w' % _BsName, mi=1):
            if PoseName == cmds.aliasAttr('%s.w[%s]' % (_BsName, i), q=1):
                break
        self.goToPose(PoseName)
        cmds.blendShape(_BsName, e=1, t=(loadobj, i, name, 1.0), w=[i, 1])    #塞回去的时候有顺序问题
        cmds.aliasAttr(PoseName, '%s.w[%s]' %(_BsName, i))
        cmds.delete(name)
        cmds.setAttr('%s.v' % loadobj, 1)
    
    def goToPose(self, name=''):
        sllist = cmds.ls(sl=1)
        if sllist or name:
            if not name:
                name = sllist[0]
            _nAttr = '%s.CtrlName' % name
            _rAttr = '%s.JointRotate' % name
            if cmds.ls(_nAttr) and cmds.ls(_rAttr):
                _rotate = cmds.getAttr(_rAttr)[0]
                cmds.setAttr('%s.r' % cmds.getAttr(_nAttr), _rotate[0], _rotate[1], _rotate[2])
    
    def extractPose(self, name):
        #需要提前判断 loadobj 和 '%s.isPose'
        #rebuildSelectedTargetShape     cmds.sculptTarget(_BsName, e=1, r=1, t=0)
        loadobj = cmds.menu('loadobj_KitKat', q=1, l=1)
        _Joint = cmds.getAttr('%s.JointName' % name)
        _Ctrl = cmds.getAttr('%s.CtrlName' % name)
        _jntRotate = cmds.getAttr('%s.JointRotate' % name)[0]
        PoseName = cmds.getAttr('%s.PoseName' % name)
        dupObj = cmds.duplicate(loadobj, n='%s_%s' % (loadobj, PoseName), rr=1)[0]
        _dupObjShape = cmds.listRelatives(dupObj, s=1)[0]
        cmds.setAttr('%s.overrideEnabled' % _dupObjShape, 1)
        cmds.setAttr('%s.overrideColor' % _dupObjShape, 20)
        self.PoseAttr_add(dupObj, 1, [_Joint, _Ctrl, PoseName, _jntRotate])
        return dupObj
    
    def BakePoseCallBack(self):
        sllist = cmds.ls(sl=1)
        loadobj = cmds.menu('loadobj_KitKat', q=1, l=1)
        if not sllist or loadobj == '| Load Object |':
            return
        self.BakePose(sllist)
        
    def BakePose(self, data):
        _exPose = []
        if cmds.listRelatives(data, s=1, typ='poseInterpolator'):
            _childItem = cmds.listRelatives(data, c=1, typ='transform')
            for i in _childItem[1:]:
                if cmds.ls('%s.isPose' % i):
                    self.goToPose(i)
                    _exPose.append(self.extractPose(i))
            self.goToPose(_childItem[0])
        else:
            for i in data:
                if cmds.ls('%s.isPose' % i):
                    self.goToPose(i)
                    _exPose.append(self.extractPose(i))
                self.goToPose(cmds.listRelatives(cmds.listRelatives(i, p=1)[0], c=1, typ='transform')[0])
        cmds.select(_exPose, r=1)
        return _exPose

    def RemakeBs(self):
        sllist = cmds.ls(sl=1)
        loadobj = cmds.menu('loadobj_KitKat', q=1, l=1)
        if not sllist or loadobj == '| Load Object |':
            return
        for i in sllist:
            if not cmds.ls('%s.isEditMesh' % i):
                continue
            _Joint = cmds.getAttr('%s.JointName' % i)
            _Ctrl = cmds.getAttr('%s.CtrlName' % i)
            _jntRotate = cmds.getAttr('%s.JointRotate' % i)[0]
            PoseName = cmds.getAttr('%s.PoseName' % i)
            if not cmds.ls('%s.Associated_Psd' % _Joint):
                cmds.select(_Joint, _Ctrl, r=1)
                self.AddProc()
            elif cmds.ls(PoseName):
                self.goToPose(i)
                self.transfer2Bs(i)
                self.goToPose(cmds.listRelatives(cmds.listRelatives(i, p=1)[0], c=1, typ='transform')[0])
                continue
            cmds.setAttr('%s.r' % _Ctrl, _jntRotate[0], _jntRotate[1], _jntRotate[2])
            cmds.select(_Joint, r=1)
            self.AddProc([_Joint, PoseName, _Ctrl, _jntRotate, i])
            self.goToPose(cmds.listRelatives(cmds.listRelatives(PoseName, p=1)[0], c=1, typ='transform')[0])
    
    def FilpTarget(self):
        sllist = cmds.ls(sl=1)
        loadobj = cmds.menu('loadobj_KitKat', q=1, l=1)
        if not sllist or loadobj == '| Load Object |':
            return
        _filpPose = []
        for i in sllist:
            sourceObj = cmds.duplicate(loadobj, n='_TempSourceMesh_')
            dupObj = cmds.duplicate(i, n='_TempFilpMesh_')
            bs = cmds.blendShape(dupObj[0], sourceObj[0], w=(0,1), tc=0)[0]
            cmds.refresh()
            for n in range(3):
                if cmds.menuItem(self.FilpAxisItem[n], q=1, rb=1):
                    break
            mel.eval('doBlendShapeFlipTarget %s 0 {"%s.0"}' % (n + 1, bs))
            
            if cmds.ls('%s.isEditMesh' % i):
                _Joint = cmds.getAttr('%s.JointName' % i)
                _Ctrl = cmds.getAttr('%s.CtrlName' % i)
                _jntRotate = cmds.getAttr('%s.JointRotate' % i)[0]
                PoseName = cmds.getAttr('%s.PoseName' % i)
                _old = cmds.text('SaveMirrorL_KitKat', q=1, l=1)
                _new = cmds.text('SaveMirrorR_KitKat', q=1, l=1)
                filpObj = cmds.duplicate(sourceObj[0], n=i.replace(_old, _new))[0]
                _filpObjShape = cmds.listRelatives(filpObj, s=1)[0]
                cmds.setAttr('%s.overrideEnabled' % _filpObjShape, 1)
                cmds.setAttr('%s.overrideColor' % _filpObjShape, 20)
                self.PoseAttr_add(filpObj, 1, [_Joint.replace(_old, _new), _Ctrl.replace(_old, _new), PoseName.replace(_old, _new), _jntRotate])
                _filpPose.append(filpObj)
            else:
                cmds.duplicate(sourceObj[0], n='{}_Filp'.format(i))
            cmds.delete(sourceObj, dupObj)
        cmds.select(_filpPose, r=1)
        return _filpPose

    def mirrorPose(self):
        sllist = cmds.ls(sl=1)
        loadobj = cmds.menu('loadobj_KitKat', q=1, l=1)
        if not sllist or loadobj == '| Load Object |':
            return
        exPose = self.BakePose(sllist)
        filpPose = self.FilpTarget()
        self.RemakeBs()
        cmds.delete(exPose, filpPose)
        
PSD_PoseUi_KitKat().ToolUi()
