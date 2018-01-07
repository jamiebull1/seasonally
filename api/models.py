from __future__ import unicode_literals

import json

from django.contrib.postgres.fields import JSONField, ArrayField
from django.db import models


class Month(models.Model):
    """Model representing a month."""
    name = models.CharField(max_length=9)
    num = models.IntegerField()

    def __unicode__(self):
        """Unicode representation for admin site."""
        return u"{0}".format(self.name)


class Recipe(models.Model):
    """Model representing a recipe on another site."""
    name = models.CharField(max_length=200)
    url = models.URLField(unique=True)
    image_url = models.URLField()
    teaser = models.CharField(max_length=500)
    additional = JSONField(null=True, blank=True)
    ingredients = JSONField(null=True, blank=True)

    def __unicode__(self):
        """Unicode representation for admin site."""
        return u"{0}".format(self.name)

    def get_ingredients(self):
        return json.loads(self.ingredients)['items']

class Product(models.Model):
    """Model representing a seasonal product."""
    name = models.CharField(max_length=30)
    months = models.ManyToManyField(Month)  # available in several months
    recipe = models.ManyToManyField(Recipe)  # belong to several recipes

    def __unicode__(self):
        """Unicode representation for admin site."""
        return u"{0}".format(self.name)
