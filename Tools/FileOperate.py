# -*-coding:utf-8-*-
import os
import re

'''
A public class about file operation
'''
# ---------------create----------------------
def createclass(abspath, dirname):
    dirpath = os.path.join(abspath, dirname)
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)


def createtext(filename, fileset, flag):
    with open(filename, 'a') as f:
        for file in fileset:
            if 2 == flag:
                writetext = file
            else:
                writetext = file + " " + str(flag)
            writetext = writetext + "\n"
            f.write(writetext)


# ---------------read-----------------------
def readspecialfile(srcdir, ext=".avi"):
    fileset = []
    for file in os.listdir(srcdir):
        absfilename = os.path.join(srcdir, file)
        if os.path.isfile(absfilename) and os.path.splitext(absfilename)[1] == ext:
            fileset.append(file)
    return sorted(fileset)


def readfile(srcdir):
    fileset = []
    for image in os.listdir(srcdir):
        if os.path.isfile(os.path.join(srcdir, image)):
            fileset.append(image)
    return sorted(fileset)


def readannotation(path):
    frameset = []
    with open(path, 'r') as f:
        text = f.readline()
        framenum = int(re.findall(r'(\w*[0-9]+)\w*', text)[0])
        for framecount in range(1, framenum):
            text = f.readline()
            box = re.findall(r'#num_bbxs:\s+\d', text)
            interacting = re.findall(r'#interacting:', text)
            boxnum = int(re.findall(r'(\w*[0-9]+)\w*', str(box))[0])
            if len(interacting) == 1:
                frameset.append(framecount)
            for boxcount in range(boxnum):
                text = f.readline()
    return frameset


# ----------------remove---------------------
def removeframe(srcdir, ext=".jpg"):
    frameset = readspecialfile(srcdir, ext)
    for frame in frameset:
        framepath = os.path.join(srcdir, frame)
        os.remove(framepath)


def removedifferentname(dirA, dirB, extA, extB):
    filesetA = readspecialfile(dirA, extA)
    filesetB = readspecialfile(dirB, extB)
    datasetA = set()
    datasetB = set()
    for file in filesetA:
        datasetA.add(os.path.splitext(file)[0])
    for file in filesetB:
        datasetB.add(os.path.splitext(file)[0])
    difdataA = datasetA - datasetB
    difdataB = datasetB - datasetA
    for ele in difdataA:
        elepath = os.path.join(dirA, ele + extA)
        os.remove(elepath)
    for ele in difdataB:
        elepath = os.path.join(dirB, ele + extB)
        os.remove(elepath)


if __name__ == "__main__":
    fileset = ('1111', '2222', '3333')
    createtext('a.txt', fileset, -1)
