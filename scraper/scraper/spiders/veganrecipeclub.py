# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import unicodedata

from scrapy import Request
from scrapy import Selector
import scrapy
from scrapy.shell import inspect_response
from six import text_type
from six.moves import urllib
from six.moves.urllib.parse import urljoin

from . import common
from ..items import RecipeItem


class VeganrecipeclubSpider(scrapy.Spider):
    name = "veganrecipeclub"
    allowed_domains = ["veganrecipeclub.org.uk"]
    root = "https://www.veganrecipeclub.org.uk"
    products = common.products
    # products = ['Apple']
    recipe_selector = '//a[starts-with(@href, "/recipes/")]/@href'
    def start_requests(self):
        for product in self.products:
            url = 'https://www.veganrecipeclub.org.uk/search?search_api_views_fulltext=%s' % product
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        s = Selector(response)
        recipes = s.xpath(self.recipe_selector).extract()
        for recipe in recipes:
            item = RecipeItem()
            query = response.url.split('search_api_views_fulltext=')[-1]
            product = urllib.parse.unquote(query)
            item['product'] = unicodedata.normalize("NFKD", product)
            request = Request(
                urljoin(self.root, recipe),
                callback=self.parse_recipe,
                meta={'item': item}
                )
            yield request

    def parse_recipe(self, response):
        s = Selector(response)
        # inspect_response(response, self)
        item = response.meta['item']
        ingredients = s.xpath("//h3[@class='label-above']/following-sibling::ul/li//text()").extract()
        item['ingredients'] = [unicodedata.normalize("NFKD", i.strip()) for i in ingredients]
        if item['product'].lower() not in ' '.join(ingredients).lower():
            yield None
        else:
            name = s.xpath("//h1//text()").extract_first()
            item['name'] = unicodedata.normalize("NFKD", name).strip()
            item['url'] = response.url
            image_url = s.xpath("//div[@class='recipe-image-wrapper']/img/@src").extract_first()
            item['image_urls'] = [urljoin(text_type(self.root), text_type(image_url)).format(size=500)]
            teaser = s.xpath("//div[@class='field-items']/div/p/text()").extract_first()
            item['teaser'] = unicodedata.normalize("NFKD", teaser).strip()
            item['additional'] = ['vegan']
            item['source'] = self.name
            yield item
