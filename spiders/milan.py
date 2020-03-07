# -*- coding: utf-8 -*-
from urllib.parse import urljoin

import scrapy
from fake_useragent import UserAgent

BASE_URL = 'http://milanuncios.com/alquiler-de-pisos-en-tarragona-tarragona/'
UA = UserAgent()


class MilanSpider(scrapy.Spider):
    name = 'milan'
    allowed_domains = ['milanuncios.com']
    start_urls = [
        f'{BASE_URL}'
        '?fromSearch=1&hasta=500&vendedor=inmo'
    ]
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'authority': 'www.milanuncios.com',
            'dnt': '1',
            'upgrade-insecure-requests': '1',
            'user-agent': UA.random,
            'sec-fetch-dest': 'document',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,es;q=0.6',
        }
    }

    def parse(self, response):
        for item in response.xpath('//div[@class="aditem-detail"]'):
            url = item.xpath('./a[@class="aditem-detail-title"]/@href')[0].root
            price = float(item.xpath('.//div[@class="aditem-price"]/text()')[0].root.replace('.', ''))
            yield {
                'url': urljoin(BASE_URL, url),
                'price': price,
                'rooms': 2,
            }
