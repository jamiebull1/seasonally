# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import datetime

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import requests
from rest_framework.decorators import api_view
from six.moves.urllib.parse import urljoin

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

ACTIVE_SOURCES = {
    'legacy',
    'delicious',
    'goodfood',
}

@api_view(['POST'])
def add_recipe(request):
    params = request.POST.copy()
    print(params)
    recipe, created = Recipe.objects.update_or_create(
        url=params.get('url'),
        defaults={
            'name': params.get('name').encode('utf-8'),
            'url': params.get('url'),
            'image_url': params.get('image_url'),
            'teaser': params.get('teaser').encode('utf-8'),
            'additional': params.get('additional'),
            'ingredients': params.get('ingredients'),
            'source': params.get('source'),
        },
    )
    # get product from DB or add it if not yet present
    product, created = Product.objects.get_or_create(
        name=params.get('product')
    )
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
    tries_left = 10
    while not recipe and tries_left:
        recipe, product = fetch_recipe()
        tries_left -= 1
    return JsonResponse({'success': True, 'recipe': recipe, 'product': product.name})


def fetch_recipes(n=1):
    recipes = []
    tries_left = 10
    while len(recipes) < n and tries_left:
        recipe, _product = fetch_recipe()
        if recipe not in recipes:
            recipes.append(recipe)
        tries_left -= 1
    return recipes


def fetch_recipe_by_key(pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    return recipe


def fetch_recipe(product=None, month_num=None):
    """Fetch a random recipe from the chosen product."""
    if not product:
        product = fetch_product()
    recipes = product.recipe.values().order_by('?')
    if not month_num:
        month = fetch_month()
        month_num = month.get('month_num')
    for recipe in recipes:
        if is_valid(recipe, month_num) and is_complete(recipe):
            return recipe, product
        else:
            fetch_recipe(month_num=month_num)


def is_valid(recipe, month_num):
    """Don't return items which are invalid for some reason."""
    return all([
        is_seasonal(recipe, month_num),
        is_complete(recipe),
        is_active_source(recipe),
    ])


def is_active_source(recipe):
    """Don't return recipe items from sources we don't want to display."""
    source = recipe.get('source')  # we will remove `legacy` from ACTIVE_SOURCES eventually
    if not source:
        source = 'legacy'
    if source in ACTIVE_SOURCES:
        return True
    return False


def is_seasonal(recipe, month_num):
    """Don't return items which are clearly for other seasons."""
    teaser = recipe.get('teaser').lower()
    name = recipe.get('name').lower()
    for season in VALID_MONTHS:
        months = VALID_MONTHS[season]
        if (season in teaser or season in name) and month_num not in months:
            return False
    return True


def is_complete(recipe):
    url = recipe.get('image_url', '').strip()
    url = image_exists(url)
    name = recipe.get('name', '').strip()
    teaser = recipe.get('teaser', '').strip()
    return all([url, name, teaser])


def image_exists(url):
    url = urljoin(settings.S3_BUCKET, url + '.jpg')
    r = requests.get(url)
    return r.status_code == 200


def fetch_product(month_num=None):
    """Fetch a random seasonal product from the database."""
    if not month_num:
        month = fetch_month()
        month_num = month.get('month_num')
    try:
        return Product.objects.filter(months__num=month_num, recipe__name__isnull=False).order_by('?')[0]
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
