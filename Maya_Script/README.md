<h2 align="center"> Maya脚本更新日志 </h2>

<h3 align="center">  </h3>
<p align="center">

## [cur2IK_FX `|动力学曲线工具|`](https://github.com/BlackC-Y/LearnCode/blob/LearnFlow/Maya_Script/cur2IK_FX.py)

#### 2020-12-09  Verision: `2.5x`
<details>
<summary>详情</summary>
<pre>
1.添加新的流程, 从骨骼开始建立
2.所有流程增加蒙皮骨骼作为最终结果
3.隐藏不需要的物体和属性
4.改用驱动关键帧对动力学开关进行控制
  (若动力学开启, 在2019和更高版本中, 会因为cache playbacka功能会引起崩溃)
5.清理冗余代码, 提升效率
6.修改Ui部件名，确保Ui的唯一性
7.Fix: 选择控制器时对名字的错误拆分
8.Fix: 插件报错后，错误信息不消失
<p align="left">
  ▽  2020-12-25  Ver_2.51
1.修改ui部件名, 与脚本的新名字保持一致
2.用刷新替代延迟运行，避免出错
</pre>
</details>

#### 2020-10-23  Verision: `2.4x`
<details>
<summary>详情</summary>
<pre>
1.优化了窗口生成的方式, 又学了一招
2.UI微调
3.增加由骨骼控制曲线的选项
4.整合了创建流程. 但流程过长貌似不是好事, 模块化会更好一些??
5.选择控制器功能优化
6.根据新的创建选项，重写了整理函数
7.Fix: 在关掉动力学时创建曲线, 不生成shape的问题
<p align="left">
  ▽  2020-11-02  Ver_2.41
1.精简多余代码
2.Fix: Maya2016的Ui支持问题
3.Fix: 生成后直接删除控制器, 不能再次运行的问题
<p align="left">
  ▽  2020-11-20  Ver_2.42
1.Fix: 提取曲线时, 尝试居中对齐会报错
</pre>
</details>


## [WeightTool `|包含点调整.Save/Load.最大影响值检查|`](https://github.com/BlackC-Y/LearnCode/blob/LearnFlow/Maya_Script/WeightTool.py)

#### 2020-12-24  Verision: `0.8x`
<details>
<summary>详情</summary>
<pre>
1.增加 Api2.0 处理权重, 同时默认使用Api2.0
  --Api2.0 只能处理Mesh模型
2.添加右键菜单中的功能
3.运行效率优化, 代码优化
4.Fix: 在空白处右键, 不会弹出菜单的问题
5.Fix: Api获取蒙皮节点时, 会误判, 改为mel调用获取
<p align="left">
  ▽  2020-12-25  Ver_0.81
1.使用Api Load权重时, 避免使用eval处理数据，改用字符串处理获取数据
2.继续优化代码
3.Fix: 脚本功能不运行时, 选择骨骼列表会报错
<p align="left">
  ▽  2020-12-25  Ver_0.82
1.修改Ui部件名, 确保Ui的唯一性
2.Fix: 权重锤运行时报错
<p align="left">
  ▽  2021-01-04  Ver_0.83
1.Fix: 触发脚本时不会立刻运行的问题
2.Fix: 列表刷新时, 骨骼锁没被刷新的问题
<p align="left">
  ▽  2021-01-07  Ver_0.84
1.Fix: 给模型添加影响后, 骨骼列表不会刷新的问题. 可能导致报错
2.Fix: copy权重后会触发刷新, 此时的选择列表可能有问题, 导致报错
3.Fix: 删除搜索栏字符后, 骨骼列表不刷新的问题在2016以上版本中不存在
</pre>
</details>

#### 2020-11-26  Verision: `0.7x`
<details>
<summary>详情</summary>
<pre>
1.增加了api处理权重功能, 但默认使用Mel
2.使用并集、差集优化循环处理方式
3.修改文件选择窗口的实现方式
4.减小Save功能的权重精度, 控制在小数点后4位
5.使用重蒙皮时, 更新初始的绑定Pose
6.Fix: 刷新时选择中有transform, 不能获取权重的报错
7.Fix: 在空白处右键菜单获取物体为空, 导致的报错
8.Fix: Save点权重时因为缺少物体而报错
9.Fix: Load权重时因为有权重锁, 可能导致设置权重失败
<p align="left">
  ▽  2020-11-26  Ver_0.81
1.Fix: 晶格、曲线、曲面的权重调整功能修复
2.Fix: 使用api Load点权重时，权重完成了点还在循环判断，会报错
</pre>
</details>

#### 2020-09  Verision: `0.6x`
<details>
<summary>详情</summary>
<pre>
1.骨骼列表刷新优化, 刷新权重注释, 不更改列表本身
<p align="left">
  ▽  2020-10-21  Ver_0.63
1.骨骼列表实现层级或平铺, 0权重显示过滤
2.WeightCheckTool: Load性能优化
3.WeightCheckTool: Select逻辑修改
</pre>
</details>


## [CopyWeightTool `|拷贝权重工具|`](https://github.com/BlackC-Y/LearnCode/blob/LearnFlow/Maya_Script/CopyWeightTool.py)

#### 2020-12-29  Verision: `1.3x`
<details>
<summary>详情</summary>
<pre>
1. 增加向未蒙皮物体拷贝权重的功能
2. 优化流程, 优化代码
3. Fix: 源组件为物体时, 没有可删除的内容会报黄
4. Fix: 源组件没有蒙皮时报错
<p align="left">
  ▽  2020-12-31  Ver_1.31
1.增加向多个未蒙皮物体拷贝权重的功能
</pre>
</details>

#### 2020-11-30  Verision: `1.2`
<details>
<summary>详情</summary>
<pre>
1.更改数据读取方式, 不再使用Py的eval, 可能导致Maya发生循环错误
</pre>
</details>

#### 2020-11-02  Verision: `1.1`
<details>
<summary>详情</summary>
<pre>
1.在拷贝时保留权重锁
2.Fix: 一个不能运行的小问题
</pre>
</details>


## [DataSaveUi `|临时储存物体或位置|`](https://github.com/BlackC-Y/LearnCode/blob/LearnFlow/Maya_Script/DataSaveUi.py)

#### 2020-11-30  Verision: `1.2`
<details>
<summary>详情</summary>
<pre>
1.更改数据读取方式, 不再使用Py的eval, 可能导致Maya发生循环错误
2.Fix: 获取位置时, 选择为空没有及时停止运行
</pre>
</details>

#### 2020-11-11  Verision: `1.1x`
<details>
<summary>详情</summary>
<pre>
1.增加所选物体中心位置的储存
2.Fix: Get时的判断逻辑
3.Fix: 临时物体没删除
<p align="left">
  ▽  2020-11-11  Ver_1.12
1.Fix: Get位置时会出现很大的偏移, 全部使用约束定位, 命令对空间的转换有问题
</pre>
</details>

#### 2020-11-10  Verision: `1.0`


## [PSDshape `|辅助PSD修型工具|`](https://github.com/BlackC-Y/LearnCode/blob/LearnFlow/Maya_Script/PSDshape.py)

#### 2021-02-04  Verision: `0.8`
<details>
<summary>详情</summary>
<pre>
1.新工具
</pre>
</details>