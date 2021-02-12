from scrapy.http import request
from hbo.items import GenericInfoItem
from hbo.items import SeriesItem

from typing import List
import scrapy


# spider na crawlovani poradu
class ShowsSpider(scrapy.Spider):
    name = "shows"

    def __init__(self, url: str, *args, **kwargs):
        """Inicializator shows spideru
            argumenty:
                url -- url poradu pro scrappovani
        """
        super().__init__(*args, **kwargs)

        # url se uklada do listu start_urls, ze ktereho scrappy vychazi
        self.start_urls = [url]

    def parse(self, response):
        """prvni parse metoda na stranku

            postupne vraci:
            GenericInfoItem (v nem strucne obecne info)
            Requesty pro jednotlive serie (nasledne zparsovane v parse_series)
        """

        # v tomto oddile jsou veskere informace o serialu
        details = response.css('div.modal-details')

        # zde je rok a zanr serialu
        meta = details.css("div.meta::text").getall()

        # list series je zatim prazdny, v pipelinu HboPipeline
        # se do nej prubezne ulozi vsechny serie serialu
        yield GenericInfoItem(
                name_original=details.css(
                              "span.original-title::text"
                              ).get(),
                year=meta[0],
                genre=meta[1],
                series=[]
                )

        # list urls jednotlivych serii
        season_urls = response.css("div#seasons a::attr(href)").getall()

        # za kazdou serii vrati Request na danou url
        for url in season_urls:
            yield response.follow(url=url, callback=self.parse_series)

    def parse_series(self, response):
        """parsuje jednotlive serie serialu
            generuje SeriesItemy s nazvem serie a urls jednotlivych epizod
        """

        # cislo serie
        series_number = response.css(
            "div.season-tab a.selected::text"
            ).get()

        # list urls jednotlivych epizod
        episodes = response.css(
            "div.shelf-modal-episode-item a::attr(href)"
            ).getall()

        yield SeriesItem(
            name=series_number,
            episodes=episodes
        )
