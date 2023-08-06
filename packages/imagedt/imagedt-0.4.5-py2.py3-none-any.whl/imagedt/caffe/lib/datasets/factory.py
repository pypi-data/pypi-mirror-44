# --------------------------------------------------------
# Fast R-CNN
# Copyright (c) 2015 Microsoft
# Licensed under The MIT License [see LICENSE for details]
# Written by Ross Girshick
# --------------------------------------------------------

"""Factory method for easily getting imdbs by name."""

__sets = {}

from datasets.pascal_voc import pascal_voc
from datasets.coco import coco
from fast_rcnn.config import cfg

import sys, os
sys.path.insert(0, '/home/train/py-R-FCN/my_project')

from init_train import parse_arg

import numpy as np

split = parse_arg().imdb_name.split('_', 0)[1]
year = parse_arg().imdb_name.split('_', 0)[0]
name = '{}_{}'.format(year, split)
__sets[name] = (lambda split=split, year=year: pascal_voc(split, year, cfg.DATA_DIR))
'''''''''
for year in ['201703']:
    for split in ['trainval']:
        name = '{}_{}'.format(year, split)
        __sets[name] = (lambda split=split, year=year: pascal_voc(split, year, cfg.DATA_DIR))
'''''''''
# Set up voc_<year>_<split> using selective search "fast" mode
for year in ['2007', '2012', '0712', '201703', '201704', '201705', '201706', '201707', '201708', '201709', '201710',
             '201711', '201712']:
    for split in ['train', 'val', 'trainval', 'test', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10']:
        name = 'voc_{}_{}'.format(year, split)
        __sets[name] = (lambda split=split, year=year: pascal_voc(split, year, cfg.DATA_DIR))


# Set up coco_2014_<split>
for year in ['2014']:
    for split in ['train', 'val', 'minival', 'valminusminival']:
        name = 'coco_{}_{}'.format(year, split)
        __sets[name] = (lambda split=split, year=year: coco(split, year))

# Set up coco_2015_<split>
for year in ['2015']:
    for split in ['test', 'test-dev']:
        name = 'coco_{}_{}'.format(year, split)
        __sets[name] = (lambda split=split, year=year: coco(split, year))

def get_imdb(name):
    """Get an imdb (image database) by name."""
    if not __sets.has_key(name):
        raise KeyError('Unknown dataset: {}'.format(name))
    print '--------------------test7------------------------------'
    # '__sets' is a set including all such as coco_2015_test coco_2014_val voc_2012_trainval...
    # print __sets[name]
    print __sets[name]()
    return __sets[name]()

def list_imdbs():
    """List all registered imdbs."""
    return __sets.keys()
