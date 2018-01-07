import subprocess
import os

os.chdir('scraper/scraper')
# goodfood
subprocess.call(['scrapy', 'crawl', 'goodfood'])
# allrecipescouk
subprocess.call(['scrapy', 'crawl', 'allrecipescouk'])
