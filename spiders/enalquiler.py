# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from fake_useragent import UserAgent

UA = UserAgent()

headers = {
    'authority': 'www.enalquiler.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'dnt': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': UA.random,
    'sec-fetch-dest': 'document',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'referer': 'https://www.enalquiler.com/',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,es;q=0.6',
    'cookie': 'x_exp=0; _btrid=6c09e678-5bb9-4416-968c-19c1f1545dfe; hl=es; e_Enalquiler=csrfctrl%263a3f777eb882533e637be5f9097c6a205ce4802d0e639b543fe256e6ac53a191; s_Enalquiler=ref_ficha.....search_page.....search_params%269.....1.....YToxOTp7czo5OiJwcm92aW5jaWEiO3M6MjoiNDUiO3M6OToicG9ibGFjaW9uIjtzOjU6IjQ3OTk1IjtzOjk6ImRpc3RyaXRvcyI7czowOiIiO3M6NzoiYmFycmlvcyI7czowOiIiO3M6MTA6InByZWNpb19tYXgiO3M6MzoiNTAwIjtzOjExOiJvcmRlcl9maWVsZCI7czoxOiIwIjtzOjI6ImxiIjtzOjA6IiI7czozMjoiZmtfaWRfdGJsX3BvYmxhY2lvbmVzX2Rlc3RhY2Fkb3MiO3M6MToiOCI7czo0OiJwYWdlIjtzOjE6IjEiO3M6Nzoic2luX3JlcyI7czowOiIiO3M6MTI6InF1ZXJ5X3N0cmluZyI7czowOiIiO3M6MzoidHBsIjtzOjA6IiI7czozOiJtaWQiO3M6MDoiIjtzOjU6Im1pZGdjIjtzOjA6IiI7czoxMDoicmVzcG9uc2l2ZSI7czowOiIiO3M6NjoicmVmY29kIjtzOjc6InNlYXJjaDIiO3M6NjoiZm9vdGVyIjtzOjA6IiI7czoxNDoib25saW5lX2Jvb2tpbmciO3M6MDoiIjtzOjU6ImxlZWRzIjtzOjI2NDoiI3MsNTY5ODY4LDAsMCw1NTgyMTAxI3MsNTg0MTUyLDQ0NDc4OSwwLDU1NzAwODQjcywxMTg3NDIsMCwwLDU0NTMxNDgjcywzMDA0NTksNjE2MzYsMCw1NjQwODk4I3MsNDMxNjc5LDQ0OTkwLDAsNTM3NzcwMCNzLDMwMDQ1OSw2MTYzNiwwLDU2NDk0MDQjcyw0MzE2NzksNDQ5OTAsMCw1MTEzOTk0I3MsNDMxNjc5LDQ0OTkwLDAsNTY1NTAzOSNzLDk0NTIwOCw0NDk5MCwwLDU2MTU3NjUjcywzMDA0NTksNjE2MzYsMCw1NjUzNzMyI3MsMTc3Mjc5LDAsMCw1NTg4OTIxIjt9',
}


class EnalquilerSpider(scrapy.Spider):
    name = 'enalquiler'
    allowed_domains = ['enalquiler.com']
    start_urls = ['https://www.enalquiler.com/search?provincia=45&poblacion=47995']
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {**headers},
    }

    def parse(self, response):
        for item in response.xpath('//*[@class="propertyCard__infoWrapper"]'):
            price = float(item.xpath('./div/span[@class="propertyCard__price--value"]//text()')[0].root.strip().rstrip(
                '€').replace('.', ''))
            url = item.xpath('.//*[@class="qa-search-tituloCard-exist propertyCard__description--title"]/@href')[0].root
            yield {
                'price': price,
                'url': url,
                'rooms': 2,
            }

            next_page_element = response.xpath('//i[@class=" fa fa-chevron-right"]/@data-ena-href')
            if next_page_element:
                next_page_url = next_page_element[-1].root
                yield Request(next_page_url, callback=self.parse)
