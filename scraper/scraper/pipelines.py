# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import requests
from hashlib import sha1
import logging

logger = logging.getLogger(__name__)


class RecipePipeline(object):

    def process_item(self, item, spider):
        image_url = item['image_urls'][0]
        image_url = sha1(image_url.encode('utf-8')).hexdigest()
        image_url = '/images/full/%s' % image_url
        data = {
            'name': item['name'],
            'url': item['url'],
            'image_url': image_url,
            'teaser': item['teaser'],
            'product': item['product'],
            'additional': item['additional'],
            'ingredients': item['ingredients'],
            }
        r = requests.post("https://seasonal-ly.herokuapp.com/api/v1/add-recipe/",data)
        if r.status_code == 200 and r.json() == {'success': True}:
            logger.debug('Post recipe succeeded')
        else:
            logger.error('Post recipe failed: %s : %s' % (r.status_code, r.json()))
        return item
