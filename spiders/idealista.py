# -*- coding: utf-8 -*-
from urllib.parse import urljoin

import scrapy
from fake_useragent import UserAgent
from scrapy import Request
from scrapy.http import Response

BASE_URL = 'https://www.idealista.com'
UA = UserAgent()


cookies = {
    '$cookie: userUUID': '8e00ba23-e136-4959-b6bb-3fdfe7eb1eac',
    '_pxhd': '6650e1555510d780a2574b060d26b838137645a909bdecea9aa5c8c9412d15d1:b1a86b51-5490-11ea-8298-15e090bf0b78',
    'cookieDirectiveClosed': 'true',
    'askToSaveAlertPopUp': 'true',
    '_pxvid': 'b1a86b51-5490-11ea-8298-15e090bf0b78',
    'cto_lwid': 'fb7ce517-fe14-44ac-98b1-ee5ed302fc70',
    'xtvrn': '$352991$',
    'xtan352991': '2-anonymous',
    'xtant352991': '1',
    'utag_main': 'v_id:01707209f5ae007ee0bc7c047df002069002c06100a82$_sn:1$_ss:1$_st:1582463020272$ses_id:1582461220272%3Bexp-session$_pn:1%3Bexp-session',
    'TestIfCookie': 'ok',
    'TestIfCookieP': 'ok',
    'vs': '33114=3757713',
    'pbw': '%24b%3d16800%3b%24o%3d99999%3b%24sw%3d1600%3b%24sh%3d768',
    'pid': '5210319609021216158',
    'pdomid': '9',
    'ABTasty': 'uid=j4qamtc37nyyjmpg&fst=1582461219534&pst=1582461241784&cst=1582461244784&ns=14&pvt=14&pvis=14&th=',
    'send9441ee40-99d9-4c5b-b859-e0e838519cea': '{\'friendsEmail\':null,\'email\':null,\'message\':null}',
    'SESSION': 'f2ce8050-319e-4c3a-a51b-e1dd20da6506',
    'contactf2ce8050-319e-4c3a-a51b-e1dd20da6506': '{\'email\':null,\'phone\':null,\'phonePrefix\':null,\'friendEmails\':null,\'name\':null,\'message\':null,\'message2Friends\':null,\'maxNumberContactsAllow\':10,\'defaultMessage\':true}',
    'cookieSearch-1': '/alquiler-viviendas/tarragona/nou-eixample-nord/:1583235097767',
    'WID': '856ee353ead52159|Xl5AH|Xl4/6',
}

class IdealistaSpider(scrapy.Spider):
    name = 'idealista'
    allowed_domains = ['idealista.com']
    start_urls = [
        urljoin(BASE_URL, f'alquiler-viviendas/tarragona/{area}/')
        for area in (
            'nou-eixample-nord/',
            'nou-eixample-sud/',
            'part-alta/',
            'barris-maritims/',
            'eixample/',
            'sant-pere-i-sant-pau/',
        )
    ]
    custom_settings = {
        'COOKIES_ENABLED': True,
        'DEFAULT_REQUEST_HEADERS': {
            'authority': 'www.idealista.com',
            'cache-control': 'max-age=0',
            'dnt': '1',
            'upgrade-insecure-requests': '1',
            'sec-fetch-dest': 'document',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,es;q=0.6',
            'user-agent': UA.random,
        }
    }

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, dont_filter=True, cookies=cookies)

    def parse(self, response: Response):
        for item in response.xpath('//div[@class="item-info-container"]'):
            url = urljoin(BASE_URL, item.xpath('./a[@class="item-link "]').attrib['href'])
            price = float(item.css('span.item-price::text')[0].root.replace('.', ''))
            rooms = 2
            yield {
                'url': url,
                'price': price,
                'rooms': rooms,
            }

        pagination = response.xpath('//div[@class="pagination"]//a')
        if pagination:
            next_page_url = urljoin(BASE_URL, pagination[-1].attrib['href'])
            current_page = self._get_page_from_url(response.url)
            next_page = self._get_page_from_url(next_page_url)

            if next_page > current_page:
                yield Request(next_page_url, callback=self.parse, cookies=cookies)

    @staticmethod
    def _get_page_from_url(url: str):
        ext = url.split('/')[-1]
        if '.htm' in ext:
            return int([i for i in ext if i.isdigit()][0])
        return 1
