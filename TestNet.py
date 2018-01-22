#!/usr/bin/env python

# --------------------------------------------------------
# Faster R-CNN
# Copyright (c) 2015 Microsoft
# Licensed under The MIT License [see LICENSE for details]
# Written by Ross Girshick
# --------------------------------------------------------

"""
Demo script showing detections in sample images.

See README.md for installation instructions before running.
"""

import _init_paths
import glob
from fast_rcnn.config import cfg
from fast_rcnn.test import im_detect
from fast_rcnn.nms_wrapper import nms
from utils.timer import Timer
import matplotlib.pyplot as plt
import numpy as np
import caffe, os, sys, cv2
from PIL import Image

CLASSES = ('__background__',
           'kiss', 'hug', 'hands', 'person')
person = [
    'person1', 'person10', 'person11', 'person12', 'person13', \
    'person14', 'person15', 'person16', 'person17', 'person18', \
    'person19', 'person2', 'person20', 'person3', 'person4', \
    'person5', 'person6', 'person7', 'person8', 'person9'
]


def DetectRCNN(net, image_name, CONF_THRESH=0.1, NMS_THRESH=0.1):
    ClassList = []
    """Detect object classes in an image using pre-computed object proposals."""
    # Load the demo image
    im_file = os.path.join(cfg.DATA_DIR, 'demo', image_name)
    im = cv2.imread(im_file)

    # Detect all object classes and regress object bounds
    timer = Timer()
    timer.tic()
    scores, boxes = im_detect(net, im)
    timer.toc()
    print ('Detection took {:.3f}s for '
           '{:d} object proposals').format(timer.total_time, boxes.shape[0])

    # Visualize detections for each class
    for cls_ind, cls in enumerate(CLASSES[1:]):
        cls_ind += 1  # because we skipped background
        cls_boxes = boxes[:, 4 * cls_ind:4 * (cls_ind + 1)]
        cls_scores = scores[:, cls_ind]
        dets = np.hstack((cls_boxes,
                          cls_scores[:, np.newaxis])).astype(np.float32)
        keep = nms(dets, NMS_THRESH)
        dets = dets[keep, :]
        inds = np.where(dets[:, -1] >= CONF_THRESH)[0]
        for i in inds:
            Cls = [cls]
            bbox = dets[i, :4]
            score = dets[i, -1]
            Cls.append(score)
            Cls.append(bbox)
            ClassList.append(Cls)
    return ClassList


def vis_detections(image_name, ClassList, thresh=0.1):
    """Draw detected bounding boxes."""
    im_file = os.path.join(cfg.DATA_DIR, 'demo', image_name)
    im = cv2.imread(im_file)
    im = im[:, :, (2, 1, 0)]
    fig, ax = plt.subplots(figsize=(12, 12))
    ax.imshow(im, aspect='equal')
    for Cls in ClassList:
        class_name = Cls[0]
        score = Cls[1]
        bbox = Cls[2]

        ax.add_patch(
            plt.Rectangle((bbox[0], bbox[1]),
                          bbox[2] - bbox[0],
                          bbox[3] - bbox[1], fill=False,
                          edgecolor='red', linewidth=3.5)
        )
        ax.text(bbox[0], bbox[1] - 2,
                '{:s} {:.3f}'.format(class_name, score),
                bbox=dict(facecolor='blue', alpha=0.5),
                fontsize=14, color='white')

    ax.set_title(('{} detections with '
                  'p({} | box) >= {:.1f}').format(class_name, class_name,
                                                  thresh),
                 fontsize=14)
    plt.axis('off')
    plt.tight_layout()
    plt.draw()
    plt.show()


def ChangePrototxt(prototxt, clsnum=20):
    posofcls = 205
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


def Classify(inputs, im_name, mode=1):
    model = "bvlc_reference_caffenet/caffenet_train_iter_300.caffemodel"
    prototxt = "bvlc_reference_caffenet/deploy.prototxt"
    ChangePrototxt(prototxt)
    classifier = caffe.Classifier(prototxt, model)
    if 1 == mode:
        inputs = [caffe.io.load_image(im_name)]
    predictions = classifier.predict(inputs)
    top_k = predictions.flatten().argsort()[-1:-2:-1]
    return top_k[0]


def BenchMark(imgdir="data/Persons", testtxt="data/Persons/test.txt"):
    rightnum = 0
    totalnum = 100
    with open(testtxt, 'r') as f:
        for line in f.readlines():
            imgset = line.split(' ')
            imgpath = os.path.join(imgdir, imgset[0])
            personcls = Classify('', imgpath)
            print imgset[0]
            if personcls == imgset[1]:
                rightnum = rightnum + 1
    accuracy = rightnum / totalnum
    print "accuracy is: " + str(accuracy)


def TestImage(im_names, mode='gpu'):
    cfg.TEST.HAS_RPN = True  # Use RPN for proposals
    prototxt = os.path.join(cfg.MODELS_DIR, 'ZF',
                            'faster_rcnn_alt_opt', 'faster_rcnn_test.pt')
    caffemodel = os.path.join(cfg.DATA_DIR, 'faster_rcnn_models',
                              'ZF_faster_rcnn_final.caffemodel')
    if 'gpu' == mode:
        caffe.set_mode_gpu()
    else:
        caffe.set_mode_cpu()
    caffe.set_device(0)
    cfg.GPU_ID = 0
    net = caffe.Net(prototxt, caffemodel, caffe.TEST)

    print '\n\nLoaded network {:s}'.format(caffemodel)

    # Warmup on a dummy image
    im = 128 * np.ones((300, 500, 3), dtype=np.uint8)
    for i in xrange(2):
        _, _ = im_detect(net, im)
    for im_name in im_names:
        print 'Demo for demo/JPEGImages/{}'.format(im_name)
        ClassList = DetectRCNN(net, im_name)
        im_file = os.path.join(cfg.DATA_DIR, 'demo', im_name)
        img = Image.open(im_file)
        contents = []
        persons = set()
        for i in range(len(ClassList)):
            cls = ClassList[i]
            if "person" == cls[0]:
                crop_file = os.path.join(cfg.DATA_DIR, 'demo', 'crop.jpg')
                cropImg = img.crop(cls[2])
                cropImg.save(crop_file)
                inputs = [caffe.io.load_image(crop_file)]
                cls[0] = Classify(inputs, im_name, 2)
                ClassList[i] = cls
                persons.add(cls[0])
            if cls[0] in set(['kiss', 'hug', 'hands']):
                contents.append(cls[0])
        contents.append(set(persons))
        vis_detections(im_name, ClassList)


if __name__ == '__main__':
    im_names = ['200001.jpg', '200002.jpg', '200003.jpg', '200004.jpg', '200005.jpg']
    TestImage(im_names, 'gpu')
    # cls=Classify(1, 'data/Persons/person19-2.jpg')
    # print person[cls]
    # BenchMark()
