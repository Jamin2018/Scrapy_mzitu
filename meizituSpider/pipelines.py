# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
import re

class MeizituspiderPipeline(object):
    def process_item(self, item, spider):
        return item

class MyImagesPipeline(ImagesPipeline):
    # 重写文件保存路径和文件名

    def get_media_requests(self, item, info):

        for image_url in item['image_urls']:
            referer=item['urls']  # 处理防盗链
            yield scrapy.Request(image_url,
                          meta={'item': item,'referer':referer}) #配合get_media_requests传递meta，不然拿不到item的.不会下载

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        folder = item['title']
        folder_strip = folder.strip()
        image_guid = request.url.split('/')[-1]
        year = item['year']
        month = item['month']
        filename = u'imge/{0}/{1}/{2}/{3}'.format(year,month,folder_strip,image_guid)
        return filename


    def item_completed(self, results, item, info):
        image_path = [x['path'] for ok, x in results if ok]
        if not image_path:
            raise DropItem('Item contains no images')
        # item['image_paths'] = image_path
        return item

    def strip(path):
        """
        :param path: 需要清洗的文件夹名字
        :return: 清洗掉Windows系统非法文件夹名字的字符串
        """
        path = re.sub(r'[？\\*|“<>:/]', '', str(path))
        return path