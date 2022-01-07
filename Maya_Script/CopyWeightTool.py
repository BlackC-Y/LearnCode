# -*- coding: UTF-8 -*-
from maya import cmds, mel


class CopyWeightTool():

    #__Verision = 1.41

    def Ui(self):
        ToolUi = 'CopyWeightTool'
        if cmds.window(ToolUi, q=1, ex=1):
            cmds.deleteUI(ToolUi)
        cmds.window(ToolUi, t=ToolUi, rtf=1, mb=1, mxb=0, wh=(300, 85))
        cmds.columnLayout(cat=('both', 2), rs=2, cw=300, adj=1)
        cmds.textFieldButtonGrp('sourceText', l='soure', bl='Select', adj=2, ed=0, cw3=[40, 200, 60],
                                bc=lambda *args: cmds.textFieldButtonGrp('sourceText', e=1, tx=str(cmds.ls(sl=1))))
        cmds.popupMenu()
        cmds.menuItem(l='Select', c=lambda *args: cmds.select(self.strProc(cmds.textFieldButtonGrp('sourceText', q=1, tx=1)), r=1))
        cmds.textFieldButtonGrp('targeText', l='targe', bl='Select', adj=2, ed=0, cw3=[40, 200, 60],
                                bc=lambda *args: cmds.textFieldButtonGrp('targeText', e=1, tx=str(cmds.ls(sl=1))))
        cmds.popupMenu()
        cmds.menuItem(l='Select', c=lambda *args: cmds.select(self.strProc(cmds.textFieldButtonGrp('targeText', q=1, tx=1)), r=1))
        cmds.rowLayout(nc=2)
        def _tVis():
            if cmds.text('helpDoc_CopyWeight', q=1, vis=1):
                cmds.text('helpDoc_CopyWeight', e=1, vis=0)
            else:
                cmds.text('helpDoc_CopyWeight', e=1, vis=1)
        cmds.button(l='Help', w=40, c=lambda *args: _tVis())
        cmds.button(l='Run', w=255, c=lambda *args: self.runProc())
        cmds.setParent('..')
        cmds.text('helpDoc_CopyWeight', l=u'源：整个模型 - 模型的点/线/面\n\n目标：源模型的点/线/面\n     单个有蒙皮模型的点/线/面\n     多个无蒙皮模型\n     单个无蒙皮Surface曲面模型\n', al='left', fn='fixedWidthFont', vis=0)
        cmds.showWindow(ToolUi)

    def runProc(self):
        _temp1_ = cmds.textFieldButtonGrp('sourceText', q=1, tx=1)
        _temp2_ = cmds.textFieldButtonGrp('targeText', q=1, tx=1)
        if not _temp1_ or not _temp2_:
            return
        sourelist = cmds.ls(self.strProc(_temp1_), fl=1)
        targelist = cmds.ls(self.strProc(_temp2_), fl=1)
        soureObj = cmds.ls(sourelist, o=1)[0]
        targeObj = cmds.ls(targelist, o=1)
        Extract = 0
        #源
        if not cmds.objectType(soureObj, i='transform'):   #是点线面
            Extract = 1   #为点线面时提取
            soureObj = cmds.listRelatives(soureObj, p=1)[0]
        elif sourelist[0] == soureObj:   #是整个模型
            Extract = 0
        #目标
        if not cmds.objectType(targeObj[0], i='transform'):   #目标选的是点线面
            targeObj = cmds.listRelatives(targeObj[0], p=1)
        
        Extract = 1 if soureObj == targeObj[0] else 0   #目标和源为相同模型 需要提取
        
        soureSkinCluster = mel.eval('findRelatedSkinCluster("%s")' % soureObj)
        if not soureSkinCluster:
            cmds.error('Soure object No Skin')
        if not '.f[' in _temp1_:
            sourelist = cmds.ls(cmds.polyListComponentConversion(sourelist, fv=1, fe=1, fuv=1, fvf=1, tf=1), fl=1)
        infJointList = cmds.skinCluster(soureObj, q=1, inf=1)   #所有骨骼
        jntLock = [cmds.getAttr('%s.liw' %j) for j in infJointList]

        if Extract:
            _TempObj_ = cmds.duplicate(soureObj, rr=1)[0]
            #allList = ['%s.f[%s]' % (soureObj, i) for i in range(cmds.polyEvaluate(_TempObj_, f=1))]
            _difflist_ = set(cmds.ls('%s.f[*]' %soureObj, fl=1)).difference(set(sourelist))
            _list_ = [i.replace(soureObj, _TempObj_) for i in _difflist_]
            if cmds.ls(_list_):
                cmds.delete(_list_)
            cmds.skinCluster(infJointList, _TempObj_, tsb=1, dr=4)
            cmds.copySkinWeights(soureObj, _TempObj_, nm=1, sa='closestPoint', ia='oneToOne', nr=1)
            soureObj = _TempObj_

        if cmds.listRelatives(targeObj, c=1, s=1, typ='nurbsSurface'):
            self.SurfaceCWeight(1, sourelist, targelist, soureObj, targeObj[0])
        else:
            #_list_ = [_TempObj_]
            # finalCopyList = _list_ + targelist   塞进列表第一位
            for i in targeObj:
                if not mel.eval('findRelatedSkinCluster("%s")' % i):
                    cmds.skinCluster(infJointList, i, tsb=1, mi=cmds.getAttr('%s.maxInfluences' % soureSkinCluster), dr=4)
                    targelist = i
                else:
                    if not '.vtx[' in _temp2_:
                        targelist = cmds.ls(cmds.polyListComponentConversion(targelist, ff=1, fe=1, fuv=1, fvf=1, tv=1), fl=1)
                cmds.copySkinWeights(soureObj, targelist, nm=1, sa='closestPoint', ia=('oneToOne', 'closestJoint'), nr=1)
        if Extract:
            cmds.delete(_TempObj_)
        for j, l in zip(infJointList, jntLock):
            cmds.setAttr('%s.liw' %j, l)
        print('Finish!')

    def SurfaceCWeight(self, mode, sourelist, targelist, soureObj, targeObj):
        _StPObj = cmds.nurbsToPoly(targeObj, mnd=1, ch=0, f=3, n='__TempStP_Obj')[0]
        #soureSkinCluster = mel.eval('findRelatedSkinCluster("%s")' % soureObj)
        targeSkinCluster = mel.eval('findRelatedSkinCluster("%s")' %targeObj)
        infJointList = cmds.skinCluster(soureObj, q=1, inf=1)
        cmds.skinCluster(infJointList, _StPObj, tsb=1, dr=4)
        cmds.copySkinWeights(soureObj, _StPObj, nm=1, sa='closestPoint', ia=('oneToOne', 'closestJoint'), nr=1)
        StpSkinCluster = mel.eval('findRelatedSkinCluster("%s")' %_StPObj)
        if not targeSkinCluster:
            cmds.skinCluster(infJointList, targeObj, tsb=1, dr=4)
            targeSkinCluster = mel.eval('findRelatedSkinCluster("%s")' %targeObj)
        
        _cPOMNode = cmds.createNode('closestPointOnMesh', n='__TempcPOM_Node')
        cmds.connectAttr('%s.worldMesh[0]' %cmds.listRelatives(_StPObj, s=1, c=1)[0], '%s.inMesh' %_cPOMNode, f=1)
        for i in cmds.ls('%s.cv[*][*]' %targeObj, fl=1):
            cvTrans = cmds.xform(i, q=1, ws=1, t=1)
            cmds.setAttr('%s.inPosition' %_cPOMNode, cvTrans[0], cvTrans[1], cvTrans[2])
            vtxIndex = cmds.getAttr('%s.vt' %_cPOMNode)
            valueList = cmds.skinPercent(StpSkinCluster, '%s.vtx[%s]' %(_StPObj, vtxIndex), q=1, ib=.000000001, v=1)
            transList = cmds.skinPercent(StpSkinCluster, '%s.vtx[%s]' %(_StPObj, vtxIndex), q=1, ib=.000000001, t=None)
            tvList = [[transList[u], valueList[u]] for u in range(len(valueList))]
            exec('cmds.skinPercent("%s", "%s", tv=%s)' % (targeSkinCluster, i, tvList))
        cmds.delete(_StPObj, _cPOMNode)

    def strProc(self, Onestr):
        if ', ' in Onestr:
            return [i[2:-1] for i in Onestr[1:-1].split(', ')]
        elif int(cmds.about(v=1)) >= 2022:
            return [Onestr[2:-2]]
        else:
            return [Onestr[3:-2]]

CopyWeightTool().Ui()
