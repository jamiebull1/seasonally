# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import scrapy


class RecipeItem(scrapy.Item):
    """Details of a recipe for reuse in seasonally."""
    name = scrapy.Field()
    url = scrapy.Field()
    image_urls = scrapy.Field()
    teaser = scrapy.Field()
    product = scrapy.Field()
    ingredients = scrapy.Field()
