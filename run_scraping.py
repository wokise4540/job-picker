import asyncio
import codecs
import os, sys
import datetime as dt

from django.contrib.auth import get_user_model
from django.db import DatabaseError


proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "scraping_service.settings"

import django
django.setup()

from scraping.parsers import *
from scraping.models import Vacansy, Error, Url, City, Language

User = get_user_model()

parsers = (
    (yandex_talents, 'https://talents.yandex.ru/vacancy/{city}/search/{language}'),
    (worki, 'https://{city}.worki.ru/?keyWord={language}'),
    (rabota, 'https://{city}.rabota.ru/vacancy/?query={language}&sort=date')
)

jobs, errors = [], []


def get_vacancies():
    cities = City.objects.filter().values()
    languages = Language.objects.filter().values()
    for language in languages:
        language_slug = language['slug']
        language_id = language['id']
        for city in cities:
            city_slug = city['slug']
            city_id = city['id']
            for func, url in parsers:
                url = url.format(city=city_slug, language=language_slug)
                job, error = func(url, language=language_id, city=city_id)
                jobs.extend(job)
                errors.extend(error)
    return jobs, errors


def save_vacancies(jobs, errors):
    for job in jobs:
        try:
            v = Vacansy(**job)
            v.save()
        except DatabaseError:
            pass
    if errors:
        qs = Error.objects.filter(timestamp=dt.date.today())
        if qs.exists():
            err = qs.first()
            err.data.update({'errors': errors})
            err.save()
        else:
            er = Error(data=f'errors: {errors}').save()


jobs, errors = get_vacancies()
save_vacancies(jobs, errors)