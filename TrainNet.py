# -*-coding:utf-8-*-

import _init_paths
import os, shutil
import random
from PIL import Image


def WriteText(trainfilename, valfilename, testfilename, fileset, count):
    trainset = []
    testset = []
    trainvalposset = set(random.sample(xrange(len(fileset)), 5))
    testposset = set(xrange(len(fileset))) - trainvalposset
    valposset = random.sample(trainvalposset, 1)
    trainposset = trainvalposset - set(valposset)
    for pos in trainposset:
        trainset.append(fileset[pos])
    for pos in testposset:
        testset.append(fileset[pos])
    with open(trainfilename, 'a') as f:
        for file in trainset:
            writetext = file + " " + str(count)
            writetext = writetext + "\n"
            f.write(writetext)
    with open(valfilename, 'a') as f:
        writetext = fileset[valposset[0]] + " " + str(count)
        writetext = writetext + "\n"
        f.write(writetext)
    with open(testfilename, 'a') as f:
        for file in testset:
            writetext = file + " " + str(count)
            writetext = writetext + "\n"
            f.write(writetext)


def ReadJpeg(srcdir, ext=".jpg"):
    fileset = []
    for file in os.listdir(srcdir):
        absfilename = os.path.join(srcdir, file)
        if os.path.isfile(absfilename) and os.path.splitext(absfilename)[1] == ext:
            fileset.append(file)
    return sorted(fileset)


def CreateTrainValTestTxt(imsetpath, fileset):
    trainfilename = os.path.join(imsetpath, 'train.txt')
    valfilename = os.path.join(imsetpath, 'val.txt')
    testfilename = os.path.join(imsetpath, 'test.txt')
    if os.path.exists(trainfilename):
        os.remove(trainfilename)
    if os.path.exists(valfilename):
        os.remove(valfilename)
    if os.path.exists(testfilename):
        os.remove(testfilename)
    clsset = []
    count = -1
    previousname = ''
    for file in fileset:
        imgname = os.path.splitext(file)[0]
        personname = imgname.split('-')[0]
        if previousname == personname:
            clsset.append(file)
        else:
            if 0 != len(clsset):
                WriteText(trainfilename, valfilename, testfilename, clsset, count)
            clsset = []
            clsset.append(file)
            previousname = personname
            count = count + 1
    if 0 != len(clsset):
        WriteText(trainfilename, valfilename, testfilename, clsset, count)
    with open(trainfilename, 'r') as f:
        trainfile = f.readlines()
        mixfile = []
        pos = 0
        for i in range(len(trainfile)):
            print pos
            mixfile.append(trainfile[pos])
            pos = (pos + 4) % len(trainfile)
    with open(trainfilename, 'w') as f:
        for fil in mixfile:
            f.write(fil)


def ConvertImagesize(imsetpath, fileset):
    for file in fileset:
        print "Convert:" + file
        filepath = os.path.join(imsetpath, file)
        im = Image.open(filepath)
        out = im.resize((256, 256), Image.ANTIALIAS)
        out.save(filepath)


def CreateImagenet(tooldir='../caffe-fast-rcnn/build/tools', datadir='../DetectPerson/data/Persons'):
    imdbdir = datadir + "/person_train_lmdb"
    if os.path.exists(imdbdir):
        shutil.rmtree(imdbdir)
    cmd = tooldir + "/convert_imageset --shuffle " + datadir + "/ " + datadir + "/train.txt " + imdbdir
    print cmd
    os.system(cmd)
    imdbdir = datadir + "/person_val_lmdb"
    if os.path.exists(imdbdir):
        shutil.rmtree(imdbdir)
    cmd = tooldir + "/convert_imageset --shuffle " + datadir + "/ " + datadir + "/val.txt " + imdbdir
    print cmd
    os.system(cmd)


def MakeImagenetMean(tooldir='../caffe-fast-rcnn/build/tools', datadir='../DetectPerson/data/Persons'):
    cmd = tooldir + "/compute_image_mean " + datadir + "/person_train_lmdb " + datadir + "/imagenet_mean.binaryproto"
    print cmd
    os.system(cmd)


def ChangePrototxt(prototxt, clsnum=20):
    posofcls = 372
    with open(prototxt, 'r') as f:
        filebuf = f.readlines()
        clstxt = filebuf[posofcls]
        clsset = clstxt.split(':')
        clsset[1] = ' ' + str(clsnum) + '\n'
        clstxt = ":".join(clsset)
        filebuf[posofcls] = clstxt
    with open(prototxt, 'w') as f:
        for line in filebuf:
            f.write(line)


def TrainCaffeNet(prototxt, mode=1):  # mode 1 for training, 2 for finetuning
    tooldir = '../caffe-fast-rcnn/build/tools'
    abspath = os.getcwd()
    imsetpath = os.path.join(abspath, 'data/Persons')
    fileset = ReadJpeg(imsetpath)
    CreateTrainValTestTxt(imsetpath, fileset)
    ConvertImagesize(imsetpath, fileset)
    CreateImagenet()
    MakeImagenetMean()
    ChangePrototxt(prototxt)
    if 1 == mode:
        cmd = tooldir + "/caffe train --solver=../DetectPerson/bvlc_reference_caffenet/solver.prototxt"
    else:
        cmd = tooldir + "/caffe train --solver=../DetectPerson/bvlc_reference_caffenet/finetune-solver.prototxt" \
              + " --weights ../DetectPerson/bvlc_reference_caffenet/bvlc_reference_caffenet.caffemodel"
    print cmd
    os.system(cmd)


if __name__ == "__main__":
    prototxt = "bvlc_reference_caffenet/finetune-train_val.prototxt"
    TrainCaffeNet(prototxt, 2)
