# -*- coding: utf-8 -*-
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


class DeliciousSpider(scrapy.Spider):
    name = "delicious"
    allowed_domains = ["deliciousmagazine.co.uk"]
    root = "http://www.deliciousmagazine.co.uk"
    products = common.products
    # products = ['Apple']
    recipe_selector = '//a[starts-with(@href, "http://www.deliciousmagazine.co.uk/recipes/")]/@href'
    def start_requests(self):
        for product in self.products:
            url = 'http://www.deliciousmagazine.co.uk/?s={product}&fq=type%3Aam_recipe'.format(product=product)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        s = Selector(response)
        recipes = s.xpath(self.recipe_selector).extract()
        for recipe in recipes:
            item = RecipeItem()
            query = response.url.split('s=')[-1].split('&fq=')[0]
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
        item['ingredients'] = [
            unicodedata.normalize("NFKD", i.strip())
            for i in s.xpath("//div[@class='ingredient-box']//text()").extract() if i.strip()
        ][1:]
        if item['product'].lower() not in ' '.join(item['ingredients']).lower():
            yield None
        else:
            name = s.xpath("//h1[@class='post-title']//text()").extract_first()
            item['name'] = unicodedata.normalize("NFKD", name).strip()
            item['url'] = response.url
            image_url = s.xpath("//img[@class='attachment-recipes-featured wp-post-image']/@src").extract_first()
            item['image_urls'] = [urljoin(text_type(self.root), text_type(image_url))]
            teaser = s.xpath("//span[@class='teaser_large']//text()").extract_first()
            item['teaser'] = unicodedata.normalize("NFKD", teaser).strip()
            item['additional'] = []
            item['source'] = self.name
            yield item
