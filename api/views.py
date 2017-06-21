# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import datetime
import json

from django.http import JsonResponse
from rest_framework.decorators import api_view

from .models import Recipe, Product, Month


VALID_MONTHS = {
    'easter': [4, 5],
    'christmas': [12],
    'spring': [3, 4, 5],
    'summer': [6, 7, 8],
    'autumn': [9, 10, 11],
    'winter': [12, 1, 2],
    'halloween': [10],
    'festive': [12],
    }


@api_view(['POST'])
def add_recipe(request):
    params = request.POST.copy()
    recipe = Recipe()
    recipe.name = params.get('name').encode('utf-8')
    recipe.url = params.get('url')
    recipe.image_url = params.get('image_url')
    recipe.teaser = params.get('teaser').encode('utf-8')
    recipe.additional = json.dumps(params.getlist('additional'))
    recipe.save()
    # get product from DB or add it if not yet present
    product = Product.objects.filter(name=params.get('product')).first()
    if not product:
        product = Product()
        product.name = params.get('product')
        product.save()
    # add new recipe to product recipes
    product.recipe.add(recipe)
    return JsonResponse({'success': True})


@api_view(['POST'])
def add_product(request):
    params = request.POST.copy()
    product = Product()
    product.name = params.get('name').encode('utf-8')
    product.save()
    months = Month.objects.filter(num__in=params.getlist('months'))
    product.months.set(months)
    product.save()
    return JsonResponse({'success': True})


@api_view(['POST'])
def add_month(request):
    params = request.POST.copy()
    month = Month()
    month.name = params.get('name')
    month.num = params.get('num')
    month.save()
    return JsonResponse({'success': True})


@api_view(['GET'])
def recipe(request):
    recipe = None
    count = 0
    while not recipe and count < 20:
        recipe = fetch_recipe()
        count += 1
    return JsonResponse({'success': True, 'recipe': recipe})


def fetch_recipe(product=None, month_num=None):
    """Fetch a random recipe from the chosen product."""
    if not product:
        product = fetch_product()
    recipes = product.recipe.values().order_by('?')
    if not month_num:
        month = fetch_month()
        month_num = month.get('month_num')
    for recipe in recipes:
        if is_valid(recipe, month_num):
            return recipe
        else:
            fetch_recipe(month_num=month_num)


def is_valid(recipe, month_num):
    """Don't return items which are clearly for other seasons."""
    if not recipe.get('image_url', False):
        return False
    teaser = recipe.get('teaser').lower()
    for season in VALID_MONTHS:
        months = VALID_MONTHS[season]
        if season in teaser and month_num not in months:
            return False
    return True


def fetch_product(month_num=None):
    """Fetch a random seasonal product from the database."""
    if not month_num:
        month = fetch_month()
        month_num = month.get('month_num')
    try:
        return Product.objects.filter(months__num=month_num).order_by('?')[0]
    except IndexError:
        return fetch_product(month_num)


def fetch_month():
    """Fetch the current month."""
    today = datetime.datetime.now()
    abbr_month = today.strftime('%b').lower()
    month = today.strftime('%B')
    month_num = int(today.strftime('%m'))
    month = {'abbr_month': abbr_month, 'month': month, 'month_num': month_num}
    return month
