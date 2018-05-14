# seasonally
A site collecting scraping recipes and presenting them when ingredients
are in season.

### Database admin

Need to run `python api/init_db.py` when setting up a new database. This populates all the months and products which are
in season in those months.

To run the scraper, you need to have the AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY env vars set. These are in the
Heroku config settings.

Database backups for the past 7 days are stored automatically.
