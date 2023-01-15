"""Views for the seasonal suggestions website."""
import datetime

from django.shortcuts import render, redirect

from api.views import fetch_recipes, fetch_recipe_by_slug
from api.views import fetch_recipe_by_key
from seasonally.settings import ADSENSE_CODE


def index(request):
    """Homepage."""
    # fetch items for this month
    context = {'recipes': fetch_recipes(n=3)}
    today = datetime.datetime.now()
    abbr_month = today.strftime('%b').lower()
    context['abbr_month'] = abbr_month
    context['adsense_code'] = ADSENSE_CODE
    return render(request, 'suggest/index.html', context=context)


def recipe(request, slug=None):
    """Individual recipe page."""
    if slug:
        context = {'recipe': fetch_recipe_by_slug(slug)}
    else:
        pk = request.GET.get('pk', 1)
        slug = fetch_recipe_by_key(pk).slug
        return redirect(f"/recipe/{slug}/")
    today = datetime.datetime.now()
    abbr_month = today.strftime('%b').lower()
    context['abbr_month'] = abbr_month
    context['adsense_code'] = ADSENSE_CODE
    return render(request, 'suggest/recipe.html', context=context)


def infographic(request):
    """Infographic page."""
    today = datetime.datetime.now()
    abbr_month = today.strftime('%b').lower()
    context = {
        'abbr_month': abbr_month,
        'full_month': today.strftime('%B').capitalize(),
        'wordcloud': f'images/wordclouds/{abbr_month}.png',
        'adsense_code': ADSENSE_CODE,
    }
    return render(request, 'suggest/infographic.html', context=context)
