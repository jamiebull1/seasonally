# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import requests


class RecipePipeline(object):

    def process_item(self, item, spider):
        data = {
            'name': item['name'],
            'url': item['url'],
            'image_url': item['image_url'],
            'teaser': item['teaser'],
            'product': item['product'],
            }
        r = requests.post("http://127.0.0.1:8000/api/v1/add-recipe/", data)
        return item
