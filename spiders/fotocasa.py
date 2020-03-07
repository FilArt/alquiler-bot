# -*- coding: utf-8 -*-
from urllib.parse import urlencode, parse_qs, urljoin

import scrapy
import ujson
from fake_useragent import UserAgent
from scrapy import Request
from scrapy.http import Response

BASE_URL = 'https://www.fotocasa.es'
API_URL = 'https://api.fotocasa.es/PropertySearch/Search'
UA = UserAgent()


class Fotocasa(scrapy.Spider):
    name = 'fotocasa'
    allowed_domains = ['api.fotocasa.es']
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'authority': 'api.fotocasa.es',
            'accept': 'application/json, text/plain, */*',
            'origin': 'https://www.fotocasa.es',
            'sec-fetch-dest': 'empty',
            'user-agent': UA.random,
            'dnt': '1',
            'sec-fetch-site': 'same-site',
            'sec-fetch-mode': 'cors',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,es;q=0.6',
            'referer': 'https://www.fotocasa.es/en/rental/homes/tarragona-capital/eixample/l?latitude=41.1203&longitude=1.25965&combinedLocationIds=724,9,43,260,452,43148,0,1277,0&gridType=3',
        },
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.counter = 0

    def start_requests(self):
        url, params = self._build_url()
        request = scrapy.Request(url, callback=self.parse)
        request.meta['params'] = params
        return [request]

    def parse(self, response: Response):
        data = ujson.loads(response.text)
        items = data['realEstates']
        self.counter += len(items)
        if self.counter >= data['count']:
            return

        for item in items:
            price = 100
            tr = [p for p in [p['value'][0] for p in item['transactions']] if p > 0]
            if tr:
                price = min(tr)
            rooms = 2
            try:
                rooms = [i for i in item['features'] if i['key'] == 'rooms'][0]['value'][0]
            except IndexError:
                pass

            alquiler_url = item['detail']['en']
            yield {
                'url': urljoin(BASE_URL, alquiler_url),
                # 'images': ','.join(map((lambda x: x['url']), item['multimedias'])),
                'price': price,
                'rooms': rooms,
            }

        next_page_number = int(parse_qs(response.url)['pageNumber'][0]) + 1
        next_page = self._build_url(next_page_number)[0]
        yield Request(next_page, self.parse)

    @staticmethod
    def _build_url(page_number: int = 1):
        params = (
            ('combinedLocationIds', '724,9,43,260,452,43148,0,0,0'),
            ('culture', 'en-GB'),
            ('hrefLangCultures', 'ca-ES;es-ES;de-DE;en-GB'),
            ('isMap', 'false'),
            ('isNewConstruction', 'false'),
            ('isNewConstructionPromotions', 'false'),
            ('latitude', '41.1203'),
            ('longitude', '1.25965'),
            ('pageNumber', page_number),
            ('platformId', '1'),
            ('sortOrderDesc', 'true'),
            ('sortType', 'bumpdate'),
            ('transactionTypeId', '3'),
            ('propertyTypeId', '2'),
        )
        return f'{API_URL}/?{urlencode(params)}', params
