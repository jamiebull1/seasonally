# -*- coding: utf-8 -*-
import datetime
import json
import os

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import requests
from rest_framework.decorators import api_view
from six.moves.urllib.parse import urljoin
import structlog

from .models import Recipe, Product, Month

log = structlog.get_logger()

VALID_MONTHS = {
    'easter': [4, 5],
    'christmas': [12],
    'spring': [3, 4, 5],
    'summer': [6, 7, 8],
    'autumn': [9, 10, 11],
    'winter': [12, 1, 2],
    'halloween': [10],
    'festive': [12],
    'diwali': [10],
    'bonfire night': [10],
    'fathers': [6],
    'mothers': [3, 5],
    'bonfire': [10],
    'stgeorge': [4],
    'stgeorgesday': [4],
    'newyear': [12],
    'valentine': [2],
    }

ACTIVE_SOURCES = os.getenv('ACTIVE_SOURCES', 'legacy delicious goodfood bbcgoodfood veganrecipeclub').split()


@api_view(['POST'])
def add_recipe(request):
    params = request.POST.copy()
    seasonal_recipe, created = Recipe.objects.update_or_create(
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
    seasonal_product, created = Product.objects.get_or_create(
        name=params.get('product')
    )
    # add new recipe to product recipes
    seasonal_product.recipe.add(seasonal_recipe)
    return JsonResponse({'success': True})


@api_view(['POST'])
def add_product(request):
    params = request.POST.copy()
    seasonal_product = Product()
    seasonal_product.name = params.get('name').encode('utf-8')
    seasonal_product.save()
    months = Month.objects.filter(num__in=params.getlist('months'))
    seasonal_product.months.set(months)
    seasonal_product.save()
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
    seasonal_recipe = None
    seasonal_product = None
    tries_left = 3
    while not seasonal_recipe and tries_left:
        seasonal_recipe, seasonal_product = fetch_recipe()
        tries_left -= 1
    if not seasonal_recipe:
        res = JsonResponse({'success': False, 'recipe': None, 'product': None})
    else:
        res = JsonResponse({'success': True, 'recipe': seasonal_recipe, 'product': seasonal_product.name})
    return res


@api_view(['GET'])
def product(request):
    """Fetch a random seasonal product from the database."""
    seasonal_product = fetch_product()
    return JsonResponse({'success': True, 'product': seasonal_product.name})


def fetch_recipes(n=1):
    recipes = []
    tries_left = 3
    while len(recipes) < n and tries_left:
        seasonal_recipe, _product = fetch_recipe()
        if seasonal_recipe not in recipes:
            recipes.append(seasonal_recipe)
        tries_left -= 1
    return recipes


def fetch_recipe_by_key(pk):
    seasonal_recipe = get_object_or_404(Recipe, pk=pk)
    try:
        seasonal_recipe.views += 1
    except TypeError:
        seasonal_recipe.views = 1
    seasonal_recipe.save(update_fields=["views"])
    return seasonal_recipe


def fetch_recipe_by_slug(slug):
    seasonal_recipe = get_object_or_404(Recipe, slug=slug)
    try:
        seasonal_recipe.views += 1
    except TypeError:
        seasonal_recipe.views = 1
    seasonal_recipe.save(update_fields=["views"])
    return seasonal_recipe


def fetch_recipe(seasonal_product=None, month_num=None):
    """Fetch a random recipe from the chosen product."""
    if not seasonal_product:
        seasonal_product = fetch_product()
    recipes = seasonal_product.recipe.values().order_by('?')
    if not month_num:
        month = fetch_month()
        month_num = month.get('month_num')
    for seasonal_recipe in recipes:
        if is_valid(seasonal_recipe, month_num) and is_complete(seasonal_recipe):
            return seasonal_recipe, seasonal_product
        else:
            return fetch_recipe(month_num=month_num)


def is_valid(seasonal_recipe, month_num):
    """Don't return items which are invalid for some reason."""
    return all([
        is_seasonal(seasonal_recipe, month_num),
        is_complete(seasonal_recipe),
        is_active_source(seasonal_recipe),
    ])


def is_active_source(seasonal_recipe):
    """Don't return recipe items from sources we don't want to display."""
    source = seasonal_recipe.get('source')
    if not source:
        source = 'legacy'
    if source in ACTIVE_SOURCES:
        log.debug('api.recipe.is_valid', active=True)
        return True
    log.debug('api.recipe.is_valid', active=False)
    return False


def is_seasonal(seasonal_recipe, month_num):
    """Don't return items which are clearly for other seasons."""
    teaser = seasonal_recipe.get('teaser').lower()
    name = seasonal_recipe.get('name').lower()
    tags = [tag.lower() for tag in json.loads(seasonal_recipe.get('additional'))['items']]
    for season in VALID_MONTHS:
        months = VALID_MONTHS[season]
        if (season in teaser or season in name or season in ' '.join(tags)) and month_num not in months:
            log.debug('api.recipe.is_valid', seasonal=False)
            return False
    log.debug('api.recipe.is_valid', seasonal=True)
    return True


def is_complete(seasonal_recipe):
    url = seasonal_recipe.get('image_url', '').strip()
    url = image_exists(url)
    name = seasonal_recipe.get('name', '').strip()
    teaser = seasonal_recipe.get('teaser', '').strip()
    complete = all([url, name, teaser])
    log.debug('api.recipe.is_valid', complete=complete)
    return complete


def image_exists(url):
    url = urljoin(settings.S3_BUCKET, url + '.jpg')
    r = requests.get(url)
    img_exists = r.status_code == 200
    log.debug('api.recipe.is_valid', img_exists=img_exists)
    return img_exists


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
