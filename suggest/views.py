"""Views for the seasonal suggestions website."""
import datetime

from django.shortcuts import render

from api.views import fetch_recipes
from api.views import fetch_recipe_by_key


def index(request):
    """Homepage."""
    # fetch items for this month
    context = {'recipes': fetch_recipes(n=3)}
    today = datetime.datetime.now()
    abbr_month = today.strftime('%b').lower()
    context['abbr_month'] = abbr_month
    return render(request, 'suggest/index.html', context=context)


def recipe(request):
    """Individual recipe page."""
    pk = request.GET.get('pk', 1)
    context = {'recipe': fetch_recipe_by_key(pk)}
    today = datetime.datetime.now()
    abbr_month = today.strftime('%b').lower()
    context['abbr_month'] = abbr_month
    return render(request, 'suggest/recipe.html', context=context)


def infographic(request):
    """Infographic page."""
    today = datetime.datetime.now()
    abbr_month = today.strftime('%b').lower()
    context = {
        'abbr_month': abbr_month,
        'full_month': today.strftime('%B').capitalize(),
        'wordcloud': f'images/wordclouds/{abbr_month}.png',
    }
    return render(request, 'suggest/infographic.html', context=context)
