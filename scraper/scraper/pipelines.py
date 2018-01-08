# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import json
import os

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
            'additional': json.dumps({'items': item['additional']}),
            'ingredients': json.dumps({'items': item['ingredients']}),
            'source': item['source'],
            }
        PRODUCTION = os.environ.get('DJANGO_PRODUCTION', False)
        if PRODUCTION:
            ROOT_URL = 'http://inseasonrecipes.co.uk'
        else:
            ROOT_URL = 'http://0.0.0.0:5000'
            ROOT_URL = 'http://inseasonrecipes.co.uk'

        r = requests.post(ROOT_URL + "/api/v1/add-recipe/", data)
        if r.status_code == 200 and r.json() == {'success': True}:
            logger.debug('Post recipe succeeded')
        else:
            logger.error('Post recipe failed: %s : %s' % (r.status_code, r.json()))
        return item
