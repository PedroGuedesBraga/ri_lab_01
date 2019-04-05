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
        date_not_formatted = item['date'][0]
        print('Data:')
        print(item['date'][0])
        formattedDate = self.formatDate(date_not_formatted)
        item['date'] = formattedDate
        print('Item date formatted to dd-mm-yyyy hh/mi/ss')
        return item




# Auxiliar:
# Change date to the format needed
    def formatToDD_MM_YY(self, date):
        date_and_time = date.split('T')
        year_month_day = date_and_time[0].split('-')
        year_month_day.reverse()
        return '-'.join(year_month_day)
        

    def formatDate(self, date):
        hh_mm_ss = date.split('T')[1]
        dd_mm_yy = self.formatToDD_MM_YY(date)
        return " ".join([dd_mm_yy, hh_mm_ss])