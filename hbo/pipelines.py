# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import scrapy
from hbo.items import GenericInfoItem, SeriesItem
from typing import List, Union
from scrapy.exporters import JsonItemExporter


class HboPipeline:
    """
    procesuje vsechny itemy nalezene v shows_spider

    shows_spider nejprve vraci GenericInfoItem, pote za kazdou serii
    jeden SeriesItem. Aby spider vratil jeden Json objekt,
    v atributech HboPipeline se ulozi nejprve instance GenericInfoItem
    v self.generic_info, kazda instance SeriesItem se ulozi do self.series,
    pote se do Json souboru output.json vypise jeden objekt
    """

    # ulozi GenericInfoItem
    generic_info: GenericInfoItem = None
    # ulozi jednotlive SeriesItemy
    series: List[SeriesItem] = []

    def process_item(self,
                     item: Union[GenericInfoItem, SeriesItem],
                     spider: scrapy.Spider
                     ) -> None:
        """
            procesuje prichozi itemy
            Argumenty:
            item -- GenericInfoItem / SeriesItem
        """

        # pokud je prichozi item instanci SeriesItemu,
        # ulozi se do self.series
        if isinstance(item, SeriesItem):
            self.series.append(item)

        # jinak pokud je instanci GenericInfoItem,
        # ulozi se do self.generic_info
        elif isinstance(item, GenericInfoItem):
            self.generic_info = item

    def close_spider(self, spider: scrapy.Spider) -> None:
        """
            vola se pri ukonceni shows_sipderu
            do atributu series objektu self.generic_info uklada list serii
            self.series
            vysledny objekt self.generic_info vypisuje do output.json
        """

        file = open('output.json', 'wb')

        # pouziva vestaveny scrapy Json Exporter
        exporter = JsonItemExporter(file)
        exporter.start_exporting()

        # do atributu series objektu generic_info
        # uklada nashromazdene SeriesItemy ze self.series
        self.generic_info.series = self.series

        exporter.export_item(self.generic_info)
        exporter.finish_exporting()
