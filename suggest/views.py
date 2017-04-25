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
    context = {}
    month = fetch_month()
    context.update(month)
    context['recipes'] = []
    # fetch items for this month
    while len(context['recipes']) < 3:
        # choose a product
        product = None
        product = fetch_product(context.get('month_num)'))
        # fetch a recipe using the product
        recipe = fetch_recipe(product)
        if recipe and recipe not in context['recipes']:
            context['recipes'].append(recipe)
    return render(request, 'suggest/index.html', context=context)


def fetch_month():
    """Fetch the current month."""
    today = datetime.datetime.now()
    abbr_month = today.strftime('%b').lower()
    month = today.strftime('%B')
    month_num = int(today.strftime('%m'))
    month = {'abbr_month': abbr_month, 'month': month, 'month_num': month_num}
    return month


def fetch_product(month_num=None):
    """Fetch a random seasonal product from the database."""
    if not month_num:
        month = fetch_month()
        month_num = month.get('month_num')
    try:
        return Product.objects.filter(months__num=month_num).order_by('?')[0]
    except IndexError:
        return fetch_product(month_num)


def fetch_recipe(product=None):
    """Fetch a random recipe from the chosen product."""
    if not product:
        product = fetch_product()
    try:
        return product.recipe.values().order_by('?')[0]
    except IndexError:
        return fetch_recipe(product)
