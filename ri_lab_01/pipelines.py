# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.conf import settings

from ri_lab_01.items import RiLab01Item
from ri_lab_01.items import RiLab01CommentItem

import csv

class RiLab01Pipeline(object):
    
    def process_item(self, item, spider):
        return item
