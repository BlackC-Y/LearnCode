from maya import cmds, mel

class CopyWeightTool():

    __Verision = 1.0

    def Ui(self)：
        ToolUi = 'CopyWeightTool'
        if cmds.window(ToolUi, q=1, ex=1):
            cmds.deleteUI(ToolUi)
        cmds.window(ToolUi, t=ToolUi, rtf=1, mb=1, mxb=0, wh=(300, 85))
        cmds.columnLayout('FiristcL', cat=('both', 2), rs=2, cw=300, adj=1)
        cmds.textFieldButtonGrp('sourceText', l='soure', bl='Select', adj=2, ed=0, cw3=[40,200,60], 
                                    bc=lambda *args: cmds.textFieldButtonGrp('sourceText', e=1, tx=str(cmds.ls(sl=1))))
        cmds.popupMenu()
        cmds.menuItem(l='Select', c=lambda *args: cmds.select(eval(cmds.textFieldButtonGrp('sourceText', q=1, tx=1)), r=1))
        cmds.textFieldButtonGrp('targeText', l='targe', bl='Select', adj=2, ed=0, cw3=[40,200,60], 
                                    bc=lambda *args: cmds.textFieldButtonGrp('targeText', e=1, tx=str(cmds.ls(sl=1))))
        cmds.popupMenu()
        cmds.menuItem(l='Select', c=lambda *args: cmds.select(eval(cmds.textFieldButtonGrp('targeText', q=1, tx=1)), r=1))
        cmds.button('Run', c=lambda *args: Runfun())
        cmds.showWindow(ToolUi)

    def Runfun():
        _temp1_ = cmds.textFieldButtonGrp('sourceText', q=1, tx=1)
        _temp2_ = cmds.textFieldButtonGrp('targeText', q=1, tx=1)
        if not _temp1_ or not _temp2_:
            return
        sourelist = cmds.ls(eval(_temp1_), fl=1)
        targelist = cmds.ls(eval(_temp2_), fl=1)
        soureObj = eval(_temp1_)[0].split('.')[0]
        _TempObj_ = cmds.duplicate(soureObj, rr=1)[0]
        if not '.f[' in _temp1_:
            sourelist = cmds.ls(cmds.polyListComponentConversion(sourelist, fv=1, fe=1, fuv=1 ,fvf=1, tf=1), fl=1)
        _list_ = ['%s.f[%s]' % (_TempObj_, i) 
                    for i in range(cmds.polyEvaluate(_TempObj_, f=1)) if not '%s.f[%s]' % (soureObj, i) in sourelist]
        cmds.delete(_list_)

        cmds.skinCluster(cmds.skinCluster(soureObj, q=1, inf=1), _TempObj_ ,tsb=True, dr=4)
        cmds.copySkinWeights(soureObj, _TempObj_, nm=1, sa='closestPoint', ia='oneToOne', nr=1)
        if not '.vtx[' in _temp2_:
            targelist = cmds.ls(cmds.polyListComponentConversion(targelist, ff=1, fe=1, fuv=1 ,fvf=1, tv=1), fl=1)
        #_list_ = [_TempObj_]
        #finalCopyList = _list_ + targelist   塞进列表第一位
        cmds.copySkinWeights(_TempObj_, targelist, nm=1, sa='closestPoint', ia=('name', 'closestJoint', 'oneToOne'), nr=1)
        cmds.delete(_TempObj_)
    
