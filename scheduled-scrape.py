import subprocess
import os

os.chdir('scraper/scraper')
# veganrecipeclub
subprocess.call(['scrapy', 'crawl', 'veganrecipeclub'])
# goodfood
subprocess.call(['scrapy', 'crawl', 'goodfood'])
# jamieoliver
subprocess.call(['scrapy', 'crawl', 'jamieoliver'])
# goodfood
subprocess.call(['scrapy', 'crawl', 'goodfood'])
# allrecipescouk
subprocess.call(['scrapy', 'crawl', 'allrecipescouk'])
# delicious
subprocess.call(['scrapy', 'crawl', 'delicious'])
