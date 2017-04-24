# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import requests
from hashlib import sha1


class RecipePipeline(object):

    def process_item(self, item, spider):
        image_url = item['image_urls'][0]
        image_url = sha1(image_url).hexdigest()
        image_url = '/images/full/%s' % image_url
        data = {
            'name': item['name'],
            'url': item['url'],
            'image_url': image_url,
            'teaser': item['teaser'],
            'product': item['product'],
            }
        r = requests.post("http://127.0.0.1:8000/api/v1/add-recipe/", data)
        return item
