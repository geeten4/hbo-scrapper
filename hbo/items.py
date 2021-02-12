# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from dataclasses import dataclass
from typing import List

#SeriesItem model
@dataclass
class SeriesItem:
    name: int
    episodes: List[str]

@dataclass
class GenericInfoItem:
    name_original: str
    year: int
    genre: str
    series: List[SeriesItem]