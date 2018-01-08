# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from django.test import TestCase

from .models import Month

from api.init_db import MONTHS
from api.views import fetch_recipe


class AddRecipeTest(TestCase):
    """Tests for /api/v1/add-recipe/ URL."""
    def test_add_recipe_get(self):
        """Test we can't reach /api/v1/add-recipe/ with GET."""
        response = self.client.get('/api/v1/add-recipe/')
        self.assertEqual(response.status_code, 405)

    def test_add_recipe_post(self):
        """Test we can reach /api/v1/add-recipe/."""
        data = {'name': 'Spam fritter',
                'url': 'https://example.com',
                'image_url': 'https://example.com/images/spam.jpg',
                'teaser': 'No one expects the Spammish inquisition!',
                'product': 'Spam',
                }
        response = self.client.post('/api/v1/add-recipe/', data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
             response.json(),
             {u'success': True})

    def test_add_recipe_accents(self):
        """Test we /api/v1/add-recipe/ can handle accented chars."""
        data = {'name': 'Spam fritter',
                'url': 'https://example.com',
                'image_url': 'https://example.com/images/spam.jpg',
                'teaser': 'No one expects the Spámmish inquisition!',
                'product': 'Spam',
                }
        response = self.client.post('/api/v1/add-recipe/', data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
             response.json(),
             {u'success': True})


class AddProductTest(TestCase):
    """Tests for /api/v1/add-product/ URL."""
    def test_add_product_get(self):
        """Test we can't reach /api/v1/add-product/ with GET."""
        response = self.client.get('/api/v1/add-product/')
        self.assertEqual(response.status_code, 405)

    def test_add_product_post(self):
        """Test we can reach /api/v1/add-product/."""
        data = {'name': 'Spam',
                'months': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]}
        for i, name in enumerate(MONTHS, 1):
            month = Month()
            month.name = name
            month.num = i
            month.save()
        response = self.client.post('/api/v1/add-product/', data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
             response.json(),
             {u'success': True})

class GetRecipeTest(TestCase):
    
    def setUp(self):
        data = {'name': 'BBQ Spam',
                'months': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]}
        for i, name in enumerate(MONTHS, 1):
            month = Month()
            month.name = name
            month.num = i
            month.save()
        response = self.client.post('/api/v1/add-product/', data)
        self.assertEqual(response.status_code, 200)
        data = {'name': 'Summer spam',
                'url': 'https://example.com',
                'image_url': 'https://example.com/images/spam.jpg',
                'teaser': 'Great in summer!',
                'product': 'BBQ Spam',
                }
        response = self.client.post('/api/v1/add-recipe/', data)
        self.assertEqual(response.status_code, 200)
    
    def testMonthFilters(self):
        for n in 6, 7, 8:
            recipe, _product = fetch_recipe(None, n)
            self.assertEqual(recipe.get('name'), 'Summer spam')
        for n in 1, 2, 3, 4, 5, 9, 10, 11, 12:
            recipe, _product = fetch_recipe(None, 5)
            self.assertEqual(recipe, None)
            self.assertEqual(recipe, None)
