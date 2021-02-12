# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from dataclasses import dataclass
from typing import List


@dataclass
class SeriesItem:
    """model pro jednotlive serie"""
    name: int
    # list urls jednotlivych epizod
    episodes: List[str]


@dataclass
class GenericInfoItem:
    """model pro vsechny informace o serialu"""
    name_original: str
    year: int
    genre: str
    # v listu series za kazdou serii jeden SeriesItem
    series: List[SeriesItem]
