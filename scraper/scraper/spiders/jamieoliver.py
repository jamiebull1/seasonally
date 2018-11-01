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


class JamieOliverSpider(scrapy.Spider):
    name = "jamieoliver"
    allowed_domains = ["jamieoliver.com"]
    root = "https://www.jamieoliver.com"
    products = common.products
    # products = ['Apple']
    recipe_selector = '//a[starts-with(@href, "http://www.jamieoliver.com/recipes/")]/@href'
    def start_requests(self):
        for product in self.products:
            url = 'https://www.jamieoliver.com/search/?s=%s' % product
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        s = Selector(response)
        recipes = s.xpath(self.recipe_selector).extract()
        for recipe in recipes:
            item = RecipeItem()
            query = response.url.split('?s=')[-1]
            product = urllib.parse.unquote(query)
            item['product'] = unicodedata.normalize("NFKD", product)
            request = Request(
                recipe,
                callback=self.parse_recipe,
                meta={'item': item}
                )
            yield request

    def parse_recipe(self, response):
        s = Selector(response)
        # inspect_response(response, self)
        item = response.meta['item']
        ingredients = s.xpath("//ul[@class='ingred-list ']/li/text()").extract()
        item['ingredients'] = [' '.join(unicodedata.normalize("NFKD", i.strip()).split()) for i in ingredients]
        if item['product'].lower() not in ' '.join(ingredients).lower():
            yield None
        else:
            name = s.xpath("//h1/text()").extract_first()
            item['name'] = unicodedata.normalize("NFKD", name).strip()
            item['url'] = response.url
            image_url = s.xpath("//source[@media='(min-width: 1200px)']/@srcset").extract_first()
            item['image_urls'] = [urljoin(text_type(self.root), text_type(image_url)).format(size=500)]
            subheading = s.xpath("//p[@class='subheading hidden-xs']//text()").extract_first()
            subheading = unicodedata.normalize("NFKD", subheading).strip() if subheading else ''
            teaser = s.xpath("//div[@class='recipe-intro']//text()").extract_first()
            teaser = unicodedata.normalize("NFKD", teaser).strip() if teaser else ''
            teaser = teaser.replace('“', '')
            item['teaser'] = '. '.join([subheading, teaser]) if subheading else teaser
            additional = s.xpath("//div[@class='tags-list']/a//text()").extract()
            item['additional'] = [unicodedata.normalize("NFKD", a.strip()) for a in additional]
            item['source'] = self.name
            yield item
