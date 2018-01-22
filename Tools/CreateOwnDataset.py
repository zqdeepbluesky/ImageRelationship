# -*-coding:utf-8-*-
import os
import random

import FileOperate as fo

'''
Generate txt files in directory VOC2017/ImageSet
'''

def GenerateSet(abspath, imgsetdir):
    imgset = []
    imgfiles = fo.readfile(os.path.join(abspath, imgsetdir))
    for imgfile in imgfiles:
        imgset.append(os.path.splitext(imgfile)[0])
    rate = [0.5, 0.5, 0.5, 0.5]
    clsset = ['kiss', 'hug', 'hands']
    txtset = ['trainval.txt', 'train.txt', 'val.txt', 'test.txt']
    trainvalset = []
    testset = []
    trainvalposset = set(random.sample(xrange(len(imgset)), int(len(imgset) * rate[0])))
    testposset = set(xrange(len(imgset))) - trainvalposset
    for pos in trainvalposset:
        trainvalset.append(imgset[pos])
    for pos in testposset:
        testset.append(imgset[pos])
    trainset = []
    valset = []
    trainposset = set(random.sample(xrange(len(trainvalset)), int(len(trainvalset) * rate[1])))
    valposset = set(xrange(len(trainvalset))) - trainposset
    for pos in trainposset:
        trainset.append(trainvalset[pos])
    for pos in valposset:
        valset.append(trainvalset[pos])
    fo.createtext(txtset[0], trainvalset, 2)
    fo.createtext(txtset[1], trainset, 2)
    fo.createtext(txtset[2], valset, 2)
    fo.createtext(txtset[3], testset, 2)
    for trainvalimg in trainvalset:
        imgname = []
        imgname.append(trainvalimg)
        clsname = trainvalimg.split("_")[0]
        if clsset[0] == clsname:
            fo.createtext(clsset[0] + "_" + txtset[0], imgname, 1)
            fo.createtext(clsset[1] + "_" + txtset[0], imgname, -1)
            fo.createtext(clsset[2] + "_" + txtset[0], imgname, -1)
        elif clsset[1] == clsname:
            fo.createtext(clsset[0] + "_" + txtset[0], imgname, -1)
            fo.createtext(clsset[1] + "_" + txtset[0], imgname, 1)
            fo.createtext(clsset[2] + "_" + txtset[0], imgname, -1)
        else:
            fo.createtext(clsset[0] + "_" + txtset[0], imgname, -1)
            fo.createtext(clsset[1] + "_" + txtset[0], imgname, -1)
            fo.createtext(clsset[2] + "_" + txtset[0], imgname, 1)
    for trainimg in trainset:
        imgname = []
        imgname.append(trainimg)
        clsname = trainimg.split("_")[0]
        if clsset[0] == clsname:
            fo.createtext(clsset[0] + "_" + txtset[1], imgname, 1)
            fo.createtext(clsset[1] + "_" + txtset[1], imgname, -1)
            fo.createtext(clsset[2] + "_" + txtset[1], imgname, -1)
        elif clsset[1] == clsname:
            fo.createtext(clsset[0] + "_" + txtset[1], imgname, -1)
            fo.createtext(clsset[1] + "_" + txtset[1], imgname, 1)
            fo.createtext(clsset[2] + "_" + txtset[1], imgname, -1)
        else:
            fo.createtext(clsset[0] + "_" + txtset[1], imgname, -1)
            fo.createtext(clsset[1] + "_" + txtset[1], imgname, -1)
            fo.createtext(clsset[2] + "_" + txtset[1], imgname, 1)
    for valimg in valset:
        imgname = []
        imgname.append(valimg)
        clsname = valimg.split("_")[0]
        if clsset[0] == clsname:
            fo.createtext(clsset[0] + "_" + txtset[2], imgname, 1)
            fo.createtext(clsset[1] + "_" + txtset[2], imgname, -1)
            fo.createtext(clsset[2] + "_" + txtset[2], imgname, -1)
        elif clsset[1] == clsname:
            fo.createtext(clsset[0] + "_" + txtset[2], imgname, -1)
            fo.createtext(clsset[1] + "_" + txtset[2], imgname, 1)
            fo.createtext(clsset[2] + "_" + txtset[2], imgname, -1)
        else:
            fo.createtext(clsset[0] + "_" + txtset[2], imgname, -1)
            fo.createtext(clsset[1] + "_" + txtset[2], imgname, -1)
            fo.createtext(clsset[2] + "_" + txtset[2], imgname, 1)
    for testimg in testset:
        imgname = []
        imgname.append(testimg)
        fo.createtext(clsset[0] + "_" + txtset[3], imgname, 0)
        fo.createtext(clsset[1] + "_" + txtset[3], imgname, 0)
        fo.createtext(clsset[2] + "_" + txtset[3], imgname, 0)


if __name__ == "__main__":
    abspath = os.path.abspath('.')
    imgsetdir = 'JPEGImages'
    GenerateSet(abspath, imgsetdir)
