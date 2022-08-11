# -*- coding: UTF-8 -*-
from maya import cmds, mel
import maya.OpenMaya as Om
import re


class cRivet():

    #Ver = 1.1

    def __init__(self, mode):
        slmesh = cmds.ls(sl=1, o=1, typ='mesh')
        slsurface = cmds.ls(sl=1, o=1, typ='nurbsSurface')
        if slmesh:
            twoEdge = cmds.filterExpand(sm=32)
            if len(twoEdge) != 2 or not twoEdge:
                Om.MGlobal.displayError(u'需要选择两条模型线')
                return
            nCFME1 = cmds.createNode('curveFromMeshEdge', n='rivetCFME01')
            cmds.setAttr('%s.ei[0]' %nCFME1, int(twoEdge[0].split('[')[1].split(']')[0]))
            cmds.connectAttr('%s.w' %slmesh[0], '%s.im' %nCFME1, f=1)
            nCFME2 = cmds.createNode('curveFromMeshEdge', n='rivetCFME02')
            cmds.setAttr('%s.ei[0]' %nCFME2, int(twoEdge[1].split('[')[1].split(']')[0]))
            cmds.connectAttr('%s.w' %slmesh[0], '%s.im' %nCFME2, f=1)
            nLoft = cmds.createNode('loft', n='rivetLoft01')
            cmds.setAttr('%s.u' %nLoft, 1)
            cmds.connectAttr('%s.oc' %nCFME1, '%s.ic[0]' %nLoft, f=1)
            cmds.connectAttr('%s.oc' %nCFME2, '%s.ic[1]' %nLoft, f=1)
            if mode == 'follicle':
                locN, locgrpN = self.cLoc(0)
                nFollicle = cmds.createNode('follicle', p=locgrpN, n='%s_FollicleShape' %locN)
                cmds.setAttr('%s.visibility' %nFollicle, 0)
                cmds.setAttr('%s.sim' %nFollicle, 0)
                cmds.connectAttr('%s.U' %locN, '%s.pu' %nFollicle, f=1)
                cmds.connectAttr('%s.V' %locN, '%s.pv' %nFollicle, f=1)
                cmds.connectAttr('%s.os' %nLoft, '%s.is' %nFollicle, f=1)
            else:
                locN, locgrpN = self.cLoc(0)
                nPOSI = cmds.createNode('pointOnSurfaceInfo', n='rivetPOSI01')
                cmds.setAttr('%s.top' %nPOSI, 1)
                cmds.connectAttr('%s.U' %locN, '%s.u' %nPOSI, f=1)
                cmds.connectAttr('%s.V' %locN, '%s.v' %nPOSI, f=1)
                cmds.connectAttr('%s.os' %nLoft, '%s.is' %nPOSI, f=1)
        elif slsurface:
            onepoint = cmds.filterExpand(sm=41)
            if len(onepoint) != 1 or not onepoint:
                Om.MGlobal.displayError(u'需要选择一个曲面点')
                return
            pointUV = re.findall(r'[[](.*?)[]]', onepoint[0])
            if mode == 'follicle':
                locN, locgrpN = self.cLoc(0, 1.0 / (cmds.getAttr('%s.mxu' %slsurface[0]) / float(pointUV[0])), 
                                                1.0 / (cmds.getAttr('%s.mxv' %slsurface[0]) / float(pointUV[1])))
                nFollicle = cmds.createNode('follicle', p=locgrpN, n='%s_FollicleShape' %locN)
                cmds.setAttr('%s.visibility' %nFollicle, 0)
                cmds.setAttr('%s.sim' %nFollicle, 0)
                cmds.connectAttr('%s.U' %locN, '%s.pu' %nFollicle, f=1)
                cmds.connectAttr('%s.V' %locN, '%s.pv' %nFollicle, f=1)
                cmds.connectAttr('%s.ws' %slsurface[0], '.is' %nFollicle, f=1)
            else:
                locN, locgrpN = self.cLoc(1, float(pointUV[0]), float(pointUV[1]))
                nPOSI = cmds.createNode('pointOnSurfaceInfo', n='rivetPOSI01')
                cmds.setAttr('%s.top' %nPOSI, 0)
                cmds.connectAttr('%s.U' %locN, '%s.u' %nPOSI, f=1)
                cmds.connectAttr('%s.V' %locN, '%s.v' %nPOSI, f=1)
                cmds.connectAttr('%s.ws' %slsurface[0], '%s.is' %nPOSI, f=1)
        else:
            Om.MGlobal.displayError(u'需要选择 模型线 或者 曲面点')
            return
        
        if mode == 'follicle':
            cmds.connectAttr('%s.ot' %nFollicle, '%s.t' %locgrpN, f=1)
            cmds.connectAttr('%s.or' %nFollicle, '%s.r' %locgrpN, f=1)
        elif mode == 'Matrix':
            if not cmds.pluginInfo('decomposeMatrix', q=1, l=1):
                cmds.loadPlugin('matrixNodes', quiet=1)
            nFBFM = cmds.createNode('fourByFourMatrix', n='rivetFBFM01')
            cmds.connectAttr('%s.nx' %nPOSI, '%s.in00' %nFBFM, f=1)
            cmds.connectAttr('%s.ny' %nPOSI, '%s.in01' %nFBFM, f=1)
            cmds.connectAttr('%s.nz' %nPOSI, '%s.in02' %nFBFM, f=1)
            cmds.connectAttr('%s.tux' %nPOSI, '%s.in10' %nFBFM, f=1)
            cmds.connectAttr('%s.tuy' %nPOSI, '%s.in11' %nFBFM, f=1)
            cmds.connectAttr('%s.tuz' %nPOSI, '%s.in12' %nFBFM, f=1)
            cmds.connectAttr('%s.tvx' %nPOSI, '%s.in20' %nFBFM, f=1)
            cmds.connectAttr('%s.tvy' %nPOSI, '%s.in21' %nFBFM, f=1)
            cmds.connectAttr('%s.tvz' %nPOSI, '%s.in22' %nFBFM, f=1)
            cmds.connectAttr('%s.px' %nPOSI, '%s.in30' %nFBFM, f=1)
            cmds.connectAttr('%s.py' %nPOSI, '%s.in31' %nFBFM, f=1)
            cmds.connectAttr('%s.pz' %nPOSI, '%s.in32' %nFBFM, f=1)
            nDM = cmds.createNode('decomposeMatrix', n='rivetDM01')
            cmds.connectAttr('%s.output' %nFBFM, '%s.inputMatrix' %nDM, f=1)
            cmds.connectAttr('%s.outputTranslate' %nDM, '%s.t' %locgrpN, f=1)
            cmds.connectAttr('%s.outputRotate' %nDM, '%s.r' %locgrpN, f=1)
        elif mode == 'Aim':
            nAimC = cmds.createNode('aimConstraint', p=locgrpN, n='%s_AimConstraint1' %locN)
            cmds.setAttr('%s.tg[0].tw' %nAimC, 1)
            cmds.setAttr('%s.a' %nAimC, 0, 1, 0, type='double3')
            cmds.setAttr('%s.u' %nAimC, 0, 0, 1, type='double3')
            cmds.connectAttr('%s.n' %nPOSI, '%s.tg[0].tt' %nAimC, f=1)
            cmds.connectAttr('%s.tv' %nPOSI, '%s.wu' %nAimC, f=1)
            cmds.connectAttr('%s.p' %nPOSI, '%s.t' %locgrpN, f=1)
            cmds.connectAttr('%s.cr' %nAimC, '%s.r' %locgrpN, f=1)

    def cLoc(self, mode, uV = .5, vV = .5):
        locName = 'rivet%s' %(len(cmds.ls('rivet*', typ='locator')) + 1)
        locN = cmds.spaceLocator(n=locName)[0]
        cmds.group(locN, n='%s_grp' %locN)
        if mode:
            cmds.addAttr(locN, ln='U', at='double', dv=0)
            cmds.addAttr(locN, ln='V', at='double', dv=0)
        else:
            cmds.addAttr(locN, ln='U', at='double', min=0, max=1, dv=0)
            cmds.addAttr(locN, ln='V', at='double', min=0, max=1, dv=0)
        cmds.setAttr('%s.U' %locN, e=1, keyable=1)
        cmds.setAttr('%s.U' %locN, uV)
        cmds.setAttr('%s.V' %locN, e=1, keyable=1)
        cmds.setAttr('%s.V' %locN, vV)
        return locN, '%s_grp' %locN

#cRivet('follicle')
