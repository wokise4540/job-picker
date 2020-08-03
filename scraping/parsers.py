import requests
import codecs
from bs4 import BeautifulSoup as BS
from random import randint

__all__ = ('yandex_talents', 'rabota', 'worki')

headers = [{"User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"},
           {"User-Agent": "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"},
           {"User-Agent": "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"}
           ]


def worki(url, city=None, language=None):
    jobs = []
    errors = []
    domain = "https://" + url.split('/')[2]
    if url:
        resp = requests.get(url, headers[randint(0, len(headers) - 1)])
        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            main_div = soup.select_one('div[class^="JobsFeedPage_feed"]')
            if main_div:
                div_lst = main_div.select('div[data-test-id="JobCard"]')
                for div in div_lst:
                    title = div.select_one('a[class^="jobCard_profession"]')
                    href = title['href']
                    cont = div.select_one('div[class^="jobCard_description"]')
                    content = cont.text
                    company = 'No name'
                    a = div.select_one('a[class^="jobCard_title"]')
                    if a:
                        company = a.text
                    jobs.append({'title': title.text, 'url': domain + href,
                                 'description': content, 'company': company,
                                 'city_id': city, 'language_id': language})
            else:
                errors.append({'url': url, 'title': 'Div does not exists'})
        else:
            errors.append({'url': url, 'title': 'Page do not response'})

    return jobs, errors


def yandex_talents(url, city=None, language=None):
    jobs = []
    errors = []
    domain = "https://" + url.split('/')[2]
    if url:
        resp = requests.get(url, headers[randint(0, len(headers) - 1)])
        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            main_div = soup.select_one('div[class="SearchResults-Vacancies"]')
            if main_div:
                article_lst = main_div.select('article[class="VacancyItem"]')
                for article in article_lst:
                    title = article.select_one('h2[class="VacancyItem-Title"]')
                    a = article.select_one('a[class="Link"]')
                    href = a['href']
                    content = article.select_one('div[class="VacancyItem-Description"]')
                    company = 'No name'
                    a = article.select_one('a[class="VacancyItem-CompanyTitle"]')
                    if a:
                        company = a.text
                    jobs.append({'title': title.text, 'url': domain + href,
                                 'description': content.text, 'company': company,
                                 'city_id': city, 'language_id': language})
            else:
                errors.append({'url': url, 'title': 'Div does not exists'})
        else:
            errors.append({'url': url, 'title': 'Page do not response'})

    return jobs, errors


def rabota(url, city=None, language=None):
    jobs = []
    errors = []
    domain = "https://" + url.split('/')[2]
    if url:
        resp = requests.get(url, headers[randint(0, len(headers) - 1)])
        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            main_div = soup.select_one('div.infinity-scroll.r-serp__infinity-list')
            if main_div:
                stop_article = main_div.select_one('div.r-serp-similar-title + article')
                article_lst = main_div.select('article[class~="vacancy-preview-card"]:not(.vacancy-preview-card_promoted)')
                for article in article_lst:
                    title = article.select_one('h3[class="vacancy-preview-card__title"] a')
                    if article == stop_article:
                        break
                    href = title['href']
                    content = article.select_one('div[class="vacancy-preview-card__content"]')
                    company = 'No name'
                    span = article.select_one('span[class="vacancy-preview-card__company-name"]')
                    if span:
                        company = span.text
                    jobs.append({'title': title.text, 'url': domain + href,
                                 'description': content.text, 'company': company,
                                 'city_id': city, 'language_id': language})
            else:
                errors.append({'url': url, 'title': 'Div does not exists'})
        else:
            errors.append({'url': url, 'title': 'Page do not response'})

    return jobs, errors