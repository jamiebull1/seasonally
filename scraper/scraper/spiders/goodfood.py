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


class GoodfoodSpider(scrapy.Spider):
    name = "goodfood"
    allowed_domains = ["bbcgoodfood.com"]
    root = "https://www.bbcgoodfood.com"
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
    products = ['Apple']
    selectors = {
        'recipe': '//a[starts-with(@href, "/recipes/") and not (contains(@href, "/category/")) and not '
                  '(contains(@href, "/collection/"))]/@href',
        'ingredients': "//li[@class='ingredients-list__item']//text()[not(ancestor::span)]",
        'name': ".recipe-header__title::text",
        'image_url': "//img[@itemprop='image']/@src",
        'teaser': "//div[@class='recipe-header__description']//text()",
        'additional': '//ul[@class="additional-info"]//text()',
        }

    def start_requests(self):
        for product in self.products:
            url = 'http://www.bbcgoodfood.com/search/recipes?query=%s' % product
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        s = Selector(response)
        recipes = s.xpath(self.selectors['recipe']).extract()
        for recipe in recipes:
            item = RecipeItem()
            query = response.url.split('query=')[-1]
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
        item = response.meta['item']
        ingredients = s.xpath(self.selectors['ingredients']).extract()
        ingredients = make_list(ingredients)
        item['ingredients'] = [
            unicodedata.normalize("NFKD", i.strip())
            for i in ingredients if i.strip()
        ]
        if item['product'].lower() not in ' '.join(ingredients).lower():
            yield None
        else:
            name = s.css(self.selectors['name']).extract_first()
            item['name'] = unicodedata.normalize("NFKD", name)
            item['url'] = response.url
            image_url = s.xpath(self.selectors['image_url']).extract_first()
            item['image_urls'] = [urljoin(text_type(self.root), text_type(image_url))]
            teaser = s.xpath(self.selectors['teaser']).extract_first()
            item['teaser'] = unicodedata.normalize("NFKD", teaser)
            item['additional'] = s.xpath(self.selectors['additional']).extract()
            yield item


def make_list(ingredients):
    as_list = []
    item = ''
    for i, text in enumerate(ingredients):
        if not item:
            item = text
        else:
            item += text
        if item.endswith(' '):
            continue
        try:
            if ingredients[i+1].startswith(' ') or ingredients[i+1].startswith(','):
                continue
        except IndexError:
            as_list.append(item)
            return as_list
        as_list.append(item)
        item = ''
