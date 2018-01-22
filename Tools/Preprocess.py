# -*-coding:utf-8-*-
import os, shutil
from PIL import Image
from lxml import etree

import FileOperate as fo

'''
This script includes function on preprocess images,xmlfile and get frames from video.
'''


##############xml#########################3
def ReadXML(path):
    with open(path, 'r') as f:
        content = f.read()
        ImgXML = etree.XML(content)
        return ImgXML


def WriteXML(XMLname, ImgXML):
    with open(XMLname, 'w') as f:
        f.write(etree.tostring(ImgXML))


def GenerateNewName(xmlfile):
    oldname = os.path.splitext(xmlfile)[0]
    if oldname.isdigit():
        newname = oldname
    else:
        clsname = oldname.split("_")[0]
        oldnum = oldname.split("_")[2]
        if clsname == 'kiss':
            clsnum = 0
        if clsname == 'hug':
            clsnum = 1
        if clsname == 'hands':
            clsnum = 2
        newname = str(clsnum) + oldnum[-5:]
    return newname


def ModifyXML(xmlfile):
    ImgXML = ReadXML(xmlfile)
    newname = GenerateNewName(xmlfile)
    path = "/home/wxyz/relationship/VOC2007/" + newname + ".jpg"
    ImgXML.find('filename').text = newname
    ImgXML.find('path').text = path
    newfile = newname + ".xml"
    WriteXML(newfile, ImgXML)


def modifytext(imgdir, textdir):
    imglist = fo.readfile(imgdir)
    textlist = fo.readfile(textdir)
    imgset = set()
    for img in imglist:
        imgset.add(os.path.splitext(img)[0])
    for text in textlist:
        newtext = []
        textpath = os.path.join(textdir, text)
        with open(textpath, 'r') as f:
            lines = f.readlines()
            for line in lines:
                name = line.split(" ")[0]
                if name in imgset:
                    newtext.append(line)
        os.rename(textpath, textpath + ".old")
        with open(textpath, 'w') as f:
            for text in newtext:
                f.write(text)


def RemoveSomePerson(suffix='f'):
    suffixes = set(['a', 'b', 'c', 'd', 'e', 'f'])
    abspath = os.path.abspath('.')
    imagepath = os.path.join(abspath, 'Persons')
    imageset = fo.readspecialfile(imagepath, '.jpg')
    enoughset = set()
    for image in imageset:
        imgsuffix = image[-5:-4]
        personname = image[:-5]
        if imgsuffix == suffix:
            enoughset.add(personname)
    for image in imageset:
        imgsuffix = image[-5:-4]
        personname = image[:-5]
        if personname not in enoughset:
            imagename = os.path.join(imagepath, image)
            os.remove(imagename)
        if imgsuffix not in suffixes:
            imagename = os.path.join(imagepath, image)
            os.remove(imagename)


def ReadPerson(path):
    personset = []
    ImgXML = ReadXML(path)
    xmlObjectlist = ImgXML.findall('object')
    for xmlObject in xmlObjectlist:
        if 'person' == xmlObject.find('name').text:
            xmin = int(xmlObject.find('bndbox').find('xmin').text)
            ymin = int(xmlObject.find('bndbox').find('ymin').text)
            xmax = int(xmlObject.find('bndbox').find('xmax').text)
            ymax = int(xmlObject.find('bndbox').find('ymax').text)
            personset.append([xmin, ymin, xmax, ymax])
    return personset


def Capture(imgdirpath, im_file, Persons):
    imgname = os.path.splitext(im_file)
    imgpath = os.path.join(imgdirpath, im_file)
    img = Image.open(imgpath)
    count = 1
    for pos in Persons:
        cropImg = img.crop(pos)
        newname = imgname[0] + '-' + str(count) + imgname[1]
        newimgpath = os.path.join(imgdirpath, newname)
        cropImg.save(newimgpath)
        count = count + 1


def GetPersonZone(imgdir='kiss', annodir='kissxml'):
    abspath = os.path.abspath('..')
    imgdirpath = os.path.join(abspath, imgdir)
    annodirpath = os.path.join(abspath, annodir)
    imgfileset = fo.readfile(imgdirpath)
    for im_file in imgfileset:
        annofile = os.path.join(annodirpath, os.path.splitext(im_file)[0] + '.xml')
        Persons = ReadPerson(annofile)
        Capture(imgdirpath, im_file, Persons)


def ffmepgcmd(file, videoname):
    cmd = "ffmpeg -i " + file + " " + videoname + "_frame_%4d.jpg"
    print cmd
    os.system(cmd)


def readlabel(path):
    labels = []
    try:
        f = open(path, 'r')
        for line in f.readlines():
            if line[-3:] == " 1\n":
                labels.append(line[:11] + '.jpg')
    finally:
        if f:
            f.close()
            return labels


def copyfile(labels, src, dst):
    for label in labels:
        imagename = os.path.join(src, label)
        shutil.copy(imagename, dst)


if __name__ == "__main__":
    abspath = os.path.abspath('.')
    annopath = os.path.join(abspath, "annotations")
    fileset = fo.readspecialfile(abspath)
    fo.createclass(abspath, "handShake")
    fo.createclass(abspath, "highFive")
    fo.createclass(abspath, "hug")
    fo.createclass(abspath, "kiss")
    for file in fileset:
        videoname = os.path.splitext(file)[0]
        kindname = videoname.split("_")[0]
        annofile = os.path.join(annopath, videoname + ".annotations")
        frameset = fo.readannotation(annofile)
        ffmepgcmd(file, videoname)
        for framenum in frameset:
            framename = videoname + "_frame_" + ("0000" + str(framenum))[-4:] + ".jpg"
            shutil.move(framename, kindname)
        fo.removeframe(abspath)
    labelpath = os.path.join(os.path.abspath('.'), "person_train.txt")
    labels = readlabel(labelpath)
    imagepath = os.path.join(os.path.abspath('.'), "JPEGImages")
    dst = os.path.join(os.path.abspath('.'), "person")
    copyfile(labels, imagepath, dst)
    # abspath = os.path.abspath('.')
    # dirA = os.path.join(abspath, "JPEGImages")
    # dirB = os.path.join(abspath, "Annotations")
    # ImageSetDir = os.path.join(abspath, "ImageSets", "Main")
    # fo.removedifferentname(dirA, dirB, ".jpg", ".xml")
    # modifytext(dirA, ImageSetDir)
    # RemoveSomePerson('f')
    GetPersonZone()
    abspath = os.path.abspath('.')
    xmlfiles = fo.readspecialfile(abspath, ext=".xml")
    for xmlfile in xmlfiles:
        ModifyXML(xmlfile)
