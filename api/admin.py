from django.contrib import admin

from .models import Product
from .models import Recipe
from .models import Month


# Register your models here.
admin.site.register(Product)
admin.site.register(Recipe)
admin.site.register(Month)
