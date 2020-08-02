from .production import *
try:
    from scraping_service.settings.local_settings import *
except:
    print('local.py does not exsists')
    pass