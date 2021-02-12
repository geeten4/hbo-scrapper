# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import scrapy
from hbo.items import GenericInfoItem, SeriesItem
from typing import List
from scrapy.exporters import JsonItemExporter

class HboPipeline:
    g: GenericInfoItem = None
    series: List[SeriesItem] = []

    def close_spider(self, spider):
        file = open('output.json', 'wb')
        exporter = JsonItemExporter(file)
        exporter.start_exporting()
        self.g.series = self.series
        exporter.export_item(self.g)
        exporter.finish_exporting()



    def process_item(self, item, spider):

        if isinstance(item, SeriesItem):
            self.series.append(item)

        elif isinstance(item, GenericInfoItem):
            self.g = item

