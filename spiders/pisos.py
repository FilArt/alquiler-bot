# -*- coding: utf-8 -*-
from urllib.parse import urljoin

import scrapy
from fake_useragent import UserAgent
from scrapy import Request

BASE_URL = 'https://www.pisos.com'
UA = UserAgent()


class PisosSpider(scrapy.Spider):
    name = 'pisos'
    allowed_domains = ['pisos.com']
    start_urls = [urljoin(BASE_URL, '/alquiler/pisos-tarragona_capital/')]
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'User-Agent': UA.random,
        }
    }

    xp = '//div[contains(@class, "row") and contains(@class, "clearfix") and not(contains(@class, "ad"))]'

    def parse(self, response):
        for item in response.xpath(self.xp):
            url = urljoin(BASE_URL, item.attrib['data-navigate-ref'])
            try:
                price = float(item.xpath('.//div[@class="price"]//text()')[0].root.replace('.', '').strip('€').strip())
                yield {
                    'url': url,
                    'price': price,
                    'rooms': 2,
                }
            except ValueError:
                pass

        next_page_element = response.css('#lnkPagSig')
        if 'href' in next_page_element.attrib:
            next_page_url = urljoin(BASE_URL, next_page_element.attrib['href'])
            yield Request(next_page_url, callback=self.parse)
