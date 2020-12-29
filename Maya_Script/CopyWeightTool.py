from maya import cmds, mel

class CopyWeightTool():

    __Verision = 1.3

    def Ui(self):
        ToolUi = 'CopyWeightTool'
        if cmds.window(ToolUi, q=1, ex=1):
            cmds.deleteUI(ToolUi)
        cmds.window(ToolUi, t=ToolUi, rtf=1, mb=1, mxb=0, wh=(300, 85))
        cmds.columnLayout('FiristcL', cat=('both', 2), rs=2, cw=300, adj=1)
        cmds.textFieldButtonGrp('sourceText', l='soure', bl='Select', adj=2, ed=0, cw3=[40,200,60], 
                                    bc=lambda *args: cmds.textFieldButtonGrp('sourceText', e=1, tx=str(cmds.ls(sl=1))))
        cmds.popupMenu()
        cmds.menuItem(l='Select', c=lambda *args: cmds.select(self.strProc(cmds.textFieldButtonGrp('sourceText', q=1, tx=1)), r=1))
        cmds.textFieldButtonGrp('targeText', l='targe', bl='Select', adj=2, ed=0, cw3=[40,200,60], 
                                    bc=lambda *args: cmds.textFieldButtonGrp('targeText', e=1, tx=str(cmds.ls(sl=1))))
        cmds.popupMenu()
        cmds.menuItem(l='Select', c=lambda *args: cmds.select(self.strProc(cmds.textFieldButtonGrp('targeText', q=1, tx=1)), r=1))
        cmds.button('Run', c=lambda *args: self.Runfun())
        cmds.showWindow(ToolUi)

    def Runfun(self):
        _temp1_ = cmds.textFieldButtonGrp('sourceText', q=1, tx=1)
        _temp2_ = cmds.textFieldButtonGrp('targeText', q=1, tx=1)
        if not _temp1_ or not _temp2_:
            return
        sourelist = cmds.ls(self.strProc(_temp1_), fl=1)
        targelist = cmds.ls(self.strProc(_temp2_), fl=1)
        soureObj = cmds.ls(sourelist, o=1)[0]
        targeObj = cmds.ls(targelist, o=1)[0]
        if cmds.objectType(soureObj, i='mesh'):
            soureObj = cmds.listRelatives(soureObj, p=1)[0]
        if cmds.objectType(targeObj, i='mesh'):
            targeObj = cmds.listRelatives(targeObj, p=1)[0]
        same = 1 if soureObj == targeObj else 0
        soureSkCluster = mel.eval('findRelatedSkinCluster("%s")' %soureObj)
        if not soureSkCluster:
            cmds.warning('Soure No Skin')
            return
        if not '.f[' in _temp1_:
            sourelist = cmds.ls(cmds.polyListComponentConversion(sourelist, fv=1, fe=1, fuv=1 ,fvf=1, tf=1), fl=1)
        
        infJointList = cmds.skinCluster(soureObj, q=1, inf=1)
        jntLock = [cmds.getAttr(j + '.liw') for j in infJointList]
        if same:
            _TempObj_ = cmds.duplicate(soureObj, rr=1)[0]
            _list_ = ['%s.f[%s]' %(_TempObj_, i) for i in range(cmds.polyEvaluate(_TempObj_, f=1)) if not '%s.f[%s]' %(soureObj, i) in set(sourelist)]
            if cmds.ls(_list_):
                cmds.delete(_list_)
            cmds.skinCluster(infJointList, _TempObj_ ,tsb=1, dr=4)
            cmds.copySkinWeights(soureObj, _TempObj_, nm=1, sa='closestPoint', ia='oneToOne', nr=1)
            soureObj = _TempObj_
        if not mel.eval('findRelatedSkinCluster("%s")' %targeObj):
            cmds.skinCluster(infJointList, targeObj, tsb=1, mi=cmds.getAttr('%s.maxInfluences' %soureSkCluster), dr=4)
            #cmds.getAttr('%s.maintainMaxInfluences' %soureSkCluster)
        if not '.vtx[' in _temp2_:
            targelist = cmds.ls(cmds.polyListComponentConversion(targelist, ff=1, fe=1, fuv=1 ,fvf=1, tv=1), fl=1)
        #_list_ = [_TempObj_]
        #finalCopyList = _list_ + targelist   塞进列表第一位
        cmds.copySkinWeights(soureObj, targelist, nm=1, sa='closestPoint', ia=('oneToOne', 'closestJoint'), nr=1)
        if same:
            cmds.delete(_TempObj_)
        for j, l in zip(infJointList, jntLock):
            cmds.setAttr(j + '.liw', l)
    
    def strProc(self, Onestr):
        return [i[2:-1] for i in Onestr[1:-1].split(', ')] if ', ' in Onestr else [Onestr[3:-2]]

CopyWeightTool().Ui()
