from seasonally.settings import *

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

DEBUG = False
ALLOWED_HOSTS = [u'seasonally.pythonanywhere.com', u'127.0.0.1']

# set all recommended security settings unrelated to SSL
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "DENY"
