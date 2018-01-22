# -*-coding:utf-8-*-
import os
import argparse

'''
This scrpit was designed for rename these jpeg images downloaded from different websites,we can use it to rename
as such format: 0000001.jpg
'''


def readimage(FileDir):
    imageset = []
    for image in os.listdir(FileDir):
        if os.path.isfile(os.path.join(FileDir, image)):
            imageset.append(image)
    return imageset


def RenameFiles(FileDir, count=1):
    extlist = ['.jpg', '.jpeg']
    imageset = readimage(FileDir)
    for image in imageset:
        extension = os.path.splitext(image)[1].lower()
        if FileDir == 'kiss':
            clsnum = 0
        if FileDir == 'hug':
            clsnum = 1
        if FileDir == 'hands':
            clsnum = 2
        if extension in extlist:
            oldname = os.path.join(FileDir, image)
            newimage = '0000' + str(count)
            count = count + 1
            newimagename = str(clsnum) + newimage[-5:] + '.jpg'

            print newimagename
            newname = os.path.join(FileDir, newimagename)
            os.rename(oldname, newname)
        else:
            print "Exist non-jpeg files: " + image
            break


def RenameExt(FileDir):
    extlist = ['.jpg', '.jpeg']
    imageset = readimage(FileDir)
    for image in imageset:
        name = os.path.splitext(image)[0].lower()
        extension = os.path.splitext(image)[1].lower()
        if extension in extlist:
            newimagename = name + '.jpg'
            print newimagename
            oldname = os.path.join(FileDir, image)
            newname = os.path.join(FileDir, newimagename)
            os.rename(oldname, newname)
        else:
            print "Exist non-jpeg files: " + image
            break


def parse_args():
    """Parse input arguments."""

    parser = argparse.ArgumentParser(description='Rename demo')
    parser.add_argument('-set', dest='dataset', help='choose dataset')
    parser.add_argument('-count', dest='countnum', help='start number is set to 0',
                        default=0, type=int)
    args = parser.parse_args()

    return args


if __name__ == "__main__":
    args = parse_args()
    if args.countnum == 0:
        RenameExt(args.dataset)
    else:
        RenameFiles(args.dataset, args.countnum)
