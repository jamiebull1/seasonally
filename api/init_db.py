# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os

import requests

PRODUCTION = os.environ.get('DJANGO_PRODUCTION', False)
if PRODUCTION:
    ROOT_URL = 'http://inseasonrecipes.co.uk'
else:
    ROOT_URL = 'http://0.0.0.0:5000'

PRODUCTS = {
    "Apple": [1, 2, 9, 10, 11, 12],
    "Apricot": [5, 6, 7, 8, 9],
    "Asparagus": [5, 6, 7],
    "Aubergine": [5, 6, 7, 8, 9, 10],
    "Banana": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    "Basil": [6, 7, 8],
    "Beef": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    "Beetroot": [1, 7, 8, 9, 10, 11, 12],
    "Blackberry": [7, 8, 9, 10],
    "Blackcurrants": [5, 6, 7],
    "Bramley apple": [1, 2, 3, 11, 12],
    "Broad bean": [6, 7, 8, 9],
    "Broccoli": [7, 8, 9, 10],
    "Brussels sprouts": [1, 2, 3, 10, 11, 12],
    "Cabbage": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    "Carrot": [5, 6, 7, 8, 9],
    "Cauliflower": [1, 2, 3, 4, 12],
    "Cavolo nero": [6, 7, 8, 9, 10],
    "Celeriac": [1, 2, 3, 4, 9, 10, 11, 12],
    "Celery": [1, 2, 7, 8, 9, 10, 11, 12],
    "Cherry": [6, 7],
    "Chervil": [5, 6, 7, 8, 9],
    "Chestnut": [1, 9, 10, 11, 12],
    "Chicken": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    "Chicory": [1, 2, 3],
    "Clementine": [1, 2, 11, 12],
    "Cod": [1, 2, 3, 4],
    "Courgette": [6, 7, 8, 9],
    "Courgette flower": [6, 7, 8],
    "Crab": [4, 5, 6, 7, 8, 9, 10, 11],
    "Cranberry": [10, 11, 12],
    "Damson": [8, 9],
    "Date": [1, 10, 11, 12],
    "Duck": [10, 11, 12],
    "Fennel bulb": [6, 7, 8, 9],
    "Fig": [7, 8, 9, 10],
    "Garlic": [6, 7, 8, 9, 10],
    "Globe artichoke": [5, 6, 7, 8, 9, 10, 11],
    "Goose": [1, 8, 9, 10, 11, 12],
    "Gooseberry": [5, 6, 7, 8, 9],
    "Grapefruit": [1, 2, 3, 4, 5, 12],
    "Grouse": [8, 9, 10, 11, 12],
    "Guinea fowl": [8, 9, 10, 11],
    "Halibut": [3, 4, 5, 6, 7, 8, 9],
    "Jerusalem artichoke": [1, 2, 3, 10, 11, 12],
    "Kale": [1, 2, 9, 10, 11, 12],
    "Kipper": [5, 6, 7, 8, 9],
    "Kohlrabi": [7, 8, 9, 10, 11],
    "Lamb": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    "Lamb's lettuce": [5, 6, 7, 8, 9, 10, 11],
    "Leek": [1, 2, 3, 9, 10, 11, 12],
    "Lemon": [1, 2, 3],
    "Lettuce": [4, 5, 6, 7, 8, 9, 10, 11, 12],
    "Mackerel": [5, 6, 7, 8, 9, 10],
    "Marrow": [7, 8, 9],
    "Mint": [5, 6, 7, 8, 9],
    "Mussels": [1, 2, 3, 10, 11, 12],
    "Nectarine": [5, 6, 7, 8, 9],
    "New potatoes": [4, 5, 6, 7],
    "Onion": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    "Orange": [1, 2, 3],
    "Oyster": [1, 2, 3, 4, 8, 9, 10, 11, 12],
    "Pak choi": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    "Parsnip": [1, 2, 3, 9, 10, 11, 12],
    "Peach": [7, 8, 9],
    "Pear": [1, 9, 10, 11, 12],
    "Peas": [4, 5, 6, 7, 8, 9, 10, 11],
    "Pepper": [2, 3, 4, 5, 6, 7, 8, 9, 10],
    "Plum": [8, 9, 10],
    "Pomegranate": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    "Pork": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    "Potato": [3, 4, 5, 6, 7],
    "Pumpkin": [9, 10, 11, 12],
    "Purple sprouting broccoli": [1, 2, 3, 4],
    "Quince": [9, 10, 11, 12],
    "Radicchio": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    "Radish": [4, 5, 6, 7, 8, 9, 10],
    "Raspberry": [6, 7, 8, 9],
    "Redcurrant": [6, 7, 8, 9],
    "Rhubarb": [1, 2, 3, 4, 5, 6],
    "Runner bean": [6, 7, 8, 9, 10, 11],
    "Salmon": [3, 4, 5, 6, 7, 8, 9],
    "Salsify": [1, 9, 10, 11, 12],
    "Samphire": [7, 8],
    "Sorrel": [3, 4, 5, 6, 7, 8, 9],
    "Spinach": [3, 4, 5, 6, 7, 8, 9],
    "Spring greens": [3, 4, 5, 6],
    "Spring lamb": [2, 3, 4, 5, 6],
    "Spring onion": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    "Strawberry": [5, 6, 7, 8, 9],
    "Swede": [1, 2, 10, 11, 12],
    "Sweet potato": [1, 2, 3, 10, 11, 12],
    "Sweetcorn": [8, 9],
    "Swiss chard": [7, 8, 9, 10, 11],
    "Tomato": [5, 6, 7, 8, 9, 10],
    "Tuna": [5, 6, 7, 8, 9],
    "Turkey": [12],
    "Turnip": [1, 2, 10, 11, 12],
    "Venison": [1, 2, 10, 11, 12],
    "Watercress": [3, 4, 5, 6, 7, 8, 9],
    "Watermelon": [6, 7, 8],
    "Whiting": [1, 2, 6, 7, 8, 9, 10, 11, 12]
    }

MONTHS = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
    ]

if __name__ == "__main__":
    for i, month in enumerate(MONTHS, 1):
        data = {'name': month, 'num': i}
        r = requests.post(ROOT_URL + "/api/v1/add-month/", data)
    for product in PRODUCTS:
        data = {'name': product, 'months': PRODUCTS.get(product)}
        print(product)
        print(PRODUCTS.get(product))
        r = requests.post(ROOT_URL + "/api/v1/add-product/", data)
