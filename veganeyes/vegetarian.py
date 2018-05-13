import json
import requests

from api.models import Recipe

def get_recipe():
    query = Recipe.objects.filter(teaser__icontains='vegan')
    res = query.first()
    product = res['product'].lower()
    recipe = res['recipe']
    return product, recipe


def munge_recipe(product, recipe):
    name = recipe['name']
    teaser = recipe['teaser']
    ingredients = json.loads(recipe['ingredients'])['items']
    munged = f'{product} {name} {teaser} {" ".join(ingredients)}'.lower()
    return munged


def check_recipe():
    test_string = munge_recipe(*get_recipe())
    print(test_string)

def get_vegan_recipe():
    while True:
        product, recipe = get_recipe()
        munged = munge_recipe(product, recipe)
        if 'vegan' in munged:
            return recipe


if __name__ == "__main__":
    print(get_vegan_recipe())
