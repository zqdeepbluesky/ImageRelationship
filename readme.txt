代码结构介绍：
ModifyFileforVOC2017/文件夹内包含对py-faster-rcnn进行修改的所有脚本,详见该文件夹下readme.txt文件
Tools/内是一些对图像进行预处理，生成图像集的脚本以及程序,详见该文件夹下readme.txt文件
Visual Relationship Interface/内包含了训练和测试的接口以及简单界面
运行demo步骤：
1.按官方文档编译py-faster-rcnn，将本文件夹拷贝至其根目录
2.执行脚本命令：python GUI.py，打开用户界面
3.选择待训练的图像文件夹，点击开始训练，进行模型训练
4.编辑好rules.txt内语义规则，选择该文件
5.选择图像，检测包含的隐私行为
faster-rcnn训练步骤：
1.收集图像，利用图像格式转换工具将图像全部转化为jpeg图像
2.运行RenameFiles.py将文件进行重命名操作
3.利用Tools/下CreateOwnDataset.py将数据集划分为train，val，test，最后的数据集形式应和PascalVOC数据集一致
4.将ModifyFileforVOC2017/内对应文件覆盖原代码中对应文件
5.根目录执行训练脚本./experiments/scripts/faster_rcnn_alt_opt.sh 0 ZF pascal_voc，得到训练模型
cnn训练步骤：
1.将图像命名为person1-1.jpg形式，修改TrainNet.py中ChangePrototxt()函数类别数。
2.执行TrainNet.py一键训练