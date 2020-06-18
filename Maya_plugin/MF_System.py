from maya import cmds
import maya.OpenMaya as Om
import decimal, re


class MFcreate():

    def MFUi(self):
        freeRotate = 0
        MFUi = 'MFxxx'
        if cmds.window(MFUi, q=1, ex=1):
                cmds.deleteUI(MFUi)
        cmds.window(MFUi, t=MFUi + 'v1.0', wh=(120, 100), tlb=1)
        cmds.columnLayout('MainLayout', cat=('both', 2), rs=2, cw=120)
        cmds.button('CreateMFButton', l='Create_MF', c=lambda *args: self.createMF())
        if cmds.ls('master_MF'):
            cmds.button('CreateMFButton', e=1, bgc=[0, 1, 0])
            if not cmds.ls('MidJoint_loc'):
                cmds.button('CreateMFButton', e=1, nbg=0)
                cmds.button('CreateMFButton', e=1, en=0)
        cmds.button('SetVtrlButton', l='SetCtrl', c=lambda *args: self.setCtrl(None), vis=freeRotate)
        cmds.popupMenu()
        cmds.menuItem(l='Break', c=lambda *args: self.Break())
        cmds.rowLayout(nc=2, cw2=(55, 55))
        cmds.button('R90Button', l='Rotate90', c=lambda *args: self.setCtrl('90'))
        cmds.button('R-90Button', l='Rotate-90', c=lambda *args: self.setCtrl('-90'))
        cmds.showWindow(MFUi)

        self.JointName = ['Center_Joint', 'YuAxis_Joint', 'YdAxis_Joint', 'XlAxis_Joint', 'XrAxis_Joint', 'ZfAxis_Joint', 'ZbAxis_Joint',
                            'L2_1_Joint',               'L2_3_Joint',                             'L2_7_Joint',               'L2_9_Joint',
                            'L1_1_Joint', 'L1_2_Joint', 'L1_3_Joint', 'L1_4_Joint', 'L1_6_Joint', 'L1_7_Joint', 'L1_8_Joint', 'L1_9_Joint',
                            'L3_1_Joint', 'L3_2_Joint', 'L3_3_Joint', 'L3_4_Joint', 'L3_6_Joint', 'L3_7_Joint', 'L3_8_Joint', 'L3_9_Joint']

    def createMF(self):
        if cmds.ls('master_MF|MidJoint_loc'):
            for i in ['MidJoint_loc', 'UpJoint_loc']:
                jointN = self.JointName[0] if i == 'MidJoint_loc' else self.JointName[1]
                cmds.select(cl=1)
                cmds.delete(cmds.parentConstraint(i, cmds.joint(n=jointN), w=1), i)
            midPosition = cmds.getAttr(self.JointName[0] + '.ty')
            distance = cmds.getAttr(self.JointName[1] + '.ty') - midPosition
            for i in self.JointName[2:]:
                cmds.select(cl=1)
                cmds.joint(n=i)
            for i in self.JointName[3:11]:
                cmds.setAttr(i + '.ty', midPosition)
            for i in self.JointName[11:19]:
                cmds.setAttr(i + '.ty', midPosition - distance)
            for i in self.JointName[19:]:
                cmds.setAttr(i + '.ty', midPosition + distance)
            cmds.setAttr(self.JointName[2] + '.ty', midPosition - distance)
            for n, s in zip([3, 5, 7, 7, 8, 9, 11, 11, 12, 13, 14, 16, 19, 19, 20, 21, 22, 24],
                            ['x', 'z', 'x', 'z', 'z', 'x', 'x', 'z', 'z', 'z', 'x', 'x', 'x', 'z', 'z', 'z', 'x', 'x']):
                cmds.setAttr('%s.t%s' % (self.JointName[n], s), distance)
            for n, s in zip([4, 6, 8, 9, 10, 10, 13, 15, 16, 17, 18, 18, 21, 23, 24, 25, 26, 26],
                            ['x', 'z', 'x', 'z', 'x', 'z', 'x', 'x', 'z', 'z', 'x', 'z', 'x', 'x', 'z', 'z', 'x', 'z']):
                cmds.setAttr('%s.t%s' % (self.JointName[n], s), -distance)
            _v = [(0, 1, 0), (1, 0, 0), (0, 0, 1)]
            Attr = ['.tx', '.ty', '.tz', '.rx', '.ry', '.rz', '.sx', '.sy', '.sz']
            for i, a in zip(self.JointName[:7], [9, 0, 0, 1, 1, 2, 2]):
                if a == 9:
                    for v, n in zip(_v, [['CenterY_Joint', '.ry'], ['CenterX_Joint', '.rx'], ['CenterZ_Joint', '.rz']]):
                        cmds.delete(cmds.parentConstraint(i, cmds.parent(
                                        cmds.group(cmds.circle(nr=v, r=2*distance+1, n=n[0] + '_Ctrl'), n=n[0] + '_Ctrl_grp'), 'master_MF'), w=1),
                                    cmds.parentConstraint(i, cmds.parent(
                                        cmds.nurbsPlane(ax=v, w=3.5*distance, ch=0, n=n[0].rsplit('_')[0] + '_Surface'), 'master_MF'), w=1))
                        for l in Attr:
                            if l == n[1]:
                                continue
                            cmds.setAttr('%s_Ctrl%s' % (n[0], l), l=1)
                else:
                    cmds.delete(cmds.parentConstraint(i, cmds.parent(
                                    cmds.group(cmds.circle(nr=_v[a], r=2*distance+1, n=i + '_Ctrl'), n=i + '_Ctrl_grp'), 'master_MF'), w=1),
                                cmds.parentConstraint(i, cmds.parent(
                                    cmds.nurbsPlane(ax=_v[a], w=3.5*distance, ch=0, n=i.rsplit('_')[0] + '_Surface'), 'master_MF'), w=1))
                    for l in Attr:
                        cmds.setAttr('%s_Ctrl%s' % (i, l), l=1)
                    cmds.setAttr('%s_Ctrl.r%s' % (i, i[0].lower()), l=0)
            '''
            getUVface = Om.MSelectionList()
            getUVface.add('YuAxis_Surface')
            faceDagPath = Om.MDagPath()
            getUVface.getDagPath(0, faceDagPath)
            scriputil = Om.MScriptUtil()
            paramu = scriputil.asDoublePtr()
            scriputil2 = Om.MScriptUtil()
            paramv = scriputil2.asDoublePtr()
            _temp_getUVJoint = self.JointName[19:]
            _temp_getUVJoint.append('YuAxis_Joint')
            for i in _temp_getUVJoint:
                jointpos = cmds.xform(i, q=1, ws=1, t=1)
                mPoint = Om.MPoint(jointpos[0], jointpos[1], jointpos[2])
                surfacea = Om.MFnNurbsSurface(faceDagPath).getParamAtPoint(mPoint, paramu, paramv, Om.MSpace.kWorld)
                self.uvFloat.append([float(decimal.Decimal(str(scriputil.getDouble(paramu))).quantize(decimal.Decimal('%.3f' % 1))),
                                        float(decimal.Decimal(str(scriputil.getDouble(paramv))).quantize(decimal.Decimal('%.3f' % 1)))])
            '''
            cmds.select(cl=1)
            cmds.parent(self.JointName, cmds.joint(n='RootJoint'))
            cmds.parent('RootJoint', 'master_MF')
            cmds.setAttr(cmds.group(cmds.ls("master_MF|*_Surface"), n='MF_Surface_grp') + '.visibility', 0)
            cmds.button('CreateMFButton', e=1, nbg=0)
            cmds.button('CreateMFButton', e=1, en=0)
        else:
            masterC = cmds.circle(nr=(0, 1, 0), r=4, ch=0, n='master_MF')
            cmds.addAttr('|master_MF', ln="CtrlJoint", dt="string")
            cmds.setAttr(cmds.listRelatives(masterC, c=1, s=1)[0] + '.overrideEnabled', 1)
            cmds.setAttr(cmds.listRelatives(masterC, c=1, s=1)[0] + '.overrideColor', 17)
            cmds.setAttr(cmds.spaceLocator(n='MidJoint_loc')[0] + '.ty', 1)
            Attr = ['.tx', '.tz', '.rx', '.ry', '.rz']
            for i in Attr:
                cmds.setAttr('MidJoint_loc' + i, lock=1)
            cmds.setAttr(cmds.duplicate('MidJoint_loc', rr=1, n='UpJoint_loc')[0] + '.ty', 2)
            cmds.parent('UpJoint_loc', 'MidJoint_loc', masterC)
            cmds.button('CreateMFButton', e=1, bgc=[0, 1, 0])

    def setCtrl(self, Rotate):
        ctrl = cmds.ls(sl=1)[0]
        if not re.match('\S*_Joint_Ctrl', ctrl):
            return
        self.Break()
        midName = ctrl.split('_')[0]
        decimal.getcontext().rounding = 'ROUND_HALF_UP'
        getUVface = Om.MSelectionList()
        getUVface.add(midName + '_Surface')
        faceDagPath = Om.MDagPath()
        getUVface.getDagPath(0, faceDagPath)
        ctrlJoint = []
        for i in self.JointName:
            jointpos = cmds.xform(i, q=1, ws=1, t=1)
            distance = Om.MFnNurbsSurface(faceDagPath).distanceToPoint(Om.MPoint(jointpos[0], jointpos[1], jointpos[2]), Om.MSpace.kWorld)
            if float(decimal.Decimal(str(distance)).quantize(decimal.Decimal('%.3f' % 1))) == 0:
                ctrlJoint.append(i)
        if 'Center_Joint' in ctrlJoint:
            ctrlJoint.remove('Center_Joint')
            cmds.parent(ctrlJoint, 'Center_Joint')
            cmds.orientConstraint(ctrl, 'Center_Joint', mo=1, w=1, n='_temp_CtrlConstraint')
            cmds.setAttr('master_MF.CtrlJoint', 'Center_Joint', typ='string')
        else:
            for j in ctrlJoint:
                if not 'L' in j:
                    cmds.orientConstraint(ctrl, j, mo=1, w=1, n='_temp_CtrlConstraint')
                    cmds.setAttr('master_MF.CtrlJoint', j, typ='string')
                    _tempMidJoint = j
                    ctrlJoint.remove(j)
                    break
            cmds.parent(ctrlJoint, _tempMidJoint)
        if Rotate:
            rotateAxis = ['.rx', '.ry', '.rz']
            for i in rotateAxis:
                if not cmds.getAttr(ctrl + i, l=1):
                    if i == '.rx':
                        cmds.rotate(int(Rotate), 0, 0, ctrl, r=1, os=1, fo=1)
                    elif i == '.ry':
                        cmds.rotate(0, int(Rotate), 0, ctrl, r=1, os=1, fo=1)
                    elif i == '.rz':
                        cmds.rotate(0, 0, int(Rotate), ctrl, r=1, os=1, fo=1)
            self.Break()
        cmds.select(ctrl, r=1)
        cmds.button('SetVtrlButton', e=1, bgc=[0, 1, 0])

    def Break(self):
        _oldMidJoint = cmds.getAttr('master_MF.CtrlJoint')
        if not _oldMidJoint:
            sljnt = cmds.ls(sl=1, typ='joint')
            if not sljnt:
                #Om.MGlobal.displayWarning('Not find Break. If need Break, select Mid Joint')
                return
            _oldMidJoint = sljnt[0]
        if cmds.ls('_temp_CtrlConstraint'):
            cmds.delete('_temp_CtrlConstraint')
        childJ = cmds.listRelatives(_oldMidJoint, c=1)
        parentJ = cmds.listRelatives(_oldMidJoint, p=1)[0]
        for i in childJ:
            cmds.parent(i, parentJ)
        cmds.setAttr('master_MF.CtrlJoint', '', typ='string')
        cmds.button('SetVtrlButton', e=1, nbg=0)

MFcreate().MFUi()