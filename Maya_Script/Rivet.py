# -*- coding: UTF-8 -*-
from maya import cmds, mel
import maya.OpenMaya as Om
import re

cRivet__Verision = 1.0

def cRivet(mode):
    slmesh = cmds.ls(sl=1, o=1, typ='mesh')
    slsurface = cmds.ls(sl=1, o=1, typ='nurbsSurface')
    if slmesh:
        twoEdge = cmds.filterExpand(sm=32)
        if len(twoEdge) != 2:
            Om.MGlobal.displayError('Select (Two Mesh Edge)')
            return
        nCFME1 = cmds.createNode('curveFromMeshEdge', n='rivetCFME01')
        cmds.setAttr(nCFME1 + '.ei[0]', int(twoEdge[0].split('[')[1].split(']')[0]))
        cmds.connectAttr(slmesh[0] + '.w', nCFME1 + '.im', f=1)
        nCFME2 = cmds.createNode('curveFromMeshEdge', n='rivetCFME02')
        cmds.setAttr(nCFME2 + '.ei[0]', int(twoEdge[1].split('[')[1].split(']')[0]))
        cmds.connectAttr(slmesh[0] + '.w', nCFME2 + '.im', f=1)
        nLoft = cmds.createNode('loft', n='rivetLoft01')
        cmds.setAttr(nLoft + '.u', 1)
        cmds.connectAttr(nCFME1 + '.oc', nLoft + '.ic[0]', f=1)
        cmds.connectAttr(nCFME2 + '.oc', nLoft + '.ic[1]', f=1)
        if mode == 'follicle':
            locN, locgrpN = cLoc(0)
            nFollicle = cmds.createNode('follicle', p=locgrpN, n='%s_FollicleShape' %locN)
            cmds.setAttr(nFollicle + '.visibility', 0)
            cmds.setAttr(nFollicle + '.sim', 0)
            cmds.connectAttr(locN + '.U', nFollicle + '.pu', f=1)
            cmds.connectAttr(locN + '.V', nFollicle + '.pv', f=1)
            cmds.connectAttr(nLoft + '.os', nFollicle + '.is', f=1)
        else:
            locN, locgrpN = cLoc(0)
            nPOSI = cmds.createNode('pointOnSurfaceInfo', n='rivetPOSI01')
            cmds.setAttr(nPOSI + '.top', 1)
            cmds.connectAttr(locN + '.U', nPOSI + '.u', f=1)
            cmds.connectAttr(locN + '.V', nPOSI + '.v', f=1)
            cmds.connectAttr(nLoft + '.os', nPOSI + '.is', f=1)
    elif slsurface:
        onepoint = cmds.filterExpand(sm=41)
        if len(onepoint) != 1:
            Om.MGlobal.displayError('Select (One nurbsSurface Point)')
            return
        pointUV = re.findall(r'[[](.*?)[]]', onepoint[0])
        if mode == 'follicle':
            locN, locgrpN = cLoc(0, 1.0 / (cmds.getAttr('%s.mxu' %slsurface[0]) / float(pointUV[0])), 1.0 / (cmds.getAttr('%s.mxv' %slsurface[0]) / float(pointUV[1])))
            nFollicle = cmds.createNode('follicle', p=locgrpN, n='%s_FollicleShape' %locN)
            cmds.setAttr(nFollicle + '.visibility', 0)
            cmds.setAttr(nFollicle + '.sim', 0)
            cmds.connectAttr(locN + '.U', nFollicle + '.pu', f=1)
            cmds.connectAttr(locN + '.V', nFollicle + '.pv', f=1)
            cmds.connectAttr(slsurface[0] + '.ws', nFollicle + '.is', f=1)
        else:
            locN, locgrpN = cLoc(1, float(pointUV[0]), float(pointUV[1]))
            nPOSI = cmds.createNode('pointOnSurfaceInfo', n='rivetPOSI01')
            cmds.setAttr(nPOSI + '.top', 0)
            cmds.connectAttr(locN + '.U', nPOSI + '.u', f=1)
            cmds.connectAttr(locN + '.V', nPOSI + '.v', f=1)
            cmds.connectAttr(slsurface[0] + '.ws', nPOSI + '.is', f=1)
    else:
        Om.MGlobal.displayError('Select (Mesh Edge) or (nurbsSurface Point)')
        return
    if mode == 'follicle':
        cmds.connectAttr(nFollicle + '.ot', locgrpN + '.t', f=1)
        cmds.connectAttr(nFollicle + '.or', locgrpN + '.r', f=1)
    elif mode == 'Matrix':
        if not cmds.pluginInfo('decomposeMatrix', q=1, l=1):
            cmds.loadPlugin('matrixNodes', quiet=1)
        nFBFM = cmds.createNode('fourByFourMatrix', n='rivetFBFM01')
        cmds.connectAttr(nPOSI + '.nx', nFBFM + '.in00', f=1)
        cmds.connectAttr(nPOSI + '.ny', nFBFM + '.in01', f=1)
        cmds.connectAttr(nPOSI + '.nz', nFBFM + '.in02', f=1)
        cmds.connectAttr(nPOSI + '.tux', nFBFM + '.in10', f=1)
        cmds.connectAttr(nPOSI + '.tuy', nFBFM + '.in11', f=1)
        cmds.connectAttr(nPOSI + '.tuz', nFBFM + '.in12', f=1)
        cmds.connectAttr(nPOSI + '.tvx', nFBFM + '.in20', f=1)
        cmds.connectAttr(nPOSI + '.tvy', nFBFM + '.in21', f=1)
        cmds.connectAttr(nPOSI + '.tvz', nFBFM + '.in22', f=1)
        cmds.connectAttr(nPOSI + '.px', nFBFM + '.in30', f=1)
        cmds.connectAttr(nPOSI + '.py', nFBFM + '.in31', f=1)
        cmds.connectAttr(nPOSI + '.pz', nFBFM + '.in32', f=1)
        nDM = cmds.createNode('decomposeMatrix', n='rivetDM01')
        cmds.connectAttr(nFBFM + '.output', nDM + '.inputMatrix', f=1)
        cmds.connectAttr(nDM + '.outputTranslate', locgrpN + '.t', f=1)
        cmds.connectAttr(nDM + '.outputRotate', locgrpN + '.r', f=1)
    elif mode == 'Aim':
        nAimC = cmds.createNode('aimConstraint', p=locgrpN, n='%s_AimConstraint1' %locN)
        cmds.setAttr(nAimC + '.tg[0].tw', 1)
        cmds.setAttr(nAimC + '.a', 0, 1, 0, type='double3')
        cmds.setAttr(nAimC + '.u', 0, 0, 1, type='double3')
        cmds.connectAttr(nPOSI + '.n', nAimC + '.tg[0].tt', f=1)
        cmds.connectAttr(nPOSI + '.tv', nAimC + '.wu', f=1)
        cmds.connectAttr(nPOSI + '.p', locgrpN + '.t', f=1)
        cmds.connectAttr(nAimC + '.cr', locgrpN + '.r', f=1)

def cLoc(mode, uV = .5, vV = .5):
    locName = 'rivet%s' % (len(cmds.ls('rivet*', typ='locator')) + 1)
    locN = cmds.spaceLocator(n=locName)[0]
    cmds.group(locN, n=locN + '_grp')
    if mode:
        cmds.addAttr(locN, ln='U', at='double', dv=0)
        cmds.addAttr(locN, ln='V', at='double', dv=0)
    else:
        cmds.addAttr(locN, ln='U', at='double', min=0, max=1, dv=0)
        cmds.addAttr(locN, ln='V', at='double', min=0, max=1, dv=0)
    cmds.setAttr(locN + '.U', e=1, keyable=1)
    cmds.setAttr(locN + '.U', uV)
    cmds.setAttr(locN + '.V', e=1, keyable=1)
    cmds.setAttr(locN + '.V', vV)
    #for i in ['.tx', '.ty', '.tz', '.rx', '.ry', '.rz', '.sx', '.sy', '.sz']:
    #    cmds.setAttr(locN + i, lock=1)
    return locN, locN + '_grp'

cRivet('follicle')
