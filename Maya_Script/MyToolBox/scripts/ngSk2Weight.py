# -*- coding: UTF-8 -*-
'''Roadmap: 一个创建/修改模板的界面
'''
from maya import cmds, mel
from maya.api import OpenMaya as om, OpenMayaAnim as omAni
#from .RecordLog_Maya import *
import json
import os
try:
    import ngSkinTools2.api as ng2api
except:
    pass


class ngSk2Weight_BbBB():

    def ToolUi(self):
        if not self.pluginCheck():
            return
        Ver = 0.1
        self.Ui = 'ngSk2Weight_Ui'
        if cmds.window(self.Ui, q=1, ex=1):
            cmds.deleteUI(self.Ui)
        cmds.window(self.Ui, t='ngSk2Weight Beta1', rtf=1, mb=1, tlb=1, wh=(240, 118))
        cmds.columnLayout('%s_MainCL' %self.Ui, cat=('both', 2), rs=1, cw=230, adj=1)
        cmds.optionMenu('%s_TemplateMenu' %self.Ui, l=u'选择模板', mvi=6)
        self.DataLoc = '%s/MyToolBoxDir/Data/ngSk2Weight/' %os.getenv('ALLUSERSPROFILE')
        if os.path.isdir(self.DataLoc):
            fileList = os.listdir(self.DataLoc)
            if fileList:
                for i in fileList:
                    fileSplit = i.rsplit('.')
                    if fileSplit[1] == 'json':
                        cmds.menuItem(l=fileSplit[0])
        
        cmds.rowLayout(nc=2, h=28)
        cmds.checkBox('%s_assignMaxInfluencesCB' %self.Ui, l=u'最大影响值', v=1)
        cmds.intField('%s_assignMaxInfluencesNum' %self.Ui, v=8)
        cmds.setParent('..')
        cmds.button(l=u'运行', c=lambda *args: self.doIt())
        cmds.popupMenu()
        cmds.menuItem('%s_objHaveSkin' %self.Ui, cb=0, l=u'模型已有蒙皮')
        cmds.separator(h=10)
        cmds.button('%s_foldSwitch' %self.Ui, l=u'Smooth △', c=lambda *args: self.foldSmoothPage())
        cmds.showWindow(self.Ui)
        cmds.window(self.Ui, e=1, rtf=1, wh=(240, 118))

    def pluginCheck(self):
        try:
            cmds.loadPlugin('ngSkinTools2', qt=1)
            import ngSkinTools2.api as ng2api
        except (RuntimeError, ImportError):
            om.MGlobal.displayError(u'这个Maya中缺少ng2插件, 无法使用!')
            return 0
        return 1

    def foldSmoothPage(self):
        if cmds.button('%s_foldSwitch' %self.Ui, q=1, l=1) == u'Smooth ▽':
            cmds.deleteUI('%s_smoothRCL' %self.Ui, lay=1)
            cmds.button('%s_foldSwitch' %self.Ui, e=1, l=u'Smooth △')
            cmds.window(self.Ui, e=1, rtf=1, wh=(240, 118))
        else:
            sllist = cmds.ls(sl=1)
            if not sllist:
                om.MGlobal.displayError(u'什么都没选, 做咩啊')
                return
            clusterName = mel.eval('findRelatedSkinCluster("%s")' %sllist[0])
            if not clusterName:
                om.MGlobal.displayError(u'模型上没得蒙皮, 做咩啊')
                return
            ngLayerData = cmds.listConnections('%s.message' %clusterName, d=1, t='ngst2SkinLayerData')
            if not ngLayerData:
                om.MGlobal.displayError(u'模型上没用过ng, smooth功能不可用')
                return
            objLayers = ng2api.Layers(clusterName)
            objAllLayer = objLayers.list()
            cmds.rowColumnLayout('%s_smoothRCL' %self.Ui, nc=2, cs=(2, 2), rs=(1, 2), w=240, p='%s_MainCL' %self.Ui)
            cmds.radioCollection('%s_smoothLayerRC' %self.Ui)
            for i in objAllLayer:
                if i.name == 'assignBase' or not max(self.get_LayerWeights(i, 'mask')):
                    continue
                cmds.radioButton(l=i.name, h=22)
                cmds.radioButton(l=u'%s子骨骼' %i.name, h=22)
            cmds.button(l=u'< 反Smooth', h=25, c=lambda *args: self.floodLayerWeight(0, objAllLayer))
            cmds.button(l=u'Smooth >', h=25, c=lambda *args: self.floodLayerWeight(1, objAllLayer))
            cmds.checkBox('%s_floodMaxInfluencesCB' %self.Ui, h=25, l=u'最大影响值', v=cmds.checkBox('%s_assignMaxInfluencesCB' %self.Ui, q=1, v=1))
            cmds.intField('%s_floodMaxInfluencesNum' %self.Ui, h=25, v=cmds.intField('%s_assignMaxInfluencesNum' %self.Ui, q=1, v=1))
            #cmds.checkBox('%s_limitSelectComponentCB' %self.Ui, l=u'只影响选中的点', v=0)
            cmds.button(l=u'镜像权重', h=25, c=lambda *args: self.mirrorLayerWeight(clusterName, objAllLayer))
            cmds.button('%s_foldSwitch' %self.Ui, e=1, l=u'Smooth ▽')
        
    def floodLayerWeight(self, mode, objAllLayer):
        slLayer = cmds.radioButton(cmds.radioCollection('%s_smoothLayerRC' %self.Ui, q=1, sl=1), q=1, l=1)
        FloodSettings = ng2api.FloodSettings()
        FloodSettings.influences_limit = cmds.intField('%s_floodMaxInfluencesNum' %self.Ui, q=1, v=1) if cmds.checkBox('%s_floodMaxInfluencesCB' %self.Ui, q=1, v=1) else 0
        #FloodSettings.limit_to_component_selection = cmds.checkBox('%s_limitSelectComponentCB' %self.Ui, q=1, v=1)
        if mode:
            FloodSettings.mode = ng2api.paint.PaintMode.smooth
            FloodSettings.intensity = 0.8
            FloodSettings.iterations = 2
        else:
            FloodSettings.mode = ng2api.paint.PaintMode.sharpen
            FloodSettings.intensity = 0.1
        '''
        mode = None                              #工具模式 api.paint.PaintMode.xxx(int 1-5)
        intensity = 1.0                          #工具强度
        iterations = 1                           #重复次数
        influences_limit = 0                     #最大影响值限制
        mirror = False                           #是否镜像
        fixed_influences_per_vertex = False      #只影响当前点上的骨骼，不扩大影响
        distribute_to_other_influences = False   #削减的权重是否分配到其他骨骼
        limit_to_component_selection = False     #只影响选中的组件
        use_volume_neighbours = False
        '''
        if u'子骨骼' in slLayer:
            for i in objAllLayer:
                if i.name == slLayer.rsplit(u'子骨骼')[0]:
                    break
            ng2api.flood_weights(i, settings=FloodSettings)
        else:
            for i in objAllLayer:
                if i.name == slLayer:
                    break
            ng2api.flood_weights(i, 'mask', FloodSettings)
    
    def mirrorLayerWeight(self, clusterName, objAllLayer):
        mirror_options = ng2api.MirrorOptions()
        mirror_options.direction = ng2api.MirrorOptions.directionPositiveToNegative
        for i in objAllLayer:
            cmds.ngst2Layers(clusterName, id=i.index, mirrorLayerWeights=1, mirrorLayerMask=1, mirrorLayerDq=1, mirrorDirection=ng2api.MirrorOptions.directionPositiveToNegative)
        
    def createTemplate(self):
        pass
        """
        import json
        jsonDirt = {
            'Mirror': '_L/_R', 
            'RootJoint': 'Root_M',
            "LayersOrder": ["Body", "Hip", "Knee", "Foot", "Scapula", "Shoulder", "Elbow", "Hand", "IndexFinger", "MiddleFinger", "RingFinger", "PinkyFinger", "ThumbFinger", "Neck", "Head"],
            "WeightOrder": [["Hip", "Knee", "Foot"], ["Scapula", "Shoulder", "Elbow", "Hand", {"Finger": ["IndexFinger", "MiddleFinger", "RingFinger", "PinkyFinger", "ThumbFinger"]}], ["Neck", "Head"]],
            'Layers': {
                "Body": ["Root_M","RootPart*_M","Spine*_M","Spine*Part*_M","Chest_M"],
                "Hip": ["Hip_L","HipPart*_L"],
                "Knee": ["Knee_L","KneePart*_L"],
                "Foot": ["Ankle_L","Toes_L"],
                "Scapula": ["Scapula_L"],
                "Shoulder": ["Shoulder_L","ShoulderPart*_L"],
                "Elbow": ["Elbow_L","ElbowPart*_L"],
                "Hand": ["Wrist_L","Cup_L"],
                "IndexFinger": ["IndexFinger1_L","IndexFinger2_L","IndexFinger3_L"],
                "MiddleFinger": ["MiddleFinger1_L","MiddleFinger2_L","MiddleFinger3_L"],
                "RingFinger": ["RingFinger1_L","RingFinger2_L","RingFinger3_L"],
                "PinkyFinger": ["PinkyFinger1_L","PinkyFinger2_L","PinkyFinger3_L"],
                "ThumbFinger": ["ThumbFinger1_L","ThumbFinger2_L","ThumbFinger3_L"],
                "Neck": ["Neck_M","NeckPart*_M"],
                "Head": ["Head_M"]
            },
            'IssueJoint': ['Cup_L']
        }

        with open('%s/%s.json' %('C:/Users/BlackC_Desk/Desktop/ts', 'aaa'), 'w') as jsFile:
            json.dump(jsonDirt, jsFile, indent=4)   #sort_keys=1 排序

        with open('%s/%s.json' %('C:/Users/BlackC_Desk/Desktop/ts/', 'aaa'), 'r') as jsFile:
            readData = json.load(jsFile)
            print(type(readData["WeightOrder"][1][-1]))
            print({}.__class__)
        """

    def doIt(self):
        filePath = os.path.normpath('%s%s.json' %(self.DataLoc, cmds.optionMenu('%s_TemplateMenu' %self.Ui, q=1, v=1)))
        if not os.path.isfile(filePath):
            om.MGlobal.displayError(u'选择的模板不存在')
            return
        sllist = cmds.ls(sl=1, typ='transform')
        if not sllist:
            om.MGlobal.displayError(u'什么都没选, 做咩啊')
            return
        objHaveSkin = cmds.menuItem('%s_objHaveSkin' %self.Ui, q=1, cb=1)
        clusterName = mel.eval('findRelatedSkinCluster("%s")' %sllist[0])
        if clusterName and not objHaveSkin:
            om.MGlobal.displayError(u'模型已经有蒙皮了, 请检查')
            return
        elif not clusterName and objHaveSkin:
            om.MGlobal.displayError(u'模型上没有蒙皮, 请检查')
            return

        with open(filePath, "r") as jsFile:
            self.TemplateData = json.loads(jsFile.read())
        jsRootJoint = self.TemplateData['RootJoint']
        if not cmds.ls(jsRootJoint, typ='joint'):
            om.MGlobal.displayError(u'没找到指定的根骨骼, 当前骨架跟选择模板不匹配')
            return
        cmds.select(jsRootJoint, hi=1)
        cmds.select(cmds.ls(sl=1, type='joint'), r=1)
        self.stuffJointList()
        heatMapLayer = None
        if not objHaveSkin:
            heatMapLayer = self.bindSkin(sllist[0])
            clusterName = mel.eval('findRelatedSkinCluster("%s")' %sllist[0])
        self.assignJointWeight(clusterName)
        self.replaceIssueJoint(heatMapLayer)
        self.setLayersMask(heatMapLayer)
        self.layersFloodWeight()
        cmds.select(sllist, r=1)
        
    def stuffJointList(self):
        #入参
        jsonLayers = self.TemplateData['Layers']
        mirror = self.TemplateData['Mirror']
        
        mirror = mirror.split('/') if '/' in mirror else 0
        stuffLayers = {}

        def multipleSplit(rangeName):
            if mirror and mirror[0] in joint:
                for i in cmds.ls(rangeName, sl=1):
                    stuffLayers[item][0].append(i)
                    stuffLayers[item][1].append(i.replace(mirror[0], mirror[1]))
            else:
                for i in cmds.ls(rangeName, sl=1):
                    stuffLayers[item][0].append(i)

        for item in jsonLayers:
            stuffLayers[item] = [[], []]
            for joint in jsonLayers[item]:
                split = joint.split('*')
                if len(split) == 1:
                    if cmds.ls(joint, sl=1):
                        stuffLayers[item][0].append(joint)
                        if mirror and mirror[0] in joint:
                            stuffLayers[item][1].append(joint.replace(mirror[0], mirror[1])) 
                elif len(split) == 2:
                    multipleSplit(['%s%s%s' %(split[0], n, split[1]) for n in range(40)])
                elif len(split) == 3:
                    multipleSplit(['%s%s%s%s%s' %(split[0], n1, split[1], n2, split[2]) for n2 in range(40) for n1 in range(40)])
                elif len(split) == 4:
                    multipleSplit(['%s%s%s%s%s%s%s' %(split[0], n1, split[1], n2, split[2], n3, split[3]) 
                                    for n3 in range(20) for n2 in range(20) for n1 in range(20)])
                elif len(split) == 5:
                    multipleSplit(['%s%s%s%s%s%s%s%s%s' %(split[0], n1, split[1], n2, split[2], n3, split[3], n4, split[4]) 
                                    for n4 in range(20) for n3 in range(20) for n2 in range(20) for n1 in range(20)])
        #出参
        self.TemplateData['LayersStuff'] = stuffLayers

    def bindSkin(self, slobj):
        #入参
        jsonLayers = self.TemplateData['LayersStuff']

        heatMapSkinMesh = cmds.duplicate(slobj, rr=1, n="__tempHeatMapSkin__Mesh")[0]
        assignJointList = []
        for key, value in jsonLayers.items():
            assignJointList += value[0] + value[1]
        cmds.skinCluster(assignJointList, slobj, tsb=1, dr=4)
        try:
            cmds.skinCluster(assignJointList, heatMapSkinMesh, tsb=1, bm=2, hmf=0.8, mi=1)
        except RuntimeError as Argument:
            if Argument.args[0] == 'Maya command error':   #报错信息
                cmds.delete(heatMapSkinMesh)
                om.MGlobal.displayWarning(u'此模型不支持热度贴图蒙皮, 将使用备用方案, 最终效果可能会降低')
                return None
        else:   #无异常时执行
            clusterName = mel.eval('findRelatedSkinCluster("%s")' %heatMapSkinMesh)
            layers = ng2api.init_layers(clusterName)
            return layers.add("heatMap")
        
    def assignJointWeight(self, skinCluster):
        #入参
        jsonLayers = self.TemplateData['LayersStuff']
        jsonLayersOrder = self.TemplateData['LayersOrder']

        layers = ng2api.init_layers(skinCluster)
        #layers = ng2api.Layers("")   #已存在数据层的skinCluster
        layerList = [layers.add("assignBase")]
        layerJointPathIndex = ng2api.target_info.list_influences(skinCluster)   #获取骨骼在数据层内的信息
        ngPath_Index = []
        for i in layerJointPathIndex:
            ngPath_Index.append(i.path.rsplit('|', 1)[1])   #path 完整路径
            ngPath_Index.append(i.logicalIndex)   #logicalIndex 层内顺序
        for i in jsonLayersOrder:
            jointInLayerIndex = []
            layerList.append(layers.add(i))
            for joint in jsonLayers[i][0]:   #jsonLayers数据结构为'LayerName': [[Joint], [JointMirror]]
                jointInLayerIndex.append(ngPath_Index[ngPath_Index.index(joint) + 1])   #查询层内骨骼的对应编号
            ng2api.assign_from_closest_joint(skinCluster, layerList[-1], jointInLayerIndex)   #分权重
        ng2api.flood_weights(layerList[1], influence='mask')
        #Base层分权重
        ng2api.assign_from_closest_joint(skinCluster, layerList[0], ngPath_Index[1::2])

        #出参
        self.TemplateData['ngLayerList'] = layerList
        self.ngPath_Index = ngPath_Index

    def replaceIssueJoint(self, heatMapLayer):
        #入参
        ngPath_Index = self.ngPath_Index
        layerList = self.TemplateData['ngLayerList']
        jsonLayers = self.TemplateData['LayersStuff']
        jsonIssueJoint = self.TemplateData['IssueJoint']
        jsonLayersOrder = self.TemplateData['LayersOrder']
        
        for i in jsonIssueJoint:
            for key, value in jsonLayers.items():
                if i in value[0]:
                    layerIndex = jsonLayersOrder.index(key) + 1
                    jointIndex = ngPath_Index[ngPath_Index.index(i) + 1]
                    if heatMapLayer:
                        layerList[layerIndex].set_weights(jointIndex, self.get_LayerWeights(heatMapLayer, jointIndex), undo_enabled=0)
                    else:
                        layerList[layerIndex].set_weights(jointIndex, self.get_LayerWeights(layerList[0], jointIndex), undo_enabled=0)
                    ng2api.tools.fill_transparency(layerList[layerIndex])
                    break
        
    def setLayersMask(self, heatMapLayer):
        #入参
        layerList = self.TemplateData['ngLayerList']
        jsonLayersOrder = self.TemplateData['LayersOrder']
        jsonWeightOrder = self.TemplateData['WeightOrder']

        #vertexNum = cmds.polyEvaluate(v=1) 获取模型点数
        def addListValue(inWeight):
            _addWeightList = []   #[0] *Num 创建指定数值列表
            for i in inWeight:
                _addWeightList = [v1 + v2 for v1, v2 in zip(_addWeightList, i)] if _addWeightList else i
            return _addWeightList

        def addLayerValue(layerIndex):   #累加指定层内所有骨骼权重
            _layerJointNum = layerList[layerIndex].get_used_influences()
            if heatMapLayer:   #如有热度蒙皮，则取热度蒙皮权重，最后一根骨骼用ng权重进行过滤
                _addHeatMapWeightList = []
                for indexList, index in enumerate(_layerJointNum):
                    if len(_layerJointNum) == 1: #如果本层只有一个骨骼 -> 且该骨骼没有权重，则返回Base层的权重
                        return self.get_LayerWeights(layerList[0], index) if not max(self.get_LayerWeights(heatMapLayer, index)) else \
                                                                                        self.get_LayerWeights(heatMapLayer, index)
                    if indexList == len(_layerJointNum) - 1:   #最后一个骨骼 进行权重整理
                        # 如果v3(Base层)有权重 > 而且v1(此层已循环骨骼的热度贴图权重之和)或v2(此层当前骨骼的热度贴图权重)之中有一个是有权重的，则这个点在范围内
                        # 如果v3(Base层)没有权重, 但v1是有权重的, 则这个点在范围内
                        # 如果v3(Base层)没有权重, 而且v1也没有权重, 则这个点不在范围内
                        _addHeatMapWeightList = [1 if v3 and v1 or v2 else 1 if v1 else 0 for v1, v2, v3 in 
                                zip(_addHeatMapWeightList, self.get_LayerWeights(heatMapLayer, index), self.get_LayerWeights(layerList[0], index))]
                    else:
                        _addHeatMapWeightList = [v1 + v2 for v1, v2 in zip(_addHeatMapWeightList, self.get_LayerWeights(heatMapLayer, index))] \
                                                                    if _addHeatMapWeightList else self.get_LayerWeights(heatMapLayer, index)   #相同代码 减少占用
                return _addHeatMapWeightList
            else:
                _addngWeightList = []
                for indexList, index in enumerate(_layerJointNum):
                    _addngWeightList = [v1 + v2 for v1, v2 in zip(_addngWeightList, self.get_LayerWeights(layerList[0], index))] if _addngWeightList else \
                                                                                    self.get_LayerWeights(layerList[0], index)   #相同代码 减少占用
                return _addngWeightList

        for l1 in reversed(jsonWeightOrder):   #肢体块
            saveLayerWeight = []
            for l2 in reversed(l1):   #层
                if type(l2) == {}.__class__:   #层里有字典(手指为平级)
                    saveChildLayerWeight = []
                    for l3 in l2["Finger"]:
                        layerIndex = jsonLayersOrder.index(l3) + 1   #获取当前循环层在ng层中的编号
                        saveWeight = addLayerValue(layerIndex)
                        layerList[layerIndex].set_weights('mask', saveWeight, undo_enabled=0)
                        saveChildLayerWeight.append(saveWeight)
                    saveLayerWeight.append(addListValue(saveChildLayerWeight))
                    continue
                layerIndex = jsonLayersOrder.index(l2) + 1   #获取当前循环层在ng层中的编号
                saveWeight = addLayerValue(layerIndex)
                if not saveLayerWeight:
                    layerList[layerIndex].set_weights('mask', saveWeight, undo_enabled=0)
                    saveLayerWeight.append(saveWeight)
                else:
                    saveLayerWeight.append(saveWeight)
                    layerList[layerIndex].set_weights('mask', addListValue(saveLayerWeight), undo_enabled=0)

        if heatMapLayer:
            cmds.delete(cmds.listRelatives(cmds.skinCluster(heatMapLayer.mesh, q=1, g=1), p=1))

    def get_LayerWeights(self, Layer, influence):
        return mel.eval("ngst2Layers -id {id} -paintTarget {index} -q -{arg} {mesh}".format(mesh=Layer.mesh, id=Layer.id, index=influence, arg='vertexWeights'))

    def layersFloodWeight(self):
        #入参
        layerList = self.TemplateData['ngLayerList']
        jsonLayers = self.TemplateData['LayersStuff']

        omList = om.MGlobal.getSelectionListByName(layerList[0].mesh)   #skinCluster
        skinMObject = omList.getDependNode(0)
        skinNode = omAni.MFnSkinCluster(skinMObject)
        allJointDagPath = skinNode.influenceObjects()
        skCluInfo = []
        for i in allJointDagPath:
            pointList, weigthList = skinNode.getPointsAffectedByInfluence(i)
            if pointList.length():
                pointDagPath, pointObject = pointList.getComponent(0)
                vertex_MIt = om.MItMeshVertex(pointDagPath, pointObject)
                skCluInfo.append(i.partialPathName())
                skCluInfo.append(vertex_MIt.count())
                """
                while not vertex_MIt.isDone():
                    print(vertex_MIt.index())
                    vertex_MIt.next()
                """
            else:
                skCluInfo.append(i.partialPathName())
                skCluInfo.append(0)
        FloodSettings = ng2api.FloodSettings()
        FloodSettings.mode = ng2api.paint.PaintMode.smooth
        FloodSettings.intensity = 0.8
        FloodSettings.influences_limit = cmds.intField('%s_assignMaxInfluencesNum' %self.Ui, q=1, v=1) if cmds.checkBox('%s_assignMaxInfluencesCB' %self.Ui, q=1, v=1) else 0
        for i in layerList[1:]:
            Num = 0
            for joint in reversed(jsonLayers[i.name][0]):   #jsonLayers数据结构为'LayerName': [[Joint], [JointMirror]]
                Num += skCluInfo[skCluInfo.index(joint) + 1]
            FloodSettings.iterations = 1 if Num < 60 else int(Num / 60)
            ng2api.flood_weights(i, settings=FloodSettings)
            lastJoint = skCluInfo[skCluInfo.index(joint) + 1]
            FloodSettings.iterations = 1 if lastJoint < 40 else int(lastJoint / 40)
            ng2api.flood_weights(i, 'mask', FloodSettings)

    
#ngSk2Weight_BbBB().ToolUi()
