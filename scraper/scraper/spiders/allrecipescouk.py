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

from ..items import RecipeItem


class AllrecipesukSpider(scrapy.Spider):
    name = "allrecipescouk"
    allowed_domains = ["allrecipes.co.uk"]
    root = "http://allrecipes.co.uk"
    products = [
        "Apple", "Apricot", "Asparagus", "Aubergine", "Banana", "Basil", "Beef", "Beetroot", "Blackberry",
        "Blackcurrants", "Bramley apple", "Broad bean", "Broad beans", "Broccoli", "Brussels sprouts", "Cabbage",
        "Carrot", "Cauliflower", "Cavolo nero", "Celeriac", "Celery", "Cherry", "Chervil", "Chestnut", "Chicken",
        "Chicory", "Clementine", "Cod", "Courgette", "Courgette flower", "Crab", "Cranberry", "Damson", "Date", "Duck",
        "Fennel bulb", "Fig", "Garlic", "Globe artichoke", "Goose", "Gooseberry", "Grapefruit", "Grouse", "Guinea fowl",
        "Halibut", "Jerusalem artichoke", "Kale", "Kipper", "Kohlrabi", "Lamb", "Lamb's lettuce", "Leek", "Lemon",
        "Lettuce", "Mackerel", "Marrow", "Mint", "Mussels", "Nectarine", "New potatoes", "Onion", "Orange", "Oyster",
        "Pak choi", "Parsnip", "Peach", "Pear", "Peas", "Pepper", "Plum", "Pomegranate", "Pork", "Potato", "Pumpkin",
        "Purple sprouting broccoli", "Quince", "Radicchio", "Radish", "Raspberry", "Redcurrant", "Rhubarb",
        "Runner bean", "Salmon", "Salsify", "Samphire", "Sorrel", "Spinach", "Spring greens", "Spring lamb",
        "Spring onion", "Strawberry", "Swede", "Sweet potato", "Sweetcorn", "Swiss chard", "Tomato", "Tuna", "Turkey",
        "Turnip", "Venison", "Watercress", "Watermelon", "Whiting",
    ]
    # products = ['Apple']
    recipe_selector = '//a[starts-with(@href, "http://allrecipes.co.uk/recipe/")]/@href'
    def start_requests(self):
        for product in self.products:
            url = 'http://allrecipes.co.uk/recipes/searchresults.aspx?text=%s' % product
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        s = Selector(response)
        recipes = s.xpath(self.recipe_selector).extract()
        for recipe in recipes:
            item = RecipeItem()
            query = response.url.split('o_s_trm=')[-1]
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
        ingredients = s.xpath("//span[@itemprop='ingredients']//text()").extract()
        item['ingredients'] = [unicodedata.normalize("NFKD", i.strip()) for i in ingredients]
        if item['product'].lower() not in ' '.join(ingredients).lower():
            yield None
        else:
            name = s.xpath(
                "//span[@itemprop='name']//text()").extract_first()
            item['name'] = unicodedata.normalize("NFKD", name).strip()
            item['url'] = response.url
            image_url = s.xpath(
                "//img[@class='recipe-img']/@data-imagesrc").extract_first()
            item['image_urls'] = [urljoin(text_type(self.root), text_type(image_url)).format(size=500)]
            teaser = s.xpath(
                "//p[@class='description']//text()").extract_first()
            item['teaser'] = unicodedata.normalize("NFKD", teaser).strip()
            item['additional'] = []
            item['source'] = self.name
            yield item
