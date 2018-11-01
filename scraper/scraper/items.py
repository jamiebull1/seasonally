# -*- coding: utf-8 -*-
import scrapy


class RecipeItem(scrapy.Item):
    """Details of a recipe for reuse in seasonally."""
    name = scrapy.Field()
    url = scrapy.Field()
    image_urls = scrapy.Field()
    teaser = scrapy.Field()
    product = scrapy.Field()
    ingredients = scrapy.Field()
    additional = scrapy.Field()
    source = scrapy.Field()
