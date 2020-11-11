<h2 align="center"> Maya脚本更新日志 </h2>

<h3 align="center">  </h3>
<p align="center">

## [pTCIK `|动力学曲线工具|`](https://github.com/BlackC-Y/LearnCode/blob/LearnFlow/Maya_plugin/pTCIK.py)

#### 2020-11-02  Verision: `2.41`
    1.听大佬的话——精简多余代码
    2.Fix:Maya2016的Ui支持问题
    3.Fix:生成后直接删除控制器，不能再次运行的问题

#### 2020-10-23  Verision: `2.4`
    1.优化了窗口生成的方式，又学了一招嘿
    2.UI微调
    3.增加由骨骼控制曲线的选项
    4.整合了创建流程。但流程过长貌似不是好事，模块化会更好一些??
    5.选择控制器功能优化
    6.根据新的创建选项，重写了整理函数
    7.Fix:在关掉动力学时创建曲线，不生成shape的问题
    8.Note:不能用PointOnCurveInfo替换运动路径，没有方向的输出


## [WeightTool `|包含点调整.Save/Load.最大影响值检查|`](https://github.com/BlackC-Y/LearnCode/blob/LearnFlow/Maya_plugin/WeightTool.py)

#### 2020-10-21  Verision: `0.63`
    1.WeightTool: 骨骼列表实现层级或平铺，0权重显示过滤
    2.WeightCheckTool: Load性能优化
    3.WeightCheckTool: Select逻辑修改
    
#### 2020-09  Verision: `0.62`
    1.WeightTool: 骨骼列表刷新优化，刷新权重注释，不更改列表本身
    
    
## [CopyWeightTool `|拷贝权重工具|`](https://github.com/BlackC-Y/LearnCode/blob/LearnFlow/Maya_plugin/CopyWeightTool.py)

#### 2020-11-02  Verision: `1.1`
    1.在拷贝时保留权重锁
    2.Fix:一个不能运行的小问题

## [DataSaveUi `|临时储存物体或位置|`](https://github.com/BlackC-Y/LearnCode/blob/LearnFlow/Maya_plugin/DataSaveUi.py)

#### 2020-11-11  Verision: `1.11`
    1.Fix:临时物体没删除
    2.Fix:Get位置时会出现很大的偏移
    
#### 2020-11-11  Verision: `1.1`
    1.增加所选物体中心位置的储存
    2.Fix:Get时的判断逻辑
    
#### 2020-11-10  Verision: `1.0`
