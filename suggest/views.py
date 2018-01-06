"""Views for the seasonal suggestions website."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import datetime

from django.shortcuts import render

from api.views import fetch_recipes


def index(request):
    """Homepage."""
    context = {}
    # fetch items for this month
    context = {'recipes': fetch_recipes(n=3)}
    today = datetime.datetime.now()
    abbr_month = today.strftime('%b').lower()
    context['abbr_month'] = abbr_month
    return render(request, 'suggest/index.html', context=context)
