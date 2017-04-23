"""Views for the seasonal suggestions website."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import datetime

from django.shortcuts import render

from api.models import Product


def index(request):
    """Homepage."""
    today = datetime.datetime.now()
    abbr_month = today.strftime('%b').lower()
    month = today.strftime('%B')
    context = {'abbr_month': abbr_month, 'month': month}
    month_num = int(today.strftime('%m'))
    context['recipes'] = []
    # fetch items for this month
    while len(context['recipes']) < 3:
        # choose a product
        product = None
        while not product:
            product = fetch_product(month_num)
        # fetch a recipe using the product
        recipe = fetch_recipe(product)
        if recipe and recipe not in context['recipes']:
            context['recipes'].append(recipe)
    return render(request, 'suggest/index.html', context=context)


def fetch_product(month_num):
    """Fetch a random seasonal product from the database."""
    try:
        return Product.objects.filter(months__num=month_num).order_by('?')[0]
    except IndexError:
        return

def fetch_recipe(product):
    """Fetch a random recipe from the chosen product."""
    try:
        return product.recipe.values().order_by('?')[0]
    except IndexError:
        return