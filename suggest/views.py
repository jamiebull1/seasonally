"""Views for the seasonal suggestions website."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from django.shortcuts import render

from api.views import fetch_recipe


def index(request):
    """Homepage."""
    context = {}
    # fetch items for this month
    context = {'recipes': [fetch_recipe() for _i in range(3)]}
    return render(request, 'suggest/index.html', context=context)
