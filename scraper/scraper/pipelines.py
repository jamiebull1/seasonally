# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from hashlib import sha1
import json
import logging
import os

# from PIL import Image, ImageChops
import requests
# from scrapy.pipelines.images import ImagesPipeline

logger = logging.getLogger(__name__)


# class MyImagesPipeline(ImagesPipeline):
#
#     pass
#
#
# def trim(im):
#     bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
#     diff = ImageChops.difference(im, bg)
#     diff = ImageChops.add(diff, diff, 2.0, -100)
#     bbox = diff.getbbox()
#     if bbox:
#         return im.crop(bbox)
#
# im = Image.open("bord3.jpg")
# im = trim(im)
# im.show()
#


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
            # ROOT_URL = 'http://0.0.0.0:5000'
            ROOT_URL = 'http://inseasonrecipes.co.uk'

        r = requests.post(ROOT_URL + "/api/v1/add-recipe/", data)
        if r.status_code == 200 and r.json() == {'success': True}:
            logger.debug('Post recipe succeeded')
        else:
            logger.error('Post recipe failed: %s : %s' % (r.status_code, r.json()))
        return item
