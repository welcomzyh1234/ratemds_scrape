# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import signals
from scrapy.exporters import CsvItemExporter


class CsvWriterPipeline(object):
    FIELDS_TO_EXPORT = ['Facility_Name', 'Doctor_Name', 'Has_Rating', 'Staff_Rating', 'Punctuality_Rating',
                        'Helpfulness_Rating', 'Knowledge_Rating', 'Average_Rating', 'Comment_Votes', 'Comment_Date',
                        'Comment_Text']

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        self.file = open('DoctorRating.csv', 'a+b')
        self.exporter = CsvItemExporter(self.file, fields_to_export=self.FIELDS_TO_EXPORT)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        comment_text = item.get('Comment_Text')

        # remove new lines in comment test
        if comment_text:
            item['Comment_Text'] = comment_text.replace('\n', ' ').replace('\r', ' ')

        self.exporter.export_item(item)
        return item
